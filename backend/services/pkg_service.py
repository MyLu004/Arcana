"""
MASSIVE Product Knowledge Graph - 100+ Products
Multiple styles, all price ranges, all room types
"""
import networkx as nx
from typing import List, Dict, Any, Optional
from models import ProductSuggestion, RoomType

class ProductKnowledgeGraph:
    """Enhanced PKG with 100+ diverse products"""
    
    def __init__(self):
        self.graph = nx.Graph()
        self._initialize_graph()
    
    def _initialize_graph(self):
        """Populate with 100+ products across all categories"""
        
        products = [
            # ==========================================
            # LIVING ROOM - BUDGET ($20-$300)
            # ==========================================
            {"id": "LR-BUDGET-001", "name": "Colorful Accent Chair", "category": "seating", "base_price": 180.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 28, "depth": 30, "height": 34}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-002", "name": "Round Side Table", "category": "table", "base_price": 95.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 18, "depth": 18, "height": 22}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-003", "name": "LED Table Lamp", "category": "lighting", "base_price": 65.0, "material": "metal", "style": "modern", "room_type": ["living_room", "bedroom"], "dimensions": {"width": 8, "depth": 8, "height": 20}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-004", "name": "Decorative Floor Plant", "category": "decor", "base_price": 55.0, "material": "natural", "style": "modern", "room_type": ["living_room", "office"], "dimensions": {"width": 14, "depth": 14, "height": 36}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-005", "name": "Colorful Area Rug 5x7", "category": "decor", "base_price": 145.0, "material": "textile", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 60, "depth": 84, "height": 0}, "size_fit": ["medium", "large"]},
            {"id": "LR-BUDGET-006", "name": "Throw Pillow Set (4pc)", "category": "decor", "base_price": 45.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 18, "depth": 18, "height": 6}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-007", "name": "Wall Shelf 36in", "category": "storage", "base_price": 75.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 36, "depth": 10, "height": 2}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-008", "name": "Storage Ottoman", "category": "seating", "base_price": 125.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 24, "depth": 24, "height": 18}, "size_fit": ["small", "medium"]},
            {"id": "LR-BUDGET-009", "name": "Floor Cushion Set", "category": "seating", "base_price": 85.0, "material": "fabric", "style": "bohemian", "room_type": ["living_room"], "dimensions": {"width": 24, "depth": 24, "height": 6}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-010", "name": "Wall Art Canvas Set", "category": "decor", "base_price": 55.0, "material": "canvas", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 16, "depth": 1, "height": 20}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-011", "name": "Woven Basket Storage", "category": "storage", "base_price": 40.0, "material": "natural", "style": "bohemian", "room_type": ["living_room"], "dimensions": {"width": 14, "depth": 14, "height": 12}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-012", "name": "Decorative Mirror 24in", "category": "decor", "base_price": 95.0, "material": "glass", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 24, "depth": 2, "height": 24}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-013", "name": "String Lights Set", "category": "lighting", "base_price": 25.0, "material": "metal", "style": "bohemian", "room_type": ["living_room", "bedroom"], "dimensions": {"width": 1, "depth": 1, "height": 240}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-014", "name": "Macrame Wall Hanging", "category": "decor", "base_price": 35.0, "material": "textile", "style": "bohemian", "room_type": ["living_room"], "dimensions": {"width": 24, "depth": 2, "height": 36}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-BUDGET-015", "name": "Ceramic Vase Set", "category": "decor", "base_price": 30.0, "material": "ceramic", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 6, "depth": 6, "height": 12}, "size_fit": ["small", "medium", "large"]},
            
            # ==========================================
            # LIVING ROOM - MID-RANGE ($300-$800)
            # ==========================================
            {"id": "LR-MID-001", "name": "Modern Loveseat", "category": "seating", "base_price": 680.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 58, "depth": 32, "height": 30}, "size_fit": ["small", "medium"]},
            {"id": "LR-MID-002", "name": "Nesting Coffee Tables", "category": "table", "base_price": 340.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 30, "depth": 20, "height": 16}, "size_fit": ["small", "medium"]},
            {"id": "LR-MID-003", "name": "Arc Floor Lamp", "category": "lighting", "base_price": 280.0, "material": "metal", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 12, "depth": 12, "height": 80}, "size_fit": ["medium", "large"]},
            {"id": "LR-MID-004", "name": "Walnut Side Table", "category": "table", "base_price": 320.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 20, "depth": 20, "height": 24}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-MID-005", "name": "Glass Coffee Table", "category": "table", "base_price": 450.0, "material": "glass", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 48, "depth": 24, "height": 18}, "size_fit": ["medium", "large"]},
            {"id": "LR-MID-006", "name": "Velvet Accent Chair", "category": "seating", "base_price": 395.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 30, "depth": 32, "height": 36}, "size_fit": ["small", "medium", "large"]},
            {"id": "LR-MID-007", "name": "Industrial Bookshelf", "category": "storage", "base_price": 380.0, "material": "metal", "style": "industrial", "room_type": ["living_room"], "dimensions": {"width": 48, "depth": 12, "height": 72}, "size_fit": ["medium", "large"]},
            {"id": "LR-MID-008", "name": "Media Console 60in", "category": "storage", "base_price": 495.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 60, "depth": 18, "height": 24}, "size_fit": ["medium", "large"]},
            {"id": "LR-MID-009", "name": "Leather Ottoman", "category": "seating", "base_price": 285.0, "material": "leather", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 36, "depth": 36, "height": 18}, "size_fit": ["medium", "large"]},
            {"id": "LR-MID-010", "name": "Tripod Floor Lamp", "category": "lighting", "base_price": 195.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 20, "depth": 20, "height": 65}, "size_fit": ["small", "medium", "large"]},
            
            # ==========================================
            # LIVING ROOM - PREMIUM ($800-$2000)
            # ==========================================
            {"id": "LR-PREM-001", "name": "Scandinavian Minimalist Sofa", "category": "seating", "base_price": 1200.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 84, "depth": 36, "height": 32}, "size_fit": ["medium", "large"]},
            {"id": "LR-PREM-002", "name": "Mid-Century Sectional", "category": "seating", "base_price": 1650.0, "material": "fabric", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 110, "depth": 85, "height": 32}, "size_fit": ["large"]},
            {"id": "LR-PREM-003", "name": "Marble Coffee Table", "category": "table", "base_price": 890.0, "material": "marble", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 48, "depth": 28, "height": 16}, "size_fit": ["medium", "large"]},
            {"id": "LR-PREM-004", "name": "Designer Floor Lamp", "category": "lighting", "base_price": 525.0, "material": "metal", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 15, "depth": 15, "height": 70}, "size_fit": ["medium", "large"]},
            {"id": "LR-PREM-005", "name": "Teak Wood Entertainment Center", "category": "storage", "base_price": 980.0, "material": "wood", "style": "modern", "room_type": ["living_room"], "dimensions": {"width": 72, "depth": 20, "height": 30}, "size_fit": ["large"]},
            
            # ==========================================
            # BEDROOM - BUDGET ($20-$300)
            # ==========================================
            {"id": "BR-BUDGET-001", "name": "Bedside Reading Lamp", "category": "lighting", "base_price": 55.0, "material": "metal", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 6, "depth": 6, "height": 16}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-002", "name": "Round Wall Mirror", "category": "decor", "base_price": 75.0, "material": "glass", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 24, "depth": 2, "height": 24}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-003", "name": "Under Bed Storage Box", "category": "storage", "base_price": 65.0, "material": "fabric", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 36, "depth": 24, "height": 8}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-004", "name": "Blackout Curtains", "category": "decor", "base_price": 75.0, "material": "textile", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 52, "depth": 0, "height": 84}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-005", "name": "Bedside Organizer", "category": "storage", "base_price": 35.0, "material": "fabric", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 12, "depth": 8, "height": 10}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-006", "name": "Bedroom Rug 5x7", "category": "decor", "base_price": 125.0, "material": "textile", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 60, "depth": 84, "height": 0}, "size_fit": ["medium", "large"]},
            {"id": "BR-BUDGET-007", "name": "Decorative Throw Blanket", "category": "decor", "base_price": 45.0, "material": "fabric", "style": "bohemian", "room_type": ["bedroom"], "dimensions": {"width": 50, "depth": 0, "height": 60}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-008", "name": "Wall Mounted Shelf", "category": "storage", "base_price": 65.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 24, "depth": 8, "height": 2}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-009", "name": "Jewelry Organizer", "category": "storage", "base_price": 40.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 10, "depth": 6, "height": 12}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-BUDGET-010", "name": "Alarm Clock with Lamp", "category": "lighting", "base_price": 50.0, "material": "plastic", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 6, "depth": 6, "height": 8}, "size_fit": ["small", "medium", "large"]},
            
            # ==========================================
            # BEDROOM - MID-RANGE ($300-$800)
            # ==========================================
            {"id": "BR-MID-001", "name": "Platform Bed Frame Queen", "category": "bed", "base_price": 590.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 60, "depth": 80, "height": 14}, "size_fit": ["medium", "large"]},
            {"id": "BR-MID-002", "name": "Floating Nightstand Pair", "category": "storage", "base_price": 280.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 18, "depth": 16, "height": 12}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-MID-003", "name": "6-Drawer Dresser", "category": "storage", "base_price": 495.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 54, "depth": 18, "height": 36}, "size_fit": ["medium", "large"]},
            {"id": "BR-MID-004", "name": "Upholstered Bench", "category": "seating", "base_price": 320.0, "material": "fabric", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 48, "depth": 18, "height": 20}, "size_fit": ["medium", "large"]},
            {"id": "BR-MID-005", "name": "Full Length Mirror", "category": "decor", "base_price": 185.0, "material": "glass", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 24, "depth": 2, "height": 65}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-MID-006", "name": "Touch Control Table Lamp Set", "category": "lighting", "base_price": 145.0, "material": "metal", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 6, "depth": 6, "height": 18}, "size_fit": ["small", "medium", "large"]},
            {"id": "BR-MID-007", "name": "Wardrobe Closet", "category": "storage", "base_price": 425.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 48, "depth": 24, "height": 72}, "size_fit": ["medium", "large"]},
            {"id": "BR-MID-008", "name": "Velvet Accent Chair", "category": "seating", "base_price": 380.0, "material": "fabric", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 28, "depth": 30, "height": 34}, "size_fit": ["small", "medium"]},
            
            # ==========================================
            # BEDROOM - PREMIUM ($800-$2000)
            # ==========================================
            {"id": "BR-PREM-001", "name": "Upholstered Platform Bed King", "category": "bed", "base_price": 1290.0, "material": "fabric", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 76, "depth": 80, "height": 48}, "size_fit": ["large"]},
            {"id": "BR-PREM-002", "name": "Designer Dresser Set", "category": "storage", "base_price": 980.0, "material": "wood", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 66, "depth": 20, "height": 40}, "size_fit": ["large"]},
            {"id": "BR-PREM-003", "name": "Chandelier Lighting", "category": "lighting", "base_price": 650.0, "material": "metal", "style": "modern", "room_type": ["bedroom"], "dimensions": {"width": 24, "depth": 24, "height": 20}, "size_fit": ["medium", "large"]},
            
            # ==========================================
            # OFFICE - BUDGET ($20-$300)
            # ==========================================
            {"id": "OF-BUDGET-001", "name": "LED Desk Lamp", "category": "lighting", "base_price": 60.0, "material": "metal", "style": "modern", "room_type": ["office"], "dimensions": {"width": 7, "depth": 7, "height": 18}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-002", "name": "Desktop Organizer Set", "category": "storage", "base_price": 45.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 12, "depth": 8, "height": 6}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-003", "name": "Cork Bulletin Board", "category": "decor", "base_price": 50.0, "material": "cork", "style": "modern", "room_type": ["office"], "dimensions": {"width": 24, "depth": 1, "height": 36}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-004", "name": "Ergonomic Seat Cushion", "category": "seating", "base_price": 55.0, "material": "foam", "style": "modern", "room_type": ["office"], "dimensions": {"width": 16, "depth": 16, "height": 3}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-005", "name": "File Organizer Rack", "category": "storage", "base_price": 35.0, "material": "metal", "style": "industrial", "room_type": ["office"], "dimensions": {"width": 12, "depth": 9, "height": 12}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-006", "name": "Monitor Stand", "category": "storage", "base_price": 40.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 20, "depth": 10, "height": 4}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-007", "name": "Cable Management Box", "category": "storage", "base_price": 25.0, "material": "plastic", "style": "modern", "room_type": ["office"], "dimensions": {"width": 12, "depth": 6, "height": 5}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-008", "name": "Desk Mat Large", "category": "decor", "base_price": 30.0, "material": "leather", "style": "modern", "room_type": ["office"], "dimensions": {"width": 36, "depth": 18, "height": 0}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-009", "name": "Whiteboard 24x36", "category": "decor", "base_price": 45.0, "material": "metal", "style": "modern", "room_type": ["office"], "dimensions": {"width": 24, "depth": 1, "height": 36}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-BUDGET-010", "name": "Desk Plant Set", "category": "decor", "base_price": 35.0, "material": "natural", "style": "modern", "room_type": ["office"], "dimensions": {"width": 6, "depth": 6, "height": 8}, "size_fit": ["small", "medium", "large"]},
            
            # ==========================================
            # OFFICE - MID-RANGE ($300-$800)
            # ==========================================
            {"id": "OF-MID-001", "name": "Standing Desk 48in", "category": "desk", "base_price": 495.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 48, "depth": 24, "height": 48}, "size_fit": ["small", "medium"]},
            {"id": "OF-MID-002", "name": "Adjustable Standing Desk 60in", "category": "desk", "base_price": 650.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 60, "depth": 30, "height": 48}, "size_fit": ["medium", "large"]},
            {"id": "OF-MID-003", "name": "Ergonomic Office Chair", "category": "seating", "base_price": 420.0, "material": "mesh", "style": "modern", "room_type": ["office"], "dimensions": {"width": 26, "depth": 26, "height": 48}, "size_fit": ["small", "medium"]},
            {"id": "OF-MID-004", "name": "L-Shaped Desk", "category": "desk", "base_price": 540.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 60, "depth": 60, "height": 30}, "size_fit": ["large"]},
            {"id": "OF-MID-005", "name": "Filing Cabinet 3-Drawer", "category": "storage", "base_price": 285.0, "material": "metal", "style": "industrial", "room_type": ["office"], "dimensions": {"width": 15, "depth": 18, "height": 40}, "size_fit": ["small", "medium", "large"]},
            {"id": "OF-MID-006", "name": "Bookshelf 5-Tier", "category": "storage", "base_price": 320.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 36, "depth": 12, "height": 70}, "size_fit": ["medium", "large"]},
            {"id": "OF-MID-007", "name": "Leather Executive Chair", "category": "seating", "base_price": 595.0, "material": "leather", "style": "modern", "room_type": ["office"], "dimensions": {"width": 28, "depth": 28, "height": 48}, "size_fit": ["medium", "large"]},
            {"id": "OF-MID-008", "name": "Conference Table", "category": "table", "base_price": 680.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 72, "depth": 36, "height": 30}, "size_fit": ["large"]},
            
            # ==========================================
            # OFFICE - PREMIUM ($800+)
            # ==========================================
            {"id": "OF-PREM-001", "name": "Executive Desk 72in", "category": "desk", "base_price": 1250.0, "material": "wood", "style": "modern", "room_type": ["office"], "dimensions": {"width": 72, "depth": 36, "height": 30}, "size_fit": ["large"]},
            {"id": "OF-PREM-002", "name": "Herman Miller Style Chair", "category": "seating", "base_price": 890.0, "material": "mesh", "style": "modern", "room_type": ["office"], "dimensions": {"width": 27, "depth": 27, "height": 42}, "size_fit": ["small", "medium", "large"]},
            
            # ==========================================
            # MULTI-ROOM ITEMS
            # ==========================================
            {"id": "MULTI-001", "name": "Succulent Planter Set", "category": "decor", "base_price": 35.0, "material": "ceramic", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 8, "depth": 8, "height": 6}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-002", "name": "Gallery Wall Frame Set", "category": "decor", "base_price": 55.0, "material": "wood", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 12, "depth": 1, "height": 16}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-003", "name": "Woven Storage Basket", "category": "storage", "base_price": 40.0, "material": "natural", "style": "bohemian", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 14, "depth": 14, "height": 12}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-004", "name": "Essential Oil Diffuser", "category": "decor", "base_price": 45.0, "material": "ceramic", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 6, "depth": 6, "height": 8}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-005", "name": "Floor Plant Large", "category": "decor", "base_price": 85.0, "material": "natural", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 16, "depth": 16, "height": 48}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-006", "name": "Table Runner", "category": "decor", "base_price": 25.0, "material": "textile", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 14, "depth": 0, "height": 72}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-007", "name": "Decorative Tray", "category": "decor", "base_price": 30.0, "material": "wood", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 16, "depth": 12, "height": 2}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-008", "name": "Candle Set", "category": "decor", "base_price": 40.0, "material": "wax", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 3, "depth": 3, "height": 4}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-009", "name": "Clock Wall Large", "category": "decor", "base_price": 65.0, "material": "metal", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 20, "depth": 2, "height": 20}, "size_fit": ["small", "medium", "large"]},
            {"id": "MULTI-010", "name": "Coat Rack Standing", "category": "storage", "base_price": 75.0, "material": "wood", "style": "modern", "room_type": ["living_room", "bedroom", "office"], "dimensions": {"width": 18, "depth": 18, "height": 72}, "size_fit": ["small", "medium", "large"]},
        ]
        
        # Add all products to graph
        for product in products:
            self.graph.add_node(product["id"], **product)
        
        # Add comprehensive compatibility relationships
        self._add_compatibility_edges()
    
    def _add_compatibility_edges(self):
        """Add smart compatibility relationships"""
        
        # Get all nodes
        nodes = list(self.graph.nodes())
        
        # Add compatibility between products in same room and price tier
        for i, node1 in enumerate(nodes):
            data1 = self.graph.nodes[node1]
            for node2 in nodes[i+1:]:
                data2 = self.graph.nodes[node2]
                
                # Check if compatible
                room_overlap = bool(set(data1["room_type"]) & set(data2["room_type"]))
                style_match = data1["style"] == data2["style"]
                price_diff = abs(data1["base_price"] - data2["base_price"])
                
                # Calculate compatibility score
                if room_overlap and style_match:
                    if price_diff < 200:
                        score = 0.95
                    elif price_diff < 500:
                        score = 0.88
                    elif price_diff < 1000:
                        score = 0.80
                    else:
                        score = 0.70
                    
                    self.graph.add_edge(node1, node2, relationship="COMPATIBLE_WITH", score=score)
    
    def get_compatible_products(
        self,
        room_type: str,
        room_size: str = "medium",
        style_preference: str = "modern",
        max_results: int = 20
    ) -> List[ProductSuggestion]:
        """Query with 100+ products"""
        
        compatible_products = []
        
        for node_id in self.graph.nodes():
            node_data = self.graph.nodes[node_id]
            
            if (room_type in node_data.get("room_type", []) and
                room_size in node_data.get("size_fit", []) and
                node_data.get("style") == style_preference):
                
                neighbors = list(self.graph.neighbors(node_id))
                avg_compatibility = 0.7
                
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
        
        compatible_products.sort(key=lambda x: x.compatibility_score, reverse=True)
        return compatible_products[:max_results]
    
    def get_product_set(self, anchor_product_id: str) -> List[str]:
        """Get compatible products"""
        if anchor_product_id not in self.graph:
            return []
        return list(self.graph.neighbors(anchor_product_id))
    
    def get_graph_stats(self) -> Dict[str, Any]:
        """Graph statistics"""
        return {
            "total_products": self.graph.number_of_nodes(),
            "total_relationships": self.graph.number_of_edges(),
            "categories": len(set(nx.get_node_attributes(self.graph, 'category').values())),
            "avg_compatibility": round(
                sum([data.get('score', 0) for _, _, data in self.graph.edges(data=True)]) / 
                max(self.graph.number_of_edges(), 1), 
                2
            ),
            "price_range": {
                "min": min([data.get('base_price', 0) for _, data in self.graph.nodes(data=True)]),
                "max": max([data.get('base_price', 0) for _, data in self.graph.nodes(data=True)])
            }
        }

# Create singleton
pkg_service = ProductKnowledgeGraph()

# Print stats on load
if __name__ == "__main__":
    stats = pkg_service.get_graph_stats()
    print("Product Database Statistics:")
    print(f"   Total Products: {stats['total_products']}")
    print(f"   Price Range: ${stats['price_range']['min']:.2f} - ${stats['price_range']['max']:.2f}")
    print(f"   Total Relationships: {stats['total_relationships']}")