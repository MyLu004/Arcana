#!/usr/bin/env python3
"""
FULL ORCHESTRATION TEST
Test the complete multi-agent design flow with real Claude API calls

Run this AFTER you've added your Anthropic API key to .env
"""

import sys
sys.path.insert(0, '/home/claude/arcana_backend')

print("\n" + "="*70)
print("🎨 ARCANA - FULL ORCHESTRATION TEST")
print("="*70)
print("\nThis will test the complete multi-agent design pipeline.")
print("Estimated time: 30-60 seconds (multiple Claude API calls)\n")

# Check API key first
try:
    from config import get_settings
    settings = get_settings()
    
    if not settings.ANTHROPIC_API_KEY.startswith("sk-ant"):
        print("❌ ERROR: No valid Anthropic API key found")
        print("\nPlease add your API key to .env:")
        print("ANTHROPIC_API_KEY=sk-ant-api03-YOUR_KEY_HERE\n")
        sys.exit(1)
    
    print(f"✅ API Key configured (starts with: {settings.ANTHROPIC_API_KEY[:15]}...)\n")
    
except Exception as e:
    print(f"❌ Configuration error: {e}\n")
    sys.exit(1)

# Import components
print("Loading backend components...")
try:
    from agents.orchestrator import orchestrator
    from services.pkg_service import pkg_service
    from models import DesignRequest, RoomType
    print("✅ All components loaded\n")
except Exception as e:
    print(f"❌ Import error: {e}\n")
    sys.exit(1)

# Prepare test scenario
print("="*70)
print("TEST SCENARIO: Modern Minimalist Living Room")
print("="*70)
print("\nUser Request:")
print("  Prompt: 'Create a modern, minimalist living room with neutral colors'")
print("  Room: Living Room (medium size)")
print("  Budget: $5,000")
print("  Style: Modern, Minimalist\n")

# Get products from PKG
print("Step 1: Querying Product Knowledge Graph...")
try:
    products = pkg_service.get_compatible_products(
        room_type="living_room",
        room_size="medium",
        style_preference="modern",
        max_results=10
    )
    print(f"✅ Found {len(products)} compatible products\n")
except Exception as e:
    print(f"❌ PKG query failed: {e}\n")
    sys.exit(1)

# Prepare orchestration request
user_request = {
    "prompt": "Create a modern, minimalist living room with neutral colors and clean lines",
    "room_type": "living_room",
    "room_size": "medium",
    "style_preferences": ["modern", "minimalist"],
    "budget_max": 5000.0
}

control_image_url = "https://i.ibb.co/placeholder.png"  # Mock URL

# Run orchestration
print("="*70)
print("RUNNING MULTI-AGENT ORCHESTRATION")
print("="*70)
print("\nThis will coordinate 5 agents:")
print("  1. Lead Orchestrator (Claude Opus 4)")
print("  2. Style Analysis Agent (Claude Sonnet 4)")
print("  3. Product Recommendation Agent (Claude Sonnet 4)")
print("  4. Layout Optimization Agent (Claude Sonnet 4)")
print("  5. Budget Management Agent (Claude Sonnet 4)")
print("\n⏳ Please wait 30-60 seconds...\n")

try:
    result = orchestrator.orchestrate_design(
        user_request=user_request,
        control_image_url=control_image_url,
        available_products=products
    )
    
    print("\n" + "="*70)
    print("ORCHESTRATION COMPLETE!")
    print("="*70)
    
    if result.get("success"):
        print("\n✅ SUCCESS: Design generated successfully\n")
        
        # Display results
        print("RESULTS:")
        print("-" * 70)
        
        # Control params
        if "control_params" in result:
            cp = result["control_params"]
            print(f"\n📸 ControlNet Prompt Preview:")
            print(f"   {cp.get('prompt', 'N/A')[:150]}...")
            print(f"   Scale: {cp.get('scale', 'N/A')}, Steps: {cp.get('steps', 'N/A')}")
        
        # Agent outputs
        if "agent_outputs" in result:
            outputs = result["agent_outputs"]
            
            # Style analysis
            if "style_analysis" in outputs:
                style = outputs["style_analysis"]
                print(f"\n🎨 Style Analysis:")
                print(f"   Primary Style: {style.get('primary_style', 'N/A')}")
                print(f"   Mood: {style.get('mood', 'N/A')}")
                print(f"   Colors: {', '.join(style.get('color_palette', ['N/A'])[:3])}")
            
            # Product recommendations
            if "product_recommendations" in outputs:
                prods = outputs["product_recommendations"]
                selected = prods.get("selected_products", [])
                total_cost = prods.get("total_estimated_cost", 0)
                print(f"\n🛋️  Product Recommendations: {len(selected)} items")
                print(f"   Total Cost: ${total_cost:.2f}")
                for i, prod in enumerate(selected[:3], 1):
                    print(f"   {i}. {prod.get('name', 'N/A')} - ${prod.get('base_price', 0)}")
            
            # Layout optimization
            if "layout_optimization" in outputs:
                layout = outputs["layout_optimization"]
                zones = layout.get("layout_zones", [])
                print(f"\n📐 Layout Planning: {len(zones)} functional zones")
                print(f"   Focal Point: {layout.get('focal_point', 'N/A')}")
            
            # Budget analysis
            if "budget_analysis" in outputs:
                budget = outputs["budget_analysis"]
                total = budget.get("total_cost", 0)
                status = budget.get("budget_status", "unknown")
                print(f"\n💰 Budget Analysis:")
                print(f"   Total: ${total:.2f}")
                print(f"   Status: {status}")
                if "budget_remaining" in budget:
                    print(f"   Remaining: ${budget['budget_remaining']:.2f}")
        
        # Confidence scores
        if "confidence_scores" in result:
            scores = result["confidence_scores"]
            print(f"\n📊 Agent Confidence Scores:")
            for agent, score in scores.items():
                print(f"   {agent.capitalize()}: {score:.2f}")
        
        print("\n" + "="*70)
        print("✅ FULL ORCHESTRATION TEST PASSED")
        print("="*70)
        print("\nYour backend is fully operational!")
        print("All agents coordinated successfully to generate a complete design.\n")
        
        print("Next steps:")
        print("  1. ✅ Backend tested and working")
        print("  2. 🔄 Start the FastAPI server: uvicorn main:app --reload")
        print("  3. 🎨 Connect your frontend")
        print("  4. 🎤 Prepare your demo\n")
        
    else:
        print("\n❌ ORCHESTRATION FAILED")
        print(f"Error: {result.get('error', 'Unknown error')}\n")
        if "partial_results" in result:
            print("Partial results available - some agents may have succeeded")
        sys.exit(1)
        
except Exception as e:
    print(f"\n❌ ORCHESTRATION ERROR: {str(e)}\n")
    import traceback
    print("Full traceback:")
    print(traceback.format_exc())
    sys.exit(1)

print("="*70 + "\n")