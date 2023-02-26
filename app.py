import os

import plotly.express as px
import gradio as gr
import pandas as pd
from collections import defaultdict

from dotenv import load_dotenv

import pinecone

"""
(Pdb) pp data.describe()
       Category  Name                   URL    $ Raised     Investors Founded                 HQ            Focus
count       540   540                   540         366           382     511                509              540
unique       17   540                   540         203           366      19                217              365
top        Text  Seek  https://www.seek.ai/  $2,000,000  Y Combinator    2021  San Francisco, CA  Writing/Editing
freq        132     1                     1          18             8     106                 75               12
"""

def get_data(num_names_per_category=2, num_categories=3):

    categories = ['Text,', 'Bio', 'Audio', 'Legal', 'Chatbot/Conversational AI', 'Summarization', 'MLOps/Platform', 'Code', 'Avatars', 'Image', 'Semantic Search', 'Game', 'Video', 'Data', 'Sentiment Analysis']
    num_categories = min(num_categories, len((categories)))

    data = query_pinecone(categories, num_categories, num_names_per_category)

    return data

def query_pinecone(categories, n_categories=3, top_k=4):
    load_dotenv()

    pinecone.init(
        api_key=os.getenv('PINECONE_API_KEY'),
        environment=os.getenv('PINECONE_ENVIRONMENT'),
    )
    index = pinecone.Index("vc-content-oracle-big")

    out = defaultdict(list)


    # loop thru all the categories
    for categories in categories[:n_categories]:

        #get vector for each category
        vector = [0.0] * 1536

        res = index.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            include_values=True,
        )

        for match in res['matches']:
            if 'company' not in match['metadata']:
                continue
            # link = '<a href="' + match['metadata']['url'] + '" style="cursor: pointer" target="_blank" rel="noopener noreferrer">' + match['metadata']['company'] + '</a>'
            # out[category].append(link)
            out[category].append(match['metadata']['company'])

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
