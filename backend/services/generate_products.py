"""
Product Generator Tool
Easy way to add bulk products to your database

Usage:
    python generate_products.py

This will print Python code you can paste into pkg_service.py
"""

# TEMPLATES FOR EASY PRODUCT CREATION

def generate_budget_living_room_items():
    """Generate 20 budget living room products"""
    
    items = [
        ("Decorative Bookends", "decor", 20, "metal"),
        ("Floor Pillow Large", "seating", 45, "fabric"),
        ("Hanging Plant Holder", "decor", 30, "metal"),
        ("Magazine Rack", "storage", 35, "wood"),
        ("Lamp Shade", "lighting", 25, "fabric"),
        ("Throw Blanket Chunky", "decor", 55, "fabric"),
        ("Coasters Set", "decor", 15, "wood"),
        ("Serving Tray", "decor", 40, "wood"),
        ("Picture Ledge Shelf", "storage", 30, "wood"),
        ("Desk Organizer", "storage", 25, "plastic"),
        ("Letter Board", "decor", 20, "wood"),
        ("String Art", "decor", 35, "wood"),
        ("Tissue Box Cover", "decor", 18, "wood"),
        ("Remote Control Holder", "storage", 22, "wood"),
        ("Magazine Basket", "storage", 38, "natural"),
        ("Curtain Rod Set", "decor", 45, "metal"),
        ("Door Stop Decorative", "decor", 15, "fabric"),
        ("Key Holder Wall", "storage", 28, "wood"),
        ("Umbrella Stand", "storage", 42, "metal"),
        ("Shoe Rack 3-Tier", "storage", 50, "metal"),
    ]
    
    products = []
    for i, (name, category, price, material) in enumerate(items, start=100):
        product = f'''{{
            "id": "LR-BUDGET-{i:03d}",
            "name": "{name}",
            "category": "{category}",
            "base_price": {price}.0,
            "material": "{material}",
            "style": "modern",
            "room_type": ["living_room"],
            "dimensions": {{"width": 12, "depth": 12, "height": 12}},
            "size_fit": ["small", "medium", "large"]
        }},'''
        products.append(product)
    
    return "\n".join(products)

def generate_budget_bedroom_items():
    """Generate 20 budget bedroom products"""
    
    items = [
        ("Jewelry Stand", "storage", 28, "wood"),
        ("Bedside Caddy", "storage", 20, "fabric"),
        ("Sleep Mask Set", "decor", 15, "fabric"),
        ("Essential Oil Set", "decor", 35, "glass"),
        ("Alarm Clock Digital", "decor", 25, "plastic"),
        ("Charging Station", "storage", 30, "wood"),
        ("Laundry Hamper", "storage", 45, "fabric"),
        ("Clothes Valet Stand", "storage", 55, "wood"),
        ("Door Mirror", "decor", 40, "glass"),
        ("Bedding Set Queen", "decor", 75, "fabric"),
        ("Pillow Inserts Set", "decor", 35, "fabric"),
        ("Mattress Pad", "decor", 50, "fabric"),
        ("Bed Risers", "storage", 20, "plastic"),
        ("Hangers Velvet Set", "storage", 25, "fabric"),
        ("Closet Organizer", "storage", 40, "fabric"),
        ("Drawer Dividers", "storage", 18, "plastic"),
        ("Shoe Organizer", "storage", 30, "fabric"),
        ("Garment Rack", "storage", 55, "metal"),
        ("Full Length Mirror Stand", "decor", 65, "glass"),
        ("Vanity Mirror LED", "decor", 50, "glass"),
    ]
    
    products = []
    for i, (name, category, price, material) in enumerate(items, start=100):
        product = f'''{{
            "id": "BR-BUDGET-{i:03d}",
            "name": "{name}",
            "category": "{category}",
            "base_price": {price}.0,
            "material": "{material}",
            "style": "modern",
            "room_type": ["bedroom"],
            "dimensions": {{"width": 12, "depth": 12, "height": 12}},
            "size_fit": ["small", "medium", "large"]
        }},'''
        products.append(product)
    
    return "\n".join(products)

def generate_budget_office_items():
    """Generate 20 budget office products"""
    
    items = [
        ("Pen Holder Set", "storage", 15, "wood"),
        ("Mousepad XL", "decor", 20, "fabric"),
        ("Webcam Cover", "decor", 10, "plastic"),
        ("Laptop Stand", "storage", 35, "metal"),
        ("Phone Stand", "storage", 15, "wood"),
        ("Cable Clips", "storage", 10, "plastic"),
        ("Desk Drawer Organizer", "storage", 20, "plastic"),
        ("Paper Tray", "storage", 18, "metal"),
        ("Tape Dispenser", "storage", 12, "metal"),
        ("Stapler Heavy Duty", "storage", 15, "metal"),
        ("Letter Opener", "storage", 10, "metal"),
        ("Calendar Desk", "decor", 15, "paper"),
        ("Sticky Note Holder", "storage", 12, "wood"),
        ("Business Card Holder", "storage", 15, "wood"),
        ("Book Stand", "storage", 25, "wood"),
        ("Magazine File", "storage", 18, "metal"),
        ("Desk Fan", "decor", 30, "plastic"),
        ("Footrest Under Desk", "seating", 40, "foam"),
        ("Lumbar Support", "seating", 35, "foam"),
        ("Wrist Rest Keyboard", "seating", 20, "foam"),
    ]
    
    products = []
    for i, (name, category, price, material) in enumerate(items, start=100):
        product = f'''{{
            "id": "OF-BUDGET-{i:03d}",
            "name": "{name}",
            "category": "{category}",
            "base_price": {price}.0,
            "material": "{material}",
            "style": "modern",
            "room_type": ["office"],
            "dimensions": {{"width": 8, "depth": 8, "height": 8}},
            "size_fit": ["small", "medium", "large"]
        }},'''
        products.append(product)
    
    return "\n".join(products)

def generate_kitchen_items():
    """Generate 20 kitchen/dining products"""
    
    items = [
        ("Bar Stool Modern", "seating", 120, "metal"),
        ("Dining Chair Set 4pc", "seating", 320, "wood"),
        ("Kitchen Cart", "storage", 180, "wood"),
        ("Dining Table 4-Person", "table", 450, "wood"),
        ("Bar Table", "table", 280, "wood"),
        ("Wine Rack Wall", "storage", 45, "metal"),
        ("Fruit Bowl", "decor", 25, "ceramic"),
        ("Utensil Holder", "storage", 20, "ceramic"),
        ("Spice Rack", "storage", 30, "wood"),
        ("Kitchen Rug Runner", "decor", 40, "textile"),
        ("Pendant Light", "lighting", 85, "metal"),
        ("Cabinet Organizer", "storage", 35, "plastic"),
        ("Dish Rack", "storage", 30, "metal"),
        ("Cookbook Stand", "storage", 20, "wood"),
        ("Kitchen Timer", "decor", 15, "plastic"),
        ("Wall Clock Large", "decor", 35, "metal"),
        ("Recipe Box", "storage", 25, "wood"),
        ("Napkin Holder", "decor", 15, "wood"),
        ("Placemats Set", "decor", 30, "textile"),
        ("Table Centerpiece", "decor", 40, "ceramic"),
    ]
    
    products = []
    for i, (name, category, price, material) in enumerate(items, start=1):
        product = f'''{{
            "id": "KI-ALL-{i:03d}",
            "name": "{name}",
            "category": "{category}",
            "base_price": {price}.0,
            "material": "{material}",
            "style": "modern",
            "room_type": ["kitchen"],
            "dimensions": {{"width": 18, "depth": 18, "height": 18}},
            "size_fit": ["small", "medium", "large"]
        }},'''
        products.append(product)
    
    return "\n".join(products)

if __name__ == "__main__":
    print("=" * 60)
    print("PRODUCT GENERATOR - Copy & Paste into pkg_service.py")
    print("=" * 60)
    print()
    
    print("# ========== BUDGET LIVING ROOM (20 items) ==========")
    print(generate_budget_living_room_items())
    print()
    
    print("# ========== BUDGET BEDROOM (20 items) ==========")
    print(generate_budget_bedroom_items())
    print()
    
    print("# ========== BUDGET OFFICE (20 items) ==========")
    print(generate_budget_office_items())
    print()
    
    print("# ========== KITCHEN/DINING (20 items) ==========")
    print(generate_kitchen_items())
    print()
    
    print("=" * 60)
    print(f"TOTAL: 80 new products generated!")
    print("Copy the sections above and paste into the products list")
    print("=" * 60)
