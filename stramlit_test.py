from turtle import left
import streamlit as st
import networkx as nx
from pyvis.network import Network
from streamlit.components.v1 import html
from knowledge_graph import KnowledgeGraph, Node
from text_generation import text_generator

# Add custom CSS
st.markdown("""
    <style>
    .stButton > button {
        width: 100%;
    }
    .graph-container {
        position: fixed;
        left: 0;
        top: 60px;  /* Account for Streamlit's top bar */
        width: 400px;
        height: 100vh;
        z-index: 1;
    }
    .writing-container {
        border: 1px solid #ddd;
        border-radius: 5px;
        padding: 20px;
        height: 600px;
        width: 100%;
        overflow-y: auto;
        background-color: black;
        margin-bottom: 10px;
        font-family: 'Times New Roman', serif;
        line-height: 1.6;
          /* Match the graph container width */
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for generated content if it doesn't exist
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = ""

# Dummy node interaction simulation
st.title("Interactive Knowledge Graph")

def build_visual_graph(knowledge_graph: KnowledgeGraph):
    # Create a Pyvis network with smaller width
    net = Network(height="600px", width="700px", directed=True,)
    
    # Add nodes and edges from the KnowledgeGraph instance
    for node in knowledge_graph.nodes:
        
        actual_node= knowledge_graph.nodes[node]
        net.add_node(node, title=actual_node.name)
    for edge in knowledge_graph.edges:
        net.add_edge(edge.source.id, edge.target.id, title=edge.relation_text)
    
    # Add click handler JavaScript
    net.set_options('''
    {
      "interaction": {
        "navigationButtons": true,
        "selectable": true
      },
      "nodes": {
        "shape": "dot",
        "size": 16
      },
      "physics": {
        "stabilization": false
      }
    }
    ''')
    
    # Save and embed HTML manually to handle events
    net.save_graph("graph.html")
    with open("graph.html", "r", encoding="utf-8") as f:
        html_graph = f.read()
    html(html_graph, height=500, width=700)  # Update width from 400 to 300

# Example usage
# Create a knowledge graph
kg = KnowledgeGraph()

# Add some nodes
intro= Node('intro', 'Introducción', 'Se presenta la idea de construir una herramienta de asistencia a la escritura, introduciendo como novedad una representación en grafo del contenido que se quiere lograr o que se va construyendo.')

p1= Node('p1', 'Primer párrafo', 'Se enuncian los desafíos del proyecto: la extracción de entidades y relaciones, la construcción de un grafo de conocimiento a partir de texto plano, y la interacción con dicho grafo.')

p2= Node('p2', 'Segundo párrafo', 'Se detalla la interacción con el grafo de conocimiento. Se explica que la generación de texto en los nodos se basa en un prompt construido a partir del contenido del nodo, sus relaciones y el contenido de los nodos relacionados.')

p3= Node('p3', 'Tercer párrafo', 'Se plantea un problema de dependencia circular al generar texto como se describe en el segundo párrafo. Si dos nodos dependen uno del otro, no se puede generar contenido porque el de uno depende del otro.')


# Add nodes to the graph
kg.add_node(intro)
kg.add_node(p1)
kg.add_node(p2)
kg.add_node(p3)

# Create relationships between nodes
kg.add_edge('p1', 'intro', 'El primer párrafo desarrolla los desafíos mencionados en la introducción.')
kg.add_edge('p2', 'p1', 'El segundo párrafo amplía la explicación sobre la interacción con el grafo mencionada en el primer párrafo.')
kg.add_edge('p3', 'p2', 'El tercer párrafo plantea un problema de dependencia circular al generar texto como se describe en el segundo párrafo.')

# Update the column layout
# Remove the columns and wrap the graph in a div
st.markdown('<div class="graph-container">', unsafe_allow_html=True)
build_visual_graph(kg)
selected_node = st.selectbox("Select a node:", [node for node in kg.nodes])
st.markdown('</div>', unsafe_allow_html=True)

# Main content area (no need for columns anymore)
st.subheader("Generated Text")

# Display the cumulative generated content
st.markdown("""
    <div class="writing-container">
    
        {}
        
    
""".format(st.session_state.generated_content), unsafe_allow_html=True)

# Add controls for the writing area
if selected_node:
    node_data:Node = kg.nodes[selected_node]
    st.markdown("**Selected Node:**")
    st.markdown(f"**{node_data.name}**")
    st.markdown("**Description:**")
    st.markdown(node_data.description)
    
    # Add a text generation button
    if st.button("Generate Content"):
        prompt_for_generation=node_data.build_prompt()
        generated_text= text_generator.generate_text(prompt_for_generation)
        node_data.generated_content=generated_text
        # Here you would add your actual text generation logic
        new_content = f"""
### {node_data.name}
{generated_text}

"""
        # Append new content to existing content
        st.session_state.generated_content += new_content
        st.rerun()

# Add this below the writing container
if st.button("Clear Generated Text"):
    st.session_state.generated_content = ""
    st.rerun()
