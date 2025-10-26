"""
Budget Management Agent - FIXED
Ensures budget_max is included in output data
"""
from typing import Dict, Any, List
import json

from agents.base_agent import BaseAgent, AgentResponse


class BudgetAgent(BaseAgent):
    """
    Specializes in financial analysis and budget optimization
    Tracks total costs, suggests alternatives, and optimizes spending
    """
    
    def __init__(self):
        super().__init__(agent_name="BudgetManager")
    def _calculate_budget_confidence(self, budget_data: Dict) -> float:
        """Calculate confidence based on budget analysis quality"""
        confidence = 0.5  # Base confidence - start lower
        
        # No data = low confidence
        if not budget_data:
            return 0.1
            
        # Budget status increases confidence
        status = budget_data.get('budget_status')
        if status == 'within_budget':
            confidence += 0.2
        elif status == 'over_budget':
            confidence += 0.1  # Still some confidence as we know the status
        
        # Having a budget max increases confidence
        if budget_data.get('budget_max'):
            confidence += 0.1
            
            # Budget utilization affects confidence
            if budget_data.get('subtotal'):
                usage = (budget_data.get('subtotal', 0) / budget_data['budget_max']) * 100
                if 80 <= usage <= 95:  # Optimal utilization
                    confidence += 0.1
                elif 60 <= usage <= 100:  # Reasonable utilization
                    confidence += 0.05
        
        # Savings tips indicate deeper analysis
        if budget_data.get('savings_tips'):
            confidence += 0.1
            
        # Cost breakdown indicates detailed analysis
        if budget_data.get('cost_breakdown'):
            confidence += 0.1
            
        # Savings opportunities show thorough analysis
        if budget_data.get('savings_opportunities'):
            confidence += 0.1
        
        return min(confidence, 1.0)  # Cap at 1.0
        
    def process(self, context: Dict[str, Any]) -> AgentResponse:
        """
        Analyze budget and provide cost optimization recommendations
        """
        self.log_activity("Analyzing budget and costs...")
        
        selected_products = context.get("selected_products", [])
        budget_max = context.get("budget_max", None)
        available_products = context.get("available_products", [])
        
        if not selected_products:
            self.log_activity("No products to analyze")
            # Create empty budget data for confidence calculation
            empty_budget_data = {
                "budget_status": "no_budget_set",
                "subtotal": 0,
                "budget_max": budget_max
            }
            return AgentResponse(
                agent_name=self.agent_name,
                success=False,
                data={},
                reasoning="No products provided for budget analysis",
                confidence=self._calculate_budget_confidence(empty_budget_data)
            )
        
        # Calculate costs with tax and shipping
        TAX_RATE = 0.0825  # 8.25%
        subtotal = sum(p.get("base_price", 0) for p in selected_products)
        tax = subtotal * TAX_RATE
        shipping = 0 if subtotal >= 1000 else 150
        total_cost = subtotal + tax + shipping
        
        # Determine budget status
        if budget_max:
            over_budget = total_cost > budget_max
            budget_remaining = budget_max - total_cost
            budget_utilization = (total_cost / budget_max) * 100
            budget_status = "over_budget" if over_budget else "within_budget"
        else:
            over_budget = False
            budget_remaining = None
            budget_utilization = None
            budget_status = "no_budget_set"
        
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
    "value_score": 0.85,
    "savings_tips": ["tip 1", "tip 2"]
}"""

        budget_context = f"Budget Limit: ${budget_max:.2f}" if budget_max else "Budget: Flexible"
        budget_alert = ""
        if over_budget:
            budget_alert = f"\nOVER BUDGET by ${abs(budget_remaining):.2f}! Suggest alternatives."
        
        user_message = f"""Analyze this design budget:

{budget_context}
Subtotal: ${subtotal:.2f}
Tax: ${tax:.2f}
Shipping: ${shipping:.2f}
Total Cost: ${total_cost:.2f}
{budget_alert}

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
            
            # FIX: Always include these calculated fields
            budget_data["subtotal"] = subtotal
            budget_data["tax"] = tax
            budget_data["shipping"] = shipping
            budget_data["total"] = total_cost
            budget_data["budget_max"] = budget_max  # ← CRITICAL: Include budget_max!
            budget_data["budget_status"] = budget_status
            budget_data["over_budget"] = over_budget
            
            if budget_max:
                budget_data["budget_remaining"] = budget_remaining
                budget_data["budget_utilization_percent"] = budget_utilization
            
            status = "OK" if not over_budget else "OVER BUDGET"
            self.log_activity(f"{status} Budget analysis: ${total_cost:.2f} / ${budget_max:.2f if budget_max else 'unlimited'}")
            
            return AgentResponse(
                agent_name=self.agent_name,
                success=True,
                data=budget_data,
                reasoning=budget_data.get("recommendations", "Budget analyzed and optimized"),
                confidence=budget_data.get("value_score", 0.85)
            )
            
        except json.JSONDecodeError as e:
            self.log_activity(f"JSON parsing failed, using basic budget summary")
            # Fallback with all critical fields
            budget_data = {
                "subtotal": subtotal,
                "tax": tax,
                "shipping": shipping,
                "total": total_cost,
                "budget_max": budget_max,  # ← CRITICAL: Include in fallback too!
                "budget_status": budget_status,
                "over_budget": over_budget,
                "cost_breakdown": {
                    "essential": subtotal * 0.6,
                    "recommended": subtotal * 0.3,
                    "optional": subtotal * 0.1
                },
                "savings_opportunities": [],
                "recommendations": "Budget tracking active. Consider prioritizing essential items if over budget.",
                "value_score": 0.75,
                "savings_tips": []
            }
            
            if budget_max:
                budget_data["budget_remaining"] = budget_remaining
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