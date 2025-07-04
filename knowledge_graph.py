from narwhals import String
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    """
    Represents a node in a knowledge graph that stores information about an entity.
    """
    def __init__(self, id, name, description="", attributes=None):
        """
        Initialize a node with an identifier, name, description, and optional attributes.
        
        Args:
            id: Unique identifier for the node
            name: Name of the entity
            description: Detailed description of what kind of content to generate with this entity
            attributes: Dictionary of additional attributes for the entity
        """
        self.id = id
        self.name = name
        self.description = description
        self.attributes = attributes or {}
        self.incoming_edges = []
        self.outgoing_edges = []
        self.generated_content:String=None
    
    def add_outgoing_edge(self, edge):
        """
        Add an outgoing edge from this node.
        
        Args:
            edge: The Edge object connecting this node to another
        """
        self.outgoing_edges.append(edge)
    
    def add_incoming_edge(self, edge):
        """
        Add an incoming edge to this node.
        
        Args:
            edge: The Edge object connecting another node to this one
        """
        self.incoming_edges.append(edge)
    
    def get_related_nodes(self):
        """
        Get all nodes directly connected to this node.
        
        Returns:
            List of tuples containing (related_node, edge, is_outgoing)
        """
        related = []
        for edge in self.outgoing_edges:
            related.append((edge.target, edge, True))
        for edge in self.incoming_edges:
            related.append((edge.source, edge, False))
        return related
    def get_outgoing_nodes(self):
        """
        Get all nodes directly connected to this node.
        
        Returns:
            List of tuples containing (related_node, edge, is_outgoing)
        """
        related = []
        for edge in self.outgoing_edges:
            related.append((edge.target, edge, True))

        return related
    
    def get_incoming_nodes(self):
        """
        Get all nodes directly connected to this node.
        
        Returns:
            List of tuples containing (related_node, edge, is_outgoing)
        """
        related = []
        for edge in self.incoming_edges:
            related.append((edge.source, edge, False))

        return related
    
    def build_prompt(self, include_related=True, max_related=5, prompt_template=None):
        """
        Build a prompt for text generation using this node's content and optionally
        the content of related nodes and their relationships.
        
        Args:
            include_related: Whether to include related nodes in the prompt
            max_related: Maximum number of related nodes to include
            prompt_template: Custom template for the prompt. If None, a default template is used.
            
        Returns:
            A string containing the generated prompt
        """
        if prompt_template is None:
            prompt = f"Entidad: {self.name}\n\nDescripción: {self.description}\n\n"
            
            if include_related and self.get_outgoing_nodes():
                prompt += "Entidades relacionadas:\n"
                related_nodes = self.get_outgoing_nodes()
                # Limit the number of related nodes to avoid overly long prompts
                for (node, edge, is_outgoing) in related_nodes[:max_related]:
                    relation_text = edge.relation_text
                    if is_outgoing:
                        prompt += f"- {self.name} {relation_text} {node.name}\n"
                        prompt += f"  Contenido de {node.name}: {node.generated_content}\n"
                    else:
                        prompt += f"- {node.name} {relation_text} {self.name}\n"
                        prompt += f"  {node.name}: {node.description}\n"
                
                prompt += "\nGenera contenido para la entidad anterior, considerando su descripción y relaciones."
            else:
                prompt += "Genera contenido para la entidad anterior basado en su descripción."
        else:
            # Use the custom template with some basic variable substitution
            prompt = prompt_template.replace("{name}", self.name)
            prompt = prompt.replace("{description}", self.description)
            
            if "{related}" in prompt_template and include_related:
                related_text = ""
                related_nodes = self.get_related_nodes()
                for (node, edge, is_outgoing) in related_nodes[:max_related]:
                    relation_text = edge.relation_text
                    if is_outgoing:
                        related_text += f"{self.name} {relation_text} {node.name}; "
                    else:
                        related_text += f"{node.name} {relation_text} {self.name}; "
                prompt = prompt.replace("{related}", related_text)
        
        return prompt


class Edge:
    """
    Represents a directed edge in a knowledge graph that connects two nodes
    and stores information about their relationship.
    """
    def __init__(self, source, target, relation_text, attributes=None):
        """
        Initialize an edge with source and target nodes, relation text, and optional attributes.
        
        Args:
            source: The source Node object
            target: The target Node object
            relation_text: Text describing the relationship between source and target
            attributes: Dictionary of additional attributes for the relationship
        """
        self.source = source
        self.target = target
        self.relation_text = relation_text
        self.attributes = attributes or {}
        
        # Register this edge with the source and target nodes
        source.add_outgoing_edge(self)
        target.add_incoming_edge(self)


class KnowledgeGraph:
    """
    Represents a knowledge graph consisting of nodes and edges.
    """
    def __init__(self):
        """
        Initialize an empty knowledge graph.
        """
        self.nodes = {}
        self.edges = []
    
    def add_node(self, node):
        """
        Add a node to the graph.
        
        Args:
            node: The Node object to add
            
        Returns:
            The added Node object
        """
        self.nodes[node.id] = node
        return node
    
    def get_node(self, node_id):
        """
        Get a node by its ID.
        
        Args:
            node_id: The ID of the node to retrieve
            
        Returns:
            The Node object if found, None otherwise
        """
        return self.nodes.get(node_id)
    
    def add_edge(self, source_id, target_id, relation_text, attributes=None):
        """
        Add an edge between two nodes.
        
        Args:
            source_id: ID of the source node
            target_id: ID of the target node
            relation_text: Text describing the relationship
            attributes: Dictionary of additional attributes for the relationship
            
        Returns:
            The created Edge object if successful, None if either node doesn't exist
        """
        source = self.get_node(source_id)
        target = self.get_node(target_id)
        
        if source is None or target is None:
            return None
        
        edge = Edge(source, target, relation_text, attributes)
        self.edges.append(edge)
        return edge
    
    def get_all_nodes(self):
        """
        Get all nodes in the graph.
        
        Returns:
            List of all Node objects
        """
        return list(self.nodes.values())
    
    def get_all_edges(self):
        """
        Get all edges in the graph.
        
        Returns:
            List of all Edge objects
        """
        return self.edges
    
    def visualize(self):
        """
        Visualize the knowledge graph using networkx and matplotlib.
        """
        G = nx.DiGraph()  # Create a directed graph

        # Add nodes and edges to the graph
        for node_id, node in self.nodes.items():
            G.add_node(node_id, label=node.name, )

        for edge in self.edges:
            G.add_edge(edge.source.id, edge.target.id, label=edge.relation_text)

        # Draw the graph
        pos = nx.spring_layout(G)  # Layout for positioning nodes
        nx.draw(G, pos, with_labels=True, node_size=3000, node_color="lightblue", font_size=10, font_weight="bold")
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color="red")

        # Show the graph
        plt.title("Knowledge Graph Visualization")
        plt.show()
    


