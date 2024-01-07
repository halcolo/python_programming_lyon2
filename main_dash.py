import os
import config
import logging
import pandas as pd
from modules.corpus import Corpus
from utils.tools import clean_text_util
from program import full_search_engine_proc, search_engine
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import (
    Dash, 
    dash_table,  
    html)
import gc

path = os.path.dirname(os.path.abspath(__file__))

df = pd.read_csv(f'{path}/data/subjects.csv', header=0)
df.rename(columns={0: 'Subject', 1: 'Subreddit'}, inplace=True)


PAGE_ZISE = 15
TABLE_DICT_ROW_NAME = 'row'
last_active_cell = None
external_css = [f"{path}/css/custom_table_styling.css"]
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


content = list()
content_name = list()
content_name += [html.H1("Search engine")]

## Check if credentials are set and make an alert if not
if os.environ.get('CLIENT_SECRET') is None \
    or os.environ.get('CLIENT_SECRET') is None \
        or os.environ.get('CLIENT_SECRET') is None:
            content_name += [ dbc.Alert(
                "Please set your credentials in the 'config.py' file", 
                color="danger"
            )]


# Add table
data_table = dash_table.DataTable(
        data=df.to_dict('records'),
        columns=[{'id': str(c), 'name': str(c)} for c in df.columns],
        style_cell={'textAlign': 'left'},
        # Options de pagination
        page_current=0,
        page_size=PAGE_ZISE,
        style_cell_conditional=[
            {
                'if': {'column_id': 'name'},
                'textAlign': 'left'
            },
        ], id='tbl'
    )


keyword_input = html.Div(
    [
        dbc.Label("Key Word", html_for="keyword-text"),
        dbc.Input(type="text", id="keyword-text", placeholder="Enter key word"),
        dbc.FormText(
            "Example Llama Machine learning",
            color="secondary",
        ),
    ],
    className="mb-6",
)


loading_obj = dbc.Spinner(
                id="tab-response",
                children=[html.Div([html.Div(id="loading-output-2")])],
                color="primary",
            )
button = dbc.Button("Submit", color="primary", className="me-1", id="add-btn")

form = dbc.Form([
        dbc.Row(content_name),
         
        dbc.Row([
            dbc.Col(html.Div(data_table)),
            dbc.Col(html.Div([keyword_input, button]))
        ]),
        dbc.Row([
            dbc.Col(
                html.Div([loading_obj]),
                ),
            
        ]),
    ])

content += [form]
app.layout = dbc.Container(content, fluid=True)

@app.callback(
    Output('tab-response', 'children'), 
    [
        Input("add-btn", "n_clicks"),
        State("keyword-text", "value"),
        State("tbl", "active_cell")
    ]
)
def render_tab_content(n_clicks, keyword_text, active_cell):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    if active_cell and keyword_text is not None:
        
        
        # Getting values from table
        arxiv_kw = df.iloc[active_cell['row']]['Subject']
        reddit_kw = df.iloc[active_cell['row']]['Subreddit']
        
        collection = full_search_engine_proc(
            arxiv_kw=arxiv_kw, 
            subreddit_kw=reddit_kw)
                
        tokens_kw = clean_text_util(keyword_text)
    
        try:
            corpus = Corpus()

            max_articles = 10
            for i in range(max_articles):
                doc = collection[i]
                corpus.add(author=doc.author , doc=doc)
                    
            vocab = corpus.stats()
            vocab = vocab.sort_values('count', ascending=False)
                        
            result = search_engine(collection=collection,
                        keywords=tokens_kw)
            result_df = pd.DataFrame(result)
            
            table = dbc.Table.from_dataframe(result_df, striped=True, bordered=True, hover=True)

            return table

            
        except TypeError as t:
            logging.error(t)
            raise TypeError
        except ValueError as v:
            logging.error(v)
            raise ValueError
        

        
    return "No tab selected"

if __name__ == '__main__':
    app.run_server(debug=True)