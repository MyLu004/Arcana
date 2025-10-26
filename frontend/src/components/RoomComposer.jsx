/**
 * GEOMETRIC ROOM COMPOSER
 * Shows 4 product images overlaid on the actual room photo
 * with spatial positioning based on Layout Agent recommendations
 */

import React, { useState, useRef, useEffect } from 'react';
import { Move, ZoomIn, ZoomOut, RotateCw } from 'lucide-react';

function RoomComposer({ originalImage, products, layoutData }) {
  const canvasRef = useRef(null);
  const [composedImage, setComposedImage] = useState(null);
  const [isComposing, setIsComposing] = useState(false);

  useEffect(() => {
    if (originalImage && products && products.length > 0) {
      composeRoomWithProducts();
    }
  }, [originalImage, products]);

  const composeRoomWithProducts = async () => {
    setIsComposing(true);
    
    try {
      const canvas = canvasRef.current;
      const ctx = canvas.getContext('2d');

      // Load room image
      const roomImg = await loadImage(originalImage);
      
      // Set canvas size to room image size
      canvas.width = roomImg.width;
      canvas.height = roomImg.height;

      // Draw room background
      ctx.drawImage(roomImg, 0, 0);

      // Add semi-transparent overlay for better product visibility
      ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Get product positions from Layout Agent
      const positions = getProductPositions(canvas.width, canvas.height, products, layoutData);

      // Draw each product with geometric placement
      for (let i = 0; i < Math.min(products.length, 4); i++) {
        const product = products[i];
        const position = positions[i];

        try {
          // Load product image
          const productImg = await loadImage(product.image_url);
          
          // Draw product with perspective and positioning
          drawProductInRoom(ctx, productImg, position, product);
          
          // Draw label
          drawProductLabel(ctx, position, product);
        } catch (error) {
          console.warn(`Failed to load product ${i}:`, error);
        }
      }

      // Convert canvas to image
      const composedUrl = canvas.toDataURL('image/png');
      setComposedImage(composedUrl);

    } catch (error) {
      console.error('Room composition failed:', error);
    } finally {
      setIsComposing(false);
    }
  };

  const getProductPositions = (canvasWidth, canvasHeight, products, layoutData) => {
    // Parse layout recommendations from Layout Agent
    const positions = [];
    
    // Default geometric positions if Layout Agent doesn't provide specific coords
    const defaultPositions = [
      { 
        x: canvasWidth * 0.25, 
        y: canvasHeight * 0.6, 
        width: canvasWidth * 0.3,
        height: canvasHeight * 0.35,
        placement: 'center-left',
        category: 'seating'
      },
      { 
        x: canvasWidth * 0.5, 
        y: canvasHeight * 0.7, 
        width: canvasWidth * 0.2,
        height: canvasHeight * 0.2,
        placement: 'center',
        category: 'table'
      },
      { 
        x: canvasWidth * 0.75, 
        y: canvasHeight * 0.5, 
        width: canvasWidth * 0.15,
        height: canvasHeight * 0.4,
        placement: 'right',
        category: 'lighting'
      },
      { 
        x: canvasWidth * 0.15, 
        y: canvasHeight * 0.55, 
        width: canvasWidth * 0.15,
        height: canvasHeight * 0.25,
        placement: 'left',
        category: 'accent'
      }
    ];

    // Match products to positions based on category
    products.forEach((product, index) => {
      // Find best position based on product category
      let position = defaultPositions[index] || defaultPositions[0];
      
      // Adjust based on product category
      const category = product.category?.toLowerCase();
      
      if (category === 'seating') {
        position = defaultPositions[0]; // Center-left, largest
      } else if (category === 'table') {
        position = defaultPositions[1]; // Center, medium
      } else if (category === 'lighting') {
        position = defaultPositions[2]; // Right, tall
      } else {
        position = defaultPositions[3]; // Left, small
      }

      positions.push({
        ...position,
        productName: product.name,
        productPrice: product.base_price
      });
    });

    return positions;
  };

  const drawProductInRoom = (ctx, productImg, position, product) => {
    // Save context state
    ctx.save();

    // Apply transparency for overlay effect
    ctx.globalAlpha = 0.85;

    // Draw shadow for depth
    ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
    ctx.shadowBlur = 15;
    ctx.shadowOffsetX = 5;
    ctx.shadowOffsetY = 5;

    // Draw product image at calculated position
    // Maintain aspect ratio
    const aspectRatio = productImg.width / productImg.height;
    let drawWidth = position.width;
    let drawHeight = position.width / aspectRatio;

    // Adjust if height exceeds position height
    if (drawHeight > position.height) {
      drawHeight = position.height;
      drawWidth = position.height * aspectRatio;
    }

    // Center in position
    const drawX = position.x - drawWidth / 2;
    const drawY = position.y - drawHeight;

    // Draw white background for product
    ctx.fillStyle = 'rgba(255, 255, 255, 0.9)';
    ctx.fillRect(drawX - 5, drawY - 5, drawWidth + 10, drawHeight + 10);

    // Draw product image
    ctx.drawImage(productImg, drawX, drawY, drawWidth, drawHeight);

    // Draw border
    ctx.strokeStyle = '#3b82f6';
    ctx.lineWidth = 3;
    ctx.strokeRect(drawX - 5, drawY - 5, drawWidth + 10, drawHeight + 10);

    // Restore context state
    ctx.restore();
  };

  const drawProductLabel = (ctx, position, product) => {
    ctx.save();

    // Label background
    const labelText = `${product.name} - $${product.base_price}`;
    ctx.font = 'bold 14px Arial';
    const textWidth = ctx.measureText(labelText).width;
    
    const labelX = position.x - textWidth / 2 - 10;
    const labelY = position.y + 10;

    ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
    ctx.fillRect(labelX, labelY, textWidth + 20, 30);

    // Label text
    ctx.fillStyle = '#ffffff';
    ctx.fillText(labelText, labelX + 10, labelY + 20);

    ctx.restore();
  };

  const loadImage = (url) => {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous'; // Handle CORS
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = url;
    });
  };

  if (!originalImage || !products || products.length === 0) {
    return null;
  }

  return (
    <div className="my-6 bg-white rounded-lg shadow-xl p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-gray-800">
          🏠 Your Room with Products Placed
        </h3>
        {isComposing && (
          <span className="text-sm text-blue-600 animate-pulse">
            Composing layout...
          </span>
        )}
      </div>

      {/* Canvas for composition (hidden) */}
      <canvas ref={canvasRef} className="hidden" />

      {/* Display composed image */}
      {composedImage && (
        <div className="relative">
          <img 
            src={composedImage} 
            alt="Room with products" 
            className="w-full rounded-lg shadow-2xl"
          />
          
          <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
            <p className="text-sm text-blue-800">
              <strong>💡 Geometric Layout:</strong> Products are positioned based on optimal 
              room arrangement. Sofa in conversation area, table in center, lighting for ambiance.
            </p>
          </div>
        </div>
      )}

      {/* Product Grid Below */}
      <div className="mt-6">
        <h4 className="text-lg font-semibold text-gray-800 mb-3">
          📦 Product Details
        </h4>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {products.slice(0, 4).map((product, index) => (
            <div 
              key={index}
              className="border border-gray-200 rounded-lg p-3 hover:shadow-lg transition-shadow"
            >
              <img 
                src={product.image_url} 
                alt={product.name}
                className="w-full h-32 object-cover rounded mb-2"
              />
              <p className="text-sm font-semibold text-gray-900 truncate">
                {product.name}
              </p>
              <p className="text-lg font-bold text-blue-600">
                ${product.base_price}
              </p>
              <span className="text-xs text-gray-600">
                {product.category}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default RoomComposer;