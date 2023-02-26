import os

import plotly.express as px
import gradio as gr
import pandas as pd
from collections import defaultdict

from time import sleep
import openai

import logging
from dotenv import load_dotenv
import pinecone

default_region = 'us-west1-gcp'
openai_embed_model = "text-embedding-ada-002"

def get_data(num_names_per_category=2, num_categories=3):

    categories = ['Text,', 'Bio', 'Audio', 'Legal', 'Chatbot/Conversational AI', 'Summarization', 'MLOps/Platform', 'Code', 'Avatars', 'Image', 'Semantic Search', 'Game', 'Video', 'Data', 'Sentiment Analysis']
    num_categories = min(num_categories, len((categories)))

    data = query_pinecone(categories, num_categories, num_names_per_category)

    return data

def get_openai_embedding(apikey, data):
    """ Fetch an embedding w/ given data """
    openai.api_key = apikey
    try:
        res = openai.Embedding.create(input=data, engine=openai_embed_model)
    except:
        done = False
        while not done:
            sleep(5)
            try:
                res = openai.Embedding.create(
                    input=data, engine=openai_embed_model)
                print('retrying')
                done = True
            except Exception as e:
                logging.exception(e)
    return res

def query_pinecone(categories, n_categories=3, top_k=4):
    load_dotenv()

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_ENVIRONMENT'),
    )
    index = pinecone.Index("vc-content-oracle-big")

    out = defaultdict(list)


    # loop thru all the categories
    for category in categories[:n_categories]:

        #get vector for each category
        vector = get_openai_embedding(os.getenv('OPENAI_API_KEY'), category)['data'][0]['embedding']

        res = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            include_values=False,
        )

        for match in res['matches']:
            if 'Organization Name' not in match['metadata'] or 'Website' not in match['metadata']:
                print('no Organization Name')
                continue

            company_link = '<a href="' + match['metadata']['Website'] + '" style="cursor: pointer" target="_blank" rel="noopener noreferrer">' + match['metadata']['Organization Name'] + '</a>'
            out[category].append(company_link)

    return out

    """
    returns { 'matches': [{
        'id': 'A', 
        'metadata': { 
            'Organization Name': '', 
            'Organization Name URL': '', 
            'Last Funding Amount': '',
            'Last Funding Amount Currency': '', 
            'Last Funding Amount Currency (in USD)': '',
            'Website': '', 
            'Total Funding Amount': '', 
            'Total Funding Amount Currency': '',
            'Total Funding Amount Currency (in USD)': '', 
            'Last Funding Date': '',
            'Founded Date': '', 
            'Founded Date Precision': '', 
            'Last Funding Type': '',
            'Number of Employees': '', 
            'Full Description': '', 
            'Top 5 Investors': '',
        }, 
        'score': 0.01, 
        'values':[] 
        }]}
    """

def make_plot(category, num_categories, num_names_per_category):

    num_categories = int(num_categories)
    num_names_per_category = int(num_names_per_category)

    data = get_data(num_names_per_category, num_categories)
    names = []
    parents = []

    for category, names_list in data.items():
        names.extend(names_list)
        parents.extend([category] * len(names_list))

    unique_parents = list(set(parents))
    names += unique_parents
    parents += [''] * len(unique_parents)

    fig = px.treemap(
        names=names,
        parents=parents,
    )

    fig.update_traces(root_color="lightgrey")
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig

with gr.Blocks() as demo:
    category = gr.Textbox(label='Market Category')
    n_subcategories = gr.Number(label="Number of Subcategories")
    n_companies = gr.Number(label="Max Number of Companies per Subcategory")
    button = gr.Button("Generate")
    plot = gr.Plot(label="Plot")
    button.click(make_plot, inputs=[category, n_subcategories, n_companies], outputs=[plot])
    # demo.load(make_plot, inputs=[button, category], outputs=[plot])
    demo.launch()
