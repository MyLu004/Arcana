import networkx as nx
from typing import List, Dict, Any, Optional
from models import ProductSuggestion, RoomType

class ProductKnowledgeGraph:
    """
    Mock Product Knowledge Graph using NetworkX
    In production, this would connect to a real graph database (Neo4j, etc.)
    """
    
    def __init__(self):
        self.graph = nx.Graph()
        self._initialize_graph()
    
    def _initialize_graph(self):
        """Populate graph with mock furniture data"""
        
        # Define products with attributes
        products = [
            # Living Room - Modern Style
            {
                "id": "LR-SOFA-001",
                "name": "Scandinavian Minimalist Sofa",
                "category": "seating",
                "base_price": 1200.0,
                "material": "fabric",
                "style": "modern",
                "room_type": ["living_room"],
                "dimensions": {"width": 84, "depth": 36, "height": 32},
                "size_fit": ["medium", "large"]
            },
            {
                "id": "LR-TABLE-001",
                "name": "Glass Coffee Table",
                "category": "table",
                "base_price": 450.0,
                "material": "glass",
                "style": "modern",
                "room_type": ["living_room"],
                "dimensions": {"width": 48, "depth": 24, "height": 18},
                "size_fit": ["small", "medium", "large"]
            },
            {
                "id": "LR-LAMP-001",
                "name": "Arc Floor Lamp",
                "category": "lighting",
                "base_price": 280.0,
                "material": "metal",
                "style": "modern",
                "room_type": ["living_room", "office"],
                "dimensions": {"width": 12, "depth": 12, "height": 80},
                "size_fit": ["small", "medium", "large"]
            },
            {
                "id": "LR-SIDE-001",
                "name": "Walnut Side Table",
                "category": "table",
                "base_price": 320.0,
                "material": "wood",
                "style": "modern",
                "room_type": ["living_room"],
                "dimensions": {"width": 20, "depth": 20, "height": 24},
                "size_fit": ["small", "medium", "large"]
            },
            
            # Bedroom - Modern Style
            {
                "id": "BR-BED-001",
                "name": "Platform Bed Frame",
                "category": "bed",
                "base_price": 890.0,
                "material": "wood",
                "style": "modern",
                "room_type": ["bedroom"],
                "dimensions": {"width": 60, "depth": 80, "height": 14},
                "size_fit": ["medium", "large"]
            },
            {
                "id": "BR-NIGHT-001",
                "name": "Floating Nightstand",
                "category": "storage",
                "base_price": 180.0,
                "material": "wood",
                "style": "modern",
                "room_type": ["bedroom"],
                "dimensions": {"width": 18, "depth": 16, "height": 12},
                "size_fit": ["small", "medium", "large"]
            },
            {
                "id": "BR-LAMP-001",
                "name": "Touch Control Table Lamp",
                "category": "lighting",
                "base_price": 95.0,
                "material": "metal",
                "style": "modern",
                "room_type": ["bedroom"],
                "dimensions": {"width": 6, "depth": 6, "height": 18},
                "size_fit": ["small", "medium", "large"]
            },
            
            # Office - Modern Style
            {
                "id": "OF-DESK-001",
                "name": "Adjustable Standing Desk",
                "category": "desk",
                "base_price": 650.0,
                "material": "wood",
                "style": "modern",
                "room_type": ["office"],
                "dimensions": {"width": 60, "depth": 30, "height": 48},
                "size_fit": ["medium", "large"]
            },
            {
                "id": "OF-CHAIR-001",
                "name": "Ergonomic Office Chair",
                "category": "seating",
                "base_price": 420.0,
                "material": "mesh",
                "style": "modern",
                "room_type": ["office"],
                "dimensions": {"width": 26, "depth": 26, "height": 48},
                "size_fit": ["small", "medium"]
            },
            {
                "id": "OF-SHELF-001",
                "name": "Industrial Bookshelf",
                "category": "storage",
                "base_price": 380.0,
                "material": "metal",
                "style": "modern",
                "room_type": ["office", "living_room"],
                "dimensions": {"width": 48, "depth": 12, "height": 72},
                "size_fit": ["medium", "large"]
            },
            
            # Small Space Specialists
            {
                "id": "SS-SOFA-001",
                "name": "Compact Loveseat",
                "category": "seating",
                "base_price": 680.0,
                "material": "fabric",
                "style": "modern",
                "room_type": ["living_room"],
                "dimensions": {"width": 58, "depth": 32, "height": 30},
                "size_fit": ["small"]
            },
            {
                "id": "SS-TABLE-001",
                "name": "Nesting Coffee Tables",
                "category": "table",
                "base_price": 240.0,
                "material": "wood",
                "style": "modern",
                "room_type": ["living_room"],
                "dimensions": {"width": 30, "depth": 20, "height": 16},
                "size_fit": ["small"]
            },
        ]
        
        # Add product nodes to graph
        for product in products:
            product_id = product["id"]
            self.graph.add_node(product_id, **product)
        
        # Define compatibility relationships (edges)
        compatibilities = [
            # Living Room Sets
            ("LR-SOFA-001", "LR-TABLE-001", {"relationship": "COMPATIBLE_WITH", "score": 0.95}),
            ("LR-SOFA-001", "LR-SIDE-001", {"relationship": "COMPATIBLE_WITH", "score": 0.90}),
            ("LR-SOFA-001", "LR-LAMP-001", {"relationship": "COMPATIBLE_WITH", "score": 0.85}),
            ("LR-TABLE-001", "LR-LAMP-001", {"relationship": "COMPATIBLE_WITH", "score": 0.80}),
            
            # Bedroom Sets
            ("BR-BED-001", "BR-NIGHT-001", {"relationship": "COMPATIBLE_WITH", "score": 0.95}),
            ("BR-NIGHT-001", "BR-LAMP-001", {"relationship": "COMPATIBLE_WITH", "score": 0.92}),
            
            # Office Sets
            ("OF-DESK-001", "OF-CHAIR-001", {"relationship": "COMPATIBLE_WITH", "score": 0.98}),
            ("OF-DESK-001", "OF-SHELF-001", {"relationship": "COMPATIBLE_WITH", "score": 0.85}),
            ("OF-CHAIR-001", "OF-SHELF-001", {"relationship": "COMPATIBLE_WITH", "score": 0.75}),
            ("OF-DESK-001", "LR-LAMP-001", {"relationship": "COMPATIBLE_WITH", "score": 0.80}),
            
            # Small Space Alternatives
            ("SS-SOFA-001", "SS-TABLE-001", {"relationship": "COMPATIBLE_WITH", "score": 0.93}),
            ("SS-SOFA-001", "LR-LAMP-001", {"relationship": "COMPATIBLE_WITH", "score": 0.85}),
        ]
        
        # Add edges
        for source, target, attrs in compatibilities:
            self.graph.add_edge(source, target, **attrs)
    
    def get_compatible_products(
        self,
        room_type: str,
        room_size: str = "medium",
        style_preference: str = "modern",
        max_results: int = 5
    ) -> List[ProductSuggestion]:
        """
        Query the graph for compatible products
        This is the CORE intelligence function
        """
        
        compatible_products = []
        
        # Filter nodes by room type and size
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            
            # Check if product matches criteria
            if (room_type in node_data.get("room_type", []) and
                room_size in node_data.get("size_fit", []) and
                node_data.get("style") == style_preference):
                
                # Calculate compatibility score based on graph connections
                neighbors = list(self.graph.neighbors(node_id))
                avg_compatibility = 0.7  # Base score
                
                if neighbors:
                    scores = [
                        self.graph[node_id][neighbor].get("score", 0.5)
                        for neighbor in neighbors
                    ]
                    avg_compatibility = sum(scores) / len(scores)
                
                compatible_products.append(
                    ProductSuggestion(
                        sku=node_data["id"],
                        name=node_data["name"],
                        base_price=node_data["base_price"],
                        material=node_data["material"],
                        category=node_data["category"],
                        compatibility_score=round(avg_compatibility, 2)
                    )
                )
        
        # Sort by compatibility score and return top N
        compatible_products.sort(key=lambda x: x.compatibility_score, reverse=True)
        return compatible_products[:max_results]
    
    def get_product_set(self, anchor_product_id: str) -> List[str]:
        """Get all products compatible with a given product"""
        if anchor_product_id not in self.graph:
            return []
        
        neighbors = list(self.graph.neighbors(anchor_product_id))
        return neighbors
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Return graph statistics for debugging"""
        return {
            "total_products": self.graph.number_of_nodes(),
            "total_relationships": self.graph.number_of_edges(),
            "categories": len(set(nx.get_node_attributes(self.graph, 'category').values())),
            "avg_compatibility": round(
                sum([data.get('score', 0) for _, _, data in self.graph.edges(data=True)]) / 
                max(self.graph.number_of_edges(), 1), 
                2
            )
        }

# Create singleton instance
pkg_service = ProductKnowledgeGraph()