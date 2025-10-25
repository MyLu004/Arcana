"""
Budget Management Agent
Tracks costs, suggests alternatives, and optimizes spending
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class BudgetAgent(BaseAgent):
    """
    Specializes in financial analysis and budget optimization
    Tracks total costs, suggests alternatives, flags overages
    """
    
    def __init__(self):
        super().__init__(agent_name="BudgetManager")
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Analyze budget and provide cost optimization recommendations
        
        Context expected:
            - selected_products: List[Dict] - from ProductAgent
            - budget_max: float (optional)
            - available_products: List[Dict] - all PKG products for alternatives
        """
        self.log_activity("Analyzing budget and costs...")
        
        selected_products = context.get("selected_products", [])
        budget_max = context.get("budget_max", None)
        available_products = context.get("available_products", [])
        
        if not selected_products:
            self.log_activity("No products to analyze")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning="No products provided for budget analysis",
                confidence=0.0
            )
        
        # Calculate total cost
        total_cost = sum(p.get("base_price", 0) for p in selected_products)
        
        # Determine budget status
        if budget_max:
            over_budget = total_cost > budget_max
            budget_utilization = (total_cost / budget_max) * 100
        else:
            over_budget = False
            budget_utilization = None
        
        # Format products with costs
        products_breakdown = "\n".join([
            f"- {p.get('name', 'Unknown')}: ${p.get('base_price', 0):.2f} "
            f"({p.get('priority', 'recommended')} priority)"
            for p in selected_products
        ])
        
        system_prompt = """You are a financial advisor specializing in interior design budgets.

Your task is to analyze spending and provide recommendations:
1. Identify potential cost savings without compromising design quality
2. Suggest alternative products if over budget
3. Prioritize essential vs. optional items
4. Calculate value-for-money ratios
5. Recommend budget allocation strategies

Respond ONLY with valid JSON in this exact format:
{
    "total_cost": 5000.50,
    "budget_status": "within_budget|over_budget|no_budget_set",
    "cost_breakdown": {
        "essential": 3000.00,
        "recommended": 1500.00,
        "optional": 500.50
    },
    "savings_opportunities": [
        {
            "item": "product name",
            "current_cost": 1000.00,
            "suggested_alternative": "alternative name",
            "potential_savings": 200.00
        }
    ],
    "recommendations": "Budget optimization advice",
    "value_score": 0.85
}"""

        budget_context = f"Budget Limit: ${budget_max}" if budget_max else "Budget: Flexible"
        
        user_message = f"""Analyze this design budget:

{budget_context}
Total Current Cost: ${total_cost:.2f}

Selected Products:
{products_breakdown}

Provide budget analysis and optimization recommendations."""

        try:
            response_text = self._call_claude(system_prompt, user_message, temperature=0.3)
            
            # Parse JSON response
            cleaned_response = response_text.strip()
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response.split("```json")[1].split("```")[0].strip()
            elif cleaned_response.startswith("```"):
                cleaned_response = cleaned_response.split("```")[1].split("```")[0].strip()
            
            budget_data = json.loads(cleaned_response)
            
            # Add calculated fields
            budget_data["total_cost"] = total_cost
            budget_data["over_budget"] = over_budget
            if budget_max:
                budget_data["budget_remaining"] = budget_max - total_cost
                budget_data["budget_utilization_percent"] = budget_utilization
            
            status = "OK" if not over_budget else "NOPE"
            self.log_activity(f"{status} Budget analysis complete: ${total_cost:.2f}")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=budget_data,
                reasoning=budget_data.get("recommendations", "Budget analyzed and optimized"),
                confidence=budget_data.get("value_score", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using basic budget summary")
            # Fallback with simple budget analysis
            budget_data = {
                "total_cost": total_cost,
                "budget_status": "over_budget" if over_budget else "within_budget" if budget_max else "no_budget_set",
                "cost_breakdown": {
                    "essential": total_cost * 0.6,
                    "recommended": total_cost * 0.3,
                    "optional": total_cost * 0.1
                },
                "savings_opportunities": [],
                "recommendations": "Budget tracking active. Consider prioritizing essential items if over budget.",
                "value_score": 0.75,
                "over_budget": over_budget
            }
            
            if budget_max:
                budget_data["budget_remaining"] = budget_max - total_cost
                budget_data["budget_utilization_percent"] = budget_utilization
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=budget_data,
                reasoning="Basic budget analysis applied due to parsing error",
                confidence=0.75
            )
        
        except Exception as e:
            self.log_activity(f"Budget analysis failed: {str(e)}")
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning=f"Error: {str(e)}",
                confidence=0.0
            )


# Create singleton
budget_agent = BudgetAgent()