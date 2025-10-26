/**
 * STEP 5: Product Gallery with Images
 * Save as: frontend/src/components/ProductGallery.jsx
 * 
 * Install: npm install lucide-react
 */

import React from 'react';
import { ExternalLink, ShoppingCart, Star } from 'lucide-react';

function ProductGallery({ products }) {
  if (!products || products.length === 0) {
    return null;
  }

  const getPriorityBadge = (priority) => {
    const badges = {
      essential: { color: 'bg-red-100 text-red-800', text: '⭐ Essential' },
      recommended: { color: 'bg-blue-100 text-blue-800', text: '✨ Recommended' },
      optional: { color: 'bg-gray-100 text-gray-800', text: '💫 Optional' },
    };
    return badges[priority] || badges.recommended;
  };

  return (
    <div className="my-6 bg-white rounded-lg shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4">
        🛋️ Recommended Furniture ({products.length} items)
      </h3>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {products.map((product, index) => {
          const badge = getPriorityBadge(product.priority);
          
          return (
            <div 
              key={index}
              className="border border-gray-200 rounded-lg overflow-hidden hover:shadow-xl transition-shadow duration-300 bg-white"
            >
              {/* Product Image */}
              <div className="relative h-48 bg-gray-100">
                <img
                  src={product.image_url || 'https://via.placeholder.com/400x300?text=Product'}
                  alt={product.name}
                  className="w-full h-full object-cover"
                  onError={(e) => {
                    e.target.src = 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&q=80';
                  }}
                />
                
                {/* Priority Badge */}
                <div className="absolute top-2 right-2">
                  <span className={`text-xs font-semibold px-2 py-1 rounded-full ${badge.color}`}>
                    {badge.text}
                  </span>
                </div>
              </div>

              {/* Product Details */}
              <div className="p-4">
                <h4 className="font-bold text-gray-900 mb-1 line-clamp-2">
                  {product.name}
                </h4>
                
                <div className="flex items-center justify-between mb-2">
                  <span className="text-2xl font-bold text-blue-600">
                    ${product.base_price?.toFixed(2)}
                  </span>
                  <span className="text-xs text-gray-500 bg-gray-100 px-2 py-1 rounded">
                    {product.material}
                  </span>
                </div>

                {/* Selection Reason */}
                {product.selection_reason && (
                  <p className="text-sm text-gray-600 mb-3 line-clamp-2">
                    {product.selection_reason}
                  </p>
                )}

                {/* Compatibility Score */}
                {product.compatibility_score && (
                  <div className="flex items-center mb-3">
                    <Star className="w-4 h-4 text-yellow-500 fill-yellow-500 mr-1" />
                    <span className="text-sm text-gray-600">
                      {(product.compatibility_score * 100).toFixed(0)}% match
                    </span>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex gap-2">
                  <a
                    href={product.purchase_url || '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-3 rounded-lg flex items-center justify-center gap-2 transition-colors"
                  >
                    <ShoppingCart className="w-4 h-4" />
                    Buy Now
                  </a>
                  
                  <a
                    href={product.purchase_url || '#'}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-semibold py-2 px-3 rounded-lg flex items-center justify-center transition-colors"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </a>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default ProductGallery;