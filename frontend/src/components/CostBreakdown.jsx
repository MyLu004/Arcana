/**
 * FIXED: Cost Breakdown Component
 * Properly handles budget display and calculations
 */

import React from 'react';
import { DollarSign, TrendingUp, CheckCircle, AlertCircle } from 'lucide-react';

function CostBreakdown({ budgetData, productData }) {
  if (!budgetData && !productData) {
    return null;
  }

  // FIX: Get values safely with proper fallbacks
  const subtotal = budgetData?.subtotal || productData?.total_estimated_cost || 0;
  const taxRate = 0.0825; // 8.25%
  const tax = budgetData?.tax || (subtotal * taxRate);
  const shipping = budgetData?.shipping ?? (subtotal < 1000 ? 150 : 0);
  const grandTotal = budgetData?.total || (subtotal + tax + shipping);
  
  // CRITICAL FIX: Get budget_max properly, DON'T fall back to totalCost!
  const budgetMax = budgetData?.budget_max;  // ← FIXED: No fallback to totalCost
  
  // Calculate remaining and status
  let budgetRemaining = null;
  let budgetStatus = 'no_budget_set';
  
  if (budgetMax && budgetMax > 0) {
    budgetRemaining = budgetData?.budget_remaining ?? (budgetMax - grandTotal);
    budgetStatus = budgetData?.budget_status || (budgetRemaining >= 0 ? 'within_budget' : 'over_budget');
  }

  const statusConfig = {
    within_budget: {
      icon: CheckCircle,
      color: 'text-green-600',
      bgColor: 'bg-green-50',
      borderColor: 'border-green-200',
      text: 'Within Budget'
    },
    over_budget: {
      icon: AlertCircle,
      color: 'text-red-600',
      bgColor: 'bg-red-50',
      borderColor: 'border-red-200',
      text: 'Over Budget'
    },
    no_budget_set: {
      icon: DollarSign,
      color: 'text-gray-600',
      bgColor: 'bg-gray-50',
      borderColor: 'border-gray-200',
      text: 'No Budget Set'
    }
  };

  const status = statusConfig[budgetStatus] || statusConfig.no_budget_set;
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
            {shipping === 0 && (
              <span className="ml-2 text-xs text-green-600 font-semibold">FREE</span>
            )}
          </span>
          <span className="font-semibold">${shipping.toFixed(2)}</span>
        </div>
        
        <div className="border-t-2 border-gray-200 pt-3 mt-3">
          <div className="flex justify-between text-xl font-bold text-gray-900">
            <span>Total</span>
            <span className="text-blue-600">${grandTotal.toFixed(2)}</span>
          </div>
        </div>
      </div>

      {/* Budget Progress - Only show if budget was set */}
      {budgetMax && budgetMax > 0 && (
        <div className="mt-4 p-4 bg-gray-50 rounded-lg">
          <div className="flex justify-between mb-2 text-sm">
            <span className="text-gray-600">Budget Used</span>
            <span className="font-semibold text-gray-900">
              ${grandTotal.toFixed(2)} / ${budgetMax.toFixed(2)}
            </span>
          </div>
          
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className={`h-3 rounded-full transition-all duration-500 ${
                budgetRemaining >= 0 ? 'bg-green-500' : 'bg-red-500'
              }`}
              style={{ width: `${Math.min((grandTotal / budgetMax) * 100, 100)}%` }}
            />
          </div>
          
          {budgetRemaining !== null && (
            <>
              {budgetRemaining >= 0 ? (
                <p className="text-sm text-green-600 mt-2 flex items-center gap-1">
                  <TrendingUp className="w-4 h-4" />
                  ${Math.abs(budgetRemaining).toFixed(2)} remaining in budget
                </p>
              ) : (
                <p className="text-sm text-red-600 mt-2 flex items-center gap-1 font-semibold">
                  <AlertCircle className="w-4 h-4" />
                  ${Math.abs(budgetRemaining).toFixed(2)} over budget!
                </p>
              )}
            </>
          )}
        </div>
      )}

      {/* Savings Tips */}
      {budgetData?.savings_tips && budgetData.savings_tips.length > 0 && (
        <div className="mt-4 p-4 bg-blue-50 rounded-lg border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">Ways to Save:</h4>
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
      
      {/* Over Budget Warning */}
      {budgetStatus === 'over_budget' && (
        <div className="mt-4 p-4 bg-red-50 rounded-lg border border-red-200">
          <h4 className="font-semibold text-red-900 mb-2">Budget Exceeded</h4>
          <p className="text-sm text-red-800">
            The selected products exceed your budget. Consider removing optional items or choosing more affordable alternatives.
          </p>
        </div>
      )}
    </div>
  );
}

export default CostBreakdown;