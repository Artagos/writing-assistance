import dash
import dash_cytoscape as cyto
from dash import html, dcc, Input, Output, State, callback_context,ALL
import json
from text_generation import example_usage

def build_cytoscape_elements(knowledge_graph):
    """
    Convert a KnowledgeGraph instance into elements for Dash Cytoscape visualization.
    
    Args:
        knowledge_graph: Instance of KnowledgeGraph class
        
    Returns:
        List of dictionaries representing nodes and edges for Cytoscape
    """
    elements = []
    
    # Add nodes
    for node_id, node in knowledge_graph.nodes.items():
        elements.append({
            'data': {
                'id': str(node_id),
                'label': node.name,
                'description': node.description,
                'attributes': node.attributes
            }
        })
    
    # Add edges
    for edge in knowledge_graph.edges:
        elements.append({
            'data': {
                'source': str(edge.source.id),
                'target': str(edge.target.id),
                'label': edge.relation_text,
                'attributes': edge.attributes
            }
        })
    
    return elements

kg = example_usage()  # Assuming the above code is in a file named example_usage.py

# Define nodes and edges
elements = build_cytoscape_elements(kg)

# Initialize Dash app
app = dash.Dash(__name__)

# Define the context menu options
context_menu_options = [
    {'id': 'generate', 'label': 'Generate Content'},
    {'id': 'edit', 'label': 'Edit Node'},
    {'id': 'delete', 'label': 'Delete Node'}
]

app.layout = html.Div([
    # Context menu div
    html.Div(
        id='context-menu',
        style={
            'display': 'none',
            'position': 'fixed',
            'background-color': 'white',
            'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)',
            'border': '1px solid #ddd',
            'border-radius': '4px',
            'z-index': 1000
        },
        children=[
            html.Div(
                [
                    html.Button(
                    option['label'],
                    id={'type': 'context-button', 'index': option['id']},
                    style={
                        'display': 'block',
                        'width': '100%',
                        'padding': '8px 16px',
                        'border': 'none',
                        'background': 'none',
                        'cursor': 'pointer',
                        'text-align': 'left'
                    }
                ) for option in context_menu_options]
            )
        ]
    ),
    
    # Store the selected node data
    dcc.Store(id='selected-node-data'),
    
    # Cytoscape component
    cyto.Cytoscape(
        id='cytoscape-graph',
        elements=elements,
        style={'width': '100%', 'height': '600px'},
        layout={'name': 'cose'},  # 'circle', 'grid', 'cose', etc.
        stylesheet=[
            {'selector': 'node', 'style': {'content': 'data(label)', 'background-color': '#3498db', 'color': 'black'}},
            {'selector': 'edge', 'style': {
                'line-color': '#ccc',
                'target-arrow-color': '#ccc',
                'target-arrow-shape': 'triangle',
                'curve-style': 'bezier',
                'label': 'data(label)',  # Display the label on edges
                'font-size': '10px',
                'text-rotation': 'autorotate',
                'text-margin-y': -10  # Adjust label position
            }}
        ]
    ),
])

@app.callback(
    [Output('context-menu', 'style'),
     Output('selected-node-data', 'data')],
    [Input('cytoscape-graph', 'tapNodeData'),
     Input('cytoscape-graph', 'mouseoverNodeData')],
    [State('context-menu', 'style')]
)
def show_context_menu(tap_node, mouseover_node, style):
    if not callback_context.triggered:
        return [style, None]
    
    trigger = callback_context.triggered[0]['prop_id']
    
    if 'tapNodeData' in trigger and tap_node:
        # Show context menu near the clicked node
        new_style = {
            'display': 'block',
            'position': 'fixed',
            # Position the menu relative to the viewport
            'left': '50%',  
            'top': '50%',
            'background-color': 'white',
            'box-shadow': '0px 0px 10px rgba(0,0,0,0.1)',
            'border': '1px solid #ddd',
            'border-radius': '4px',
            'z-index': 1000
        }
        return [new_style, tap_node]
    
    # Hide context menu
    style['display'] = 'none'
    return [style, None]

@app.callback(
    Output('cytoscape-graph', 'elements'),
    [Input({'type': 'context-button', 'index': ALL}, 'n_clicks')],
    [State('selected-node-data', 'data'),
     State('cytoscape-graph', 'elements')]
)
def handle_context_menu_click(n_clicks, node_data, elements):
    if not callback_context.triggered or not node_data:
        return elements
    
    # Get which button was clicked
    triggered_id = json.loads(callback_context.triggered[0]['prop_id'].split('.')[0])
    action = triggered_id['index']
    
    if action == 'generate':
        # Handle generate content action
        pass
    elif action == 'edit':
        # Handle edit node action
        pass
    elif action == 'delete':
        # Handle delete node action
        elements = [ele for ele in elements 
                   if ele['data']['id'] != node_data['id']]
    
    return elements

if __name__ == '__main__':
    app.run(debug=True)

