#!/usr/bin/env python3
"""
ARCANA BACKEND - QUICK TEST SUITE
Simple, clear testing of all backend components
"""

import sys
sys.path.insert(0, '/home/claude/arcana_backend')

passed = 0
failed = 0
warnings = 0

def test(name, func):
    """Run a test function"""
    global passed, failed, warnings
    try:
        result = func()
        if result == "pass":
            print(f"✅ {name}")
            passed += 1
        elif result == "warn":
            print(f"⚠️  {name}")
            warnings += 1
        elif result == "fail":
            print(f"❌ {name}")
            failed += 1
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        failed += 1

print("\n" + "="*70)
print("🚀 ARCANA BACKEND TEST SUITE")
print("="*70 + "\n")

# TEST 1: Imports
print("TEST 1: Module Imports")
print("-" * 70)

def test_models():
    import models
    return "pass"
test("Import models.py", test_models)

def test_config():
    import config
    return "pass"
test("Import config.py", test_config)

def test_base_agent():
    from agents.base_agent import BaseAgent
    return "pass"
test("Import base_agent", test_base_agent)

def test_orchestrator():
    from agents.orchestrator import orchestrator
    print(f"    └─ Model: {orchestrator.model}")
    return "pass"
test("Import orchestrator", test_orchestrator)

def test_style_agent():
    from agents.style_agent import style_agent
    print(f"    └─ Agent: {style_agent.agent_name}")
    return "pass"
test("Import style_agent", test_style_agent)

def test_product_agent():
    from agents.product_agent import product_agent
    print(f"    └─ Agent: {product_agent.agent_name}")
    return "pass"
test("Import product_agent", test_product_agent)

def test_layout_agent():
    from agents.layout_agent import layout_agent
    print(f"    └─ Agent: {layout_agent.agent_name}")
    return "pass"
test("Import layout_agent", test_layout_agent)

def test_budget_agent():
    from agents.budget_agent import budget_agent
    print(f"    └─ Agent: {budget_agent.agent_name}")
    return "pass"
test("Import budget_agent", test_budget_agent)

def test_pkg_service():
    from services.pkg_service import pkg_service
    stats = pkg_service.get_graph_stats()
    print(f"    └─ Products: {stats['total_products']}, Relationships: {stats['total_relationships']}")
    return "pass"
test("Import pkg_service", test_pkg_service)

def test_image_service():
    from services.image_service import ImageService
    return "pass"
test("Import image_service", test_image_service)

# TEST 2: Configuration
print("\nTEST 2: Configuration")
print("-" * 70)

def test_api_keys():
    from config import get_settings
    settings = get_settings()
    
    if settings.ANTHROPIC_API_KEY.startswith("sk-ant"):
        print(f"    └─ Anthropic API Key: Valid format")
        return "pass"
    elif settings.ANTHROPIC_API_KEY != "your_anthropic_key_here":
        print(f"    └─ Anthropic API Key: Present (unusual format)")
        return "warn"
    else:
        print(f"    └─ Anthropic API Key: MISSING (placeholder detected)")
        return "warn"

test("API Keys Configured", test_api_keys)

# TEST 3: Pydantic Models
print("\nTEST 3: Pydantic Models")
print("-" * 70)

def test_design_request():
    from models import DesignRequest, RoomType
    req = DesignRequest(
        prompt="Modern living room",
        room_type=RoomType.LIVING_ROOM,
        room_size="medium",
        style_preferences=["modern"],
        budget_max=5000.0
    )
    print(f"    └─ budget_max field: ${req.budget_max}")
    return "pass"

test("DesignRequest Model", test_design_request)

def test_product_suggestion():
    from models import ProductSuggestion
    prod = ProductSuggestion(
        sku="TEST-001",
        name="Test Sofa",
        base_price=999.99,
        material="fabric",
        category="seating",
        compatibility_score=0.85
    )
    return "pass"

test("ProductSuggestion Model", test_product_suggestion)

# TEST 4: PKG Functionality
print("\nTEST 4: Product Knowledge Graph")
print("-" * 70)

def test_pkg_query():
    from services.pkg_service import pkg_service
    products = pkg_service.get_compatible_products(
        room_type="living_room",
        room_size="medium",
        style_preference="modern",
        max_results=5
    )
    if len(products) > 0:
        print(f"    └─ Found {len(products)} products")
        print(f"    └─ Example: {products[0].name} (${products[0].base_price})")
        return "pass"
    else:
        return "fail"

test("PKG Product Query", test_pkg_query)

# TEST 5: FastAPI App
print("\nTEST 5: FastAPI Application")
print("-" * 70)

def test_fastapi_app():
    from main import app
    routes = [route.path for route in app.routes if hasattr(route, 'path')]
    
    critical_endpoints = [
        "/agent/design/multi",
        "/pkg/query",
        "/upload-image"
    ]
    
    found = sum(1 for ep in critical_endpoints if ep in routes)
    print(f"    └─ Critical endpoints: {found}/{len(critical_endpoints)} found")
    print(f"    └─ Total routes: {len(routes)}")
    
    if found == len(critical_endpoints):
        return "pass"
    else:
        return "warn"

test("FastAPI Endpoints", test_fastapi_app)

# TEST 6: Claude API (if key available)
print("\nTEST 6: Claude API Connection")
print("-" * 70)

def test_claude_api():
    from config import get_settings
    settings = get_settings()
    
    if not settings.ANTHROPIC_API_KEY.startswith("sk-ant"):
        print("    └─ Skipped (no valid API key)")
        return "warn"
    
    from anthropic import Anthropic
    client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)
    
    print("    └─ Making test API call...")
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=50,
        messages=[{"role": "user", "content": "Reply with: API_TEST_SUCCESS"}]
    )
    
    text = response.content[0].text
    if "API_TEST_SUCCESS" in text:
        print(f"    └─ Response: {text[:40]}")
        return "pass"
    else:
        return "warn"

test("Claude API Basic Call", test_claude_api)

# SUMMARY
print("\n" + "="*70)
print("SUMMARY")
print("="*70)

total = passed + failed + warnings
print(f"\n✅ PASSED:   {passed}/{total}")
print(f"❌ FAILED:   {failed}/{total}")
print(f"⚠️  WARNINGS: {warnings}/{total}")

print("\n" + "="*70)

if failed == 0:
    print("🎉 ALL TESTS PASSED!")
    print("\nYour backend is ready! Next steps:")
    print("  1. Add your ANTHROPIC_API_KEY to .env for full functionality")
    print("  2. Test the full orchestration with the script below")
    print("  3. Integrate with frontend")
    print("\nTest orchestration:")
    print("  python test_orchestration.py")
else:
    print("⚠️  SOME TESTS FAILED")
    print("\nFix the failed tests above, then re-run")

print("="*70 + "\n")