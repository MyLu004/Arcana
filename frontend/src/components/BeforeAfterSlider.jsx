/**
 * STEP 4: Before/After Image Slider
 * Save as: frontend/src/components/BeforeAfterSlider.jsx
 * 
 * Install: npm install react-compare-image
 */

import React from 'react';
import ReactCompareImage from 'react-compare-image';

function BeforeAfterSlider({ beforeImage, afterImage }) {
  if (!beforeImage || !afterImage) {
    return null;
  }

  return (
    <div className="my-6 bg-white rounded-lg shadow-lg p-4">
      <h3 className="text-lg font-bold text-gray-800 mb-3">
        ✨ Room Transformation
      </h3>
      
      <div className="relative rounded-lg overflow-hidden border-2 border-gray-200">
        <ReactCompareImage
          leftImage={beforeImage}
          rightImage={afterImage}
          sliderLineColor="#3b82f6"
          sliderLineWidth={3}
          handleSize={40}
          hover={true}
        />
      </div>
      
      <div className="flex justify-between mt-3 text-sm text-gray-600">
        <span>← Before</span>
        <span className="text-blue-600 font-semibold">Drag to compare</span>
        <span>After →</span>
      </div>
    </div>
  );
}

export default BeforeAfterSlider;