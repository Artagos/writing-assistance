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

# Example usage
def example_usage():
    # Create a knowledge graph
    kg = KnowledgeGraph()
    
    # Add some nodes
    intro = Node("intro", "Introduction", "Introduction of a loving story that begins with a swordsman")
    par1 = Node("paragraph1", "First Paragraph", "A paragraph explaining its background")
    par2 = Node("paragraph2", "Second Paragraph", "A paragraph talking about her lover")
    
    # Add nodes to the graph
    kg.add_node(intro)
    kg.add_node(par1)
    kg.add_node(par2)
    
    # Create relationships between nodes
    kg.add_edge("paragraph1", "intro", "makes funny allutions ")
    kg.add_edge("paragraph2", "paragraph1", "puts examples of what happened in")
    
    
    # Generate a prompt for the intro node
    prompt1 = intro.build_prompt()
    prompt2 = par1.build_prompt()
    prompt3 = par2.build_prompt()
    
    kg.visualize()
    print("Generated Prompts:")
    print(prompt1)
    print(prompt2)
    print(prompt3)
    print("Generated Content:")
    # Initialize the text generator
    text_generator = GeminiTextGenerator(api_key,system_instructions)
    
    # # Generate text using the prompt
    # full_text=''
    # generated_text = text_generator.generate_text(prompt1)
    # full_text+=generated_text
    # full_text+="\n---------------------------------------------------\n"
    # generated_text = text_generator.generate_text(prompt2)
    # full_text+=generated_text
    # full_text+="\n---------------------------------------------------\n"
    # generated_text =text_generator.generate_text(prompt3)
    # full_text+=generated_text
    # full_text+="\n---------------------------------------------------\n"
    
    # print(full_text)
    return kg


# if __name__ == "__main__":
#     example_usage()