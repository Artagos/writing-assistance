from numpy import full
from sympy import fu
from llm_text_generation import GeminiTextGenerator
from knowledge_graph import Node, Edge, KnowledgeGraph
import os
from dotenv import load_dotenv
import asyncio

load_dotenv()

api_key=os.getenv("GEMINI_API_KEY")
system_instructions= os.getenv("LLM_INSTRUCTION")
text_generator = GeminiTextGenerator(api_key,system_instructions)

# Example usage
def example_usage():
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
    # Generate a prompt for the intro node
    
    
    
    full_text=''
    prompt1 = intro.build_prompt()  
    generated_text = text_generator.generate_text(prompt1)
    intro.generated_content=generated_text
    full_text+=generated_text
    full_text+="\n---------------------------------------------------\n"
    
    prompt2 = p1.build_prompt()
    generated_text = text_generator.generate_text(prompt2)
    p1.generated_content=generated_text
    full_text+=generated_text
    full_text+="\n---------------------------------------------------\n"
    
    prompt3 = p2.build_prompt()
    generated_text =text_generator.generate_text(prompt3)
    p2.generated_content=generated_text
    full_text+=generated_text
    full_text+="\n---------------------------------------------------\n"
    
    prompt4 = p3.build_prompt()
    generated_text = text_generator.generate_text(prompt4)
    p3.generated_content=generated_text
    full_text+=generated_text
    full_text+="\n---------------------------------------------------\n"
    
    
    kg.visualize()
    print("Generated Prompts:")
    print(prompt1)
    print("---------------------------------------------------")
    print(prompt2)
    print("---------------------------------------------------")
    print(prompt3)
    print("---------------------------------------------------")
    print(prompt4)
    print("Generated Content:")
    # Initialize the text generator
    
    # Generate text using the prompt
    
    print(full_text)
    return kg


if __name__ == "__main__":
    example_usage()