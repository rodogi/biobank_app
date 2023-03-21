import dash
import pickle
import dash_cytoscape as cyto
from dash.dependencies import Output, Input
from dash import dcc, dash_table, html
import pandas as pd


df = pd.read_csv('data/biobanks.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

with open('/Users/r.dorantesgilardi/app/data/elements.p', 'rb') as f:
    elements = pickle.load(f)
with open('/Users/r.dorantesgilardi/app/data/stylesheet.p', 'rb') as f:
    stylesheet = pickle.load(f)
with open('/Users/r.dorantesgilardi/app/data/chars.p', 'rb') as f:
    chars = pickle.load(f)

app.layout = html.Div([
    html.Div([
        cyto.Cytoscape(
            id='biobanks',
            layout={'name': 'preset'},
            style={'width': '100%', 'height': '700px'},
            maxZoom=1.5,
            minZoom=0.4,
            stylesheet=stylesheet,
            elements=elements

        )
    ], className='seven columns'),

    html.Div([
        dcc.Markdown('''
        #### Quantifying biobank impact

        *Click on each node to see more information about the biobank*.
    ''', id='my-text')],
        className='four columns'),

    html.Div([
        dash_table.DataTable(
    df.to_dict('records'),[{"name": i, "id": i} for i in df.columns],
    id='tbl')], className='one column'),
        ], className='row')

@app.callback(
    Output('my-text','children'),
    Input('biobanks','tapNodeData'),
)
def update_nodes(data):
    text = '''
        ## Quantifying biobank impact
        ###### Scroll right to see the biobank ranking

        ###### *--Click on each node to see more information about the biobank--*




        '''
    if data is None:
        return text 
    else:
        v = int(data['id'])
        update = (f"""
        * Paper: *{chars['paper'][v]}*
        * Year: {chars['year'][v]}
        * Community: **{chars['comm'][v]}**
        * Citations: {chars['citations'][v]}
        * Conditions studied: {chars['diseases'][v]}
        * Main conditions studied: {chars['main_disease'][v]}
        * Team Size: {chars['team_size'][v]}
        * Team Gender: {chars['female_proportion'][v]}
        * Lead: {chars['PI'][v]}
        """)

        return text + update

if __name__ == '__main__':
    app.run_server(debug=True)