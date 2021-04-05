import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import main

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# Get figures from main function
topo_figs, clustered_figs, full_clustered_figs, force_figs = main.main()

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.layout = html.Div([
    html.Label('Layout Options:', style = {'width': '25%', 'display': 'inline-block'}, id = 'lay_ops'),
    html.Label('Node Options:', style = {'width': '25%', 'display': 'inline-block'}, id = 'node_ops'),
    html.Label('Work Allocation:', style = {'width': '50%', 'display': 'inline-block'}, id = 'work_alloc'),

    html.Div(
        dcc.RadioItems(
            id = 'layout-radio',
            options = [
                {'label': 'Topological Sort', 'value': 'topo'},
                {'label': 'Agent Clustering Sort', 'value': 'cluster'},
                {'label': 'Force Directed Sort', 'value': 'force'}
            ],
            value = 'topo'
        ), style = {'width': '25%', 'display': 'inline-block'}
    ),

    
    html.Div(
        dcc.RadioItems(
            id = 'full-radio',
            options = [
                {'label': 'Actions Only', 'value': 'acts'},
                {'label': 'Full Network', 'value': 'full'}
            ],
            value = 'acts'
        ), style = {'width': '25%', 'display': 'inline-block'}
    ),

    # Checkbox to show work allocation
    html.Div(
        dcc.RadioItems(
            id = 'alloc-checkbox',
            options = [
                {'label': 'Show work allocation','value': 'show'},
                {'label': 'Hide work allocation', 'value': ''}
            ],
            value = 'show'
        ), style = {'width': '50%', 'display': 'inline-block'}
    ),

    # Figure
    dcc.Graph(id = 'network-graph'),
    
    # Slider to select control mode
    dcc.Slider(
        id = 'mode-slider',
        min = 0,
        max = 2,
        marks = {
            0: 'scrambled',
            1: 'tactical/opportunistic',
            2: 'strategic'
        },
        value = 0
    )
])

# callback for when "layout options" selection is changed
@app.callback(
    Output('alloc-checkbox','style'),
    Output('work_alloc', 'style'),
    [Input('layout-radio','value')])
def hide_checkbox(layoutstyle):
    if layoutstyle == 'topo' or layoutstyle == 'force':
        return {'width': '50%', 'display': 'inline-block'}, {'width': '50%', 'display': 'inline-block'}
    else:
        return {'display': 'none'}, {'width': '50%', 'display': 'inline-block'}

# callback for updating graph
@app.callback(
    Output('network-graph', 'figure'),
    [Input('mode-slider', 'value'),
    Input('alloc-checkbox','value'),
    Input('layout-radio','value'),
    Input('full-radio', 'value')])
def update_output(modeval, showval, layoutval, fullval):
    # update graph based on slider value and checkbox
    if fullval == 'acts':
        if layoutval == 'topo':
            if showval == 'show':
                k = 'show'
            else:
                k = 'no-show'
            fig = topo_figs[k][modeval]
        elif layoutval == 'force':
            if showval == 'show':
                k = 'showf'
            else:
                k = 'no-showf'
            fig = force_figs[k][modeval]
        else:
            fig = clustered_figs[modeval]
    else:
        if layoutval == 'topo':
            if showval == 'show':
                k = 'show-full'
            else:
                k = 'no-show-full'
            fig = topo_figs[k][modeval]
        elif layoutval == 'force':
            if showval == 'show':
                k = 'show-fullf'
            else:
                k = 'no-show-fullf'
            fig = force_figs[k][modeval]
        else:
            fig = full_clustered_figs[modeval]
    return fig

if __name__ == '__main__':
    app.run_server(debug=False)
