/**
 * STEP 6: Cost Breakdown Component
 * Save as: frontend/src/components/CostBreakdown.jsx
 * 
 * Install: npm install lucide-react
 */

import React from 'react';
import { DollarSign, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react';

function CostBreakdown({ budgetData, productData }) {
  if (!budgetData && !productData) {
    return null;
  }

  const totalCost = productData?.total_estimated_cost || 0;
  const budgetMax = budgetData?.budget_max || totalCost;
  const budgetRemaining = budgetData?.budget_remaining ?? (budgetMax - totalCost);
  const budgetStatus = budgetData?.budget_status || 
    (budgetRemaining >= 0 ? 'within_budget' : 'over_budget');
  
  const taxRate = 0.0825; // 8.25%
  const shippingCost = totalCost < 1000 ? 150 : 0;
  const subtotal = totalCost;
  const tax = subtotal * taxRate;
  const grandTotal = subtotal + tax + shippingCost;

  const statusConfig = {
    within_budget: {
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      text: '✅ Within Budget'
    },
    over_budget: {
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      text: '⚠️ Over Budget'
    }
  };

  const status = statusConfig[budgetStatus] || statusConfig.within_budget;
  const StatusIcon = status.icon;

  return (
    <div className="my-6 bg-white rounded-lg shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800 flex items-center gap-2">
          <DollarSign className="w-6 h-6" />
          Cost Breakdown
        </h3>
        
        <div className={`flex items-center gap-2 px-3 py-1 rounded-full ${status.bgColor} border ${status.borderColor}`}>
          <StatusIcon className={`w-4 h-4 ${status.color}`} />
          <span className={`text-sm font-semibold ${status.color}`}>
            {status.text}
          </span>
        </div>
      </div>

      {/* Line Items */}
      <div className="space-y-3 mb-4">
        <div className="flex justify-between text-gray-700">
          <span>Subtotal ({productData?.selected_products?.length || 0} items)</span>
          <span className="font-semibold">${subtotal.toFixed(2)}</span>
        </div>
        
        <div className="flex justify-between text-gray-700">
          <span>Tax (8.25%)</span>
          <span className="font-semibold">${tax.toFixed(2)}</span>
        </div>
        
        <div className="flex justify-between text-gray-700">
          <span>
            Shipping
            {shippingCost === 0 && (
              <span className="ml-2 text-xs text-green-600 font-semibold">FREE</span>
            )}
          </span>
          <span className="font-semibold">${shippingCost.toFixed(2)}</span>
        </div>
        
        <div className="border-t-2 border-gray-200 pt-3 mt-3">
          <div className="flex justify-between text-xl font-bold text-gray-900">
            <span>Total</span>
            <span className="text-blue-600">${grandTotal.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Budget Progress */}
      {budgetMax > 0 && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between mb-2 text-sm">
            <span className="text-gray-600">Budget Used</span>
            <span className="font-semibold text-gray-900">
              ${grandTotal.toFixed(2)} / ${budgetMax.toFixed(2)}
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                budgetRemaining >= 0 ? 'bg-green-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min((grandTotal / budgetMax) * 100, 100)}%` }}
            />
          </div>
          
          {budgetRemaining >= 0 ? (
            <p className="text-sm text-green-600 mt-2 flex items-center gap-1">
              <TrendingUp className="w-4 h-4" />
              ${Math.abs(budgetRemaining).toFixed(2)} remaining in budget
            </p>
          ) : (
            <p className="text-sm text-red-600 mt-2 flex items-center gap-1">
              <AlertCircle className="w-4 h-4" />
              ${Math.abs(budgetRemaining).toFixed(2)} over budget
            </p>
          )}
        </div>
      )}

      {/* Savings Tips */}
      {budgetData?.savings_tips && budgetData.savings_tips.length > 0 && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">💡 Ways to Save:</h4>
          <ul className="space-y-1">
            {budgetData.savings_tips.map((tip, index) => (
              <li key={index} className="text-sm text-blue-800 flex items-start gap-2">
                <span className="text-blue-500">•</span>
                <span>{tip}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default CostBreakdown;