import plotly.express as px
import altair as alt
import gradio as gr
import numpy as np
import pandas as pd
from vega_datasets import data


def make_plot(plot_type):
    if plot_type == "generative AI":
        fig = px.treemap(
            names = ["Eve","Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
            parents = ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"]
        )
        fig.update_traces(root_color="lightgrey")
        fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
        return fig
    else:
        raise Exception("Invalid plot type")

with gr.Blocks() as demo:
    button = gr.Radio(label="Plot type", choices=['generative AI'], value='scatter_plot')
    plot = gr.Plot(label="Plot")
    button.change(make_plot, inputs=button, outputs=[plot])
    demo.load(make_plot, inputs=[button], outputs=[plot])
    demo.launch()
