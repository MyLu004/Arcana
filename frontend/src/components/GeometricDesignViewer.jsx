/**
 * COMPLETE GEOMETRIC VISUALIZATION SYSTEM
 * Combines: Before/After + Product Placement + Product Gallery
 */

import React, { useState } from 'react';
import { Layers, Grid, Package } from 'lucide-react';

function GeometricDesignViewer({ designData }) {
  const [viewMode, setViewMode] = useState('composed'); // 'composed', 'comparison', 'products'
  
  const { agent_outputs, room_images } = designData;
  const products = agent_outputs?.product_recommendations?.selected_products || [];
  const layoutData = agent_outputs?.layout_optimization || {};
  const originalImage = room_images?.original;

  if (!originalImage || products.length === 0) {
    return null;
  }

  return (
    <div className="my-6 bg-white rounded-lg shadow-xl p-6">
      
      {/* View Mode Selector */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-2xl font-bold text-gray-800">
          🎨 Your Redesigned Space
        </h3>
        
        <div className="flex gap-2">
          <button
            onClick={() => setViewMode('composed')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${
              viewMode === 'composed'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Layers className="w-4 h-4" />
            Composed View
          </button>
          
          <button
            onClick={() => setViewMode('comparison')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${
              viewMode === 'comparison'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Grid className="w-4 h-4" />
            Before/After
          </button>
          
          <button
            onClick={() => setViewMode('products')}
            className={`flex items-center gap-2 px-4 py-2 rounded-lg font-semibold transition-all ${
              viewMode === 'products'
                ? 'bg-blue-600 text-white shadow-lg'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            <Package className="w-4 h-4" />
            Products
          </button>
        </div>
      </div>

      {/* Composed View: Room + Products Overlaid */}
      {viewMode === 'composed' && (
        <ComposedRoomView 
          originalImage={originalImage}
          products={products.slice(0, 4)}
          layoutData={layoutData}
        />
      )}

      {/* Comparison View: Side-by-Side or Slider */}
      {viewMode === 'comparison' && (
        <ComparisonView 
          originalImage={originalImage}
          products={products.slice(0, 4)}
          layoutData={layoutData}
        />
      )}

      {/* Products View: Gallery Grid */}
      {viewMode === 'products' && (
        <ProductsGridView products={products} />
      )}

    </div>
  );
}

// ============================================================
// COMPOSED VIEW: Room with products overlaid geometrically
// ============================================================
function ComposedRoomView({ originalImage, products, layoutData }) {
  return (
    <div className="space-y-4">
      
      {/* Main Composed Image */}
      <div className="relative bg-gray-100 rounded-xl overflow-hidden shadow-2xl">
        <img 
          src={originalImage} 
          alt="Your room"
          className="w-full opacity-90"
        />
        
        {/* Overlay products with geometric positioning */}
        {products.map((product, index) => {
          const placement = layoutData?.product_placements?.[index];
          
          // Get position (default if not provided)
          const position = placement?.position || getDefaultPosition(index, product.category);
          
          return (
            <ProductOverlay
              key={index}
              product={product}
              position={position}
              index={index}
            />
          );
        })}
      </div>

      {/* Geometric Layout Info */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {products.map((product, index) => (
          <div 
            key={index}
            className="flex items-center gap-2 p-3 bg-gray-50 rounded-lg border border-gray-200"
          >
            <div className={`w-3 h-3 rounded-full ${getColorClass(index)}`}></div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-semibold text-gray-900 truncate">
                {product.name}
              </p>
              <p className="text-xs text-gray-600">
                ${product.base_price}
              </p>
            </div>
          </div>
        ))}
      </div>

      {/* Layout Description */}
      {layoutData?.layout_reasoning && (
        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
          <p className="text-sm text-blue-800">
            <strong>📐 Layout Strategy:</strong> {layoutData.layout_reasoning}
          </p>
        </div>
      )}
    </div>
  );
}

// Product overlay component with positioning
function ProductOverlay({ product, position, index }) {
  const colorClass = getColorClass(index);
  
  return (
    <div
      className="absolute"
      style={{
        left: `${position.x_percent}%`,
        top: `${position.y_percent}%`,
        width: `${position.width_percent}%`,
        height: `${position.height_percent}%`,
        transform: 'translate(-50%, -50%)',
      }}
    >
      {/* Product image container */}
      <div className="relative w-full h-full group">
        
        {/* Product image */}
        <img
          src={product.image_url}
          alt={product.name}
          className="w-full h-full object-contain drop-shadow-2xl rounded-lg bg-white/90 border-4 border-blue-500 group-hover:scale-105 transition-transform duration-300"
        />
        
        {/* Position indicator dot */}
        <div className={`absolute -top-2 -left-2 w-6 h-6 ${colorClass} rounded-full border-2 border-white shadow-lg flex items-center justify-center text-white text-xs font-bold`}>
          {index + 1}
        </div>
        
        {/* Hover label */}
        <div className="absolute bottom-0 left-0 right-0 bg-black/80 text-white p-2 rounded-b-lg opacity-0 group-hover:opacity-100 transition-opacity">
          <p className="text-xs font-semibold truncate">{product.name}</p>
          <p className="text-xs">${product.base_price}</p>
        </div>
      </div>
    </div>
  );
}

// ============================================================
// COMPARISON VIEW: Before vs After
// ============================================================
function ComparisonView({ originalImage, products, layoutData }) {
  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        
        {/* Before */}
        <div className="space-y-2">
          <h4 className="text-sm font-bold text-gray-700 text-center">
            BEFORE: Your Original Room
          </h4>
          <div className="relative rounded-lg overflow-hidden shadow-xl border-4 border-gray-300">
            <img 
              src={originalImage} 
              alt="Before"
              className="w-full"
            />
          </div>
        </div>

        {/* After */}
        <div className="space-y-2">
          <h4 className="text-sm font-bold text-gray-700 text-center">
            AFTER: With Your New Furniture
          </h4>
          <div className="relative rounded-lg overflow-hidden shadow-xl border-4 border-blue-500">
            <img 
              src={originalImage} 
              alt="After"
              className="w-full opacity-90"
            />
            
            {/* Overlay products */}
            {products.map((product, index) => {
              const placement = layoutData?.product_placements?.[index];
              const position = placement?.position || getDefaultPosition(index, product.category);
              
              return (
                <ProductOverlay
                  key={index}
                  product={product}
                  position={position}
                  index={index}
                />
              );
            })}
          </div>
        </div>
      </div>

      <div className="p-4 bg-green-50 rounded-lg border border-green-200">
        <p className="text-sm text-green-800 text-center">
          <strong>✨ Transformation:</strong> See how your space looks with the recommended furniture geometrically placed!
        </p>
      </div>
    </div>
  );
}

// ============================================================
// PRODUCTS GRID VIEW: Detailed product information
// ============================================================
function ProductsGridView({ products }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {products.map((product, index) => (
        <div 
          key={index}
          className="border-2 border-gray-200 rounded-lg overflow-hidden hover:shadow-xl hover:border-blue-500 transition-all group"
        >
          <div className="relative">
            <img 
              src={product.image_url} 
              alt={product.name}
              className="w-full h-48 object-cover"
            />
            <div className={`absolute top-2 right-2 w-8 h-8 ${getColorClass(index)} rounded-full border-2 border-white shadow-lg flex items-center justify-center text-white text-sm font-bold`}>
              {index + 1}
            </div>
          </div>
          
          <div className="p-4">
            <h5 className="font-bold text-gray-900 text-sm mb-1 line-clamp-2">
              {product.name}
            </h5>
            <p className="text-xl font-bold text-blue-600 mb-2">
              ${product.base_price}
            </p>
            <div className="flex items-center justify-between text-xs">
              <span className="text-gray-600 capitalize">{product.category}</span>
              <span className="text-gray-500">{product.material}</span>
            </div>
            
            {product.selection_reason && (
              <p className="mt-2 text-xs text-gray-600 line-clamp-2">
                {product.selection_reason}
              </p>
            )}
            
            <a
              href={product.purchase_url || '#'}
              target="_blank"
              rel="noopener noreferrer"
              className="mt-3 block w-full bg-blue-600 hover:bg-blue-700 text-white text-sm font-semibold py-2 px-3 rounded-lg text-center transition-colors"
            >
              Buy Now
            </a>
          </div>
        </div>
      ))}
    </div>
  );
}

// Helper functions
function getDefaultPosition(index, category) {
  const positions = {
    0: { x_percent: 25, y_percent: 60, width_percent: 30, height_percent: 35 },
    1: { x_percent: 50, y_percent: 70, width_percent: 20, height_percent: 20 },
    2: { x_percent: 75, y_percent: 50, width_percent: 15, height_percent: 40 },
    3: { x_percent: 15, y_percent: 55, width_percent: 15, height_percent: 25 },
  };
  
  return positions[index] || positions[0];
}

function getColorClass(index) {
  const colors = [
    'bg-blue-500',
    'bg-green-500',
    'bg-purple-500',
    'bg-orange-500'
  ];
  return colors[index] || 'bg-gray-500';
}

export default GeometricDesignViewer;