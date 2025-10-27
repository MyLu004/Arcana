const API_BASE_URL = 'http://localhost:8000';

class ArcanaAPI {

  // helper: safely parse the JSON 
  async _parseJsonSafe(response) {
    const ct = response.headers.get('content-type') || '';
    if (!ct.includes('application/json')) {
      const txt = await response.text();
      throw new Error(`Expected JSON but got ${ct || 'no content-type'}\nBody:\n${txt}`);
    }
    return response.json();
  }


  /**
   * Generate design using multi-agent orchestration
   * 🔥 FIXED: Added logging for debugging
   */
  async generateDesign(userPrompt, roomType = 'living_room', roomSize = 'medium', budget = null, controlImageUrl = null) {
    try {
      console.log("📤 API generateDesign called with:", {
        prompt: userPrompt,
        room_type: roomType,
        room_size: roomSize,
        budget_max: budget,  // ← Budget is already here!
        control_image_url: controlImageUrl
      });

      const response = await fetch(`${API_BASE_URL}/agent/design/multi`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: userPrompt,
          room_type: roomType,
          room_size: roomSize,
          style_preferences: ['modern', 'minimalist'],
          budget_max: budget,  // ✅ Your code already has this!
          // optionally include a control image URL (from upload)
          ...(controlImageUrl ? { control_image_url: controlImageUrl } : {})
        })
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || `Design generation failed: ${response.status}`);
      }

      const result = await this._parseJsonSafe(response);
      console.log("📥 API response received:", result);
      
      return result;
    } catch (error) {
      console.error('❌ API Error:', error);
      throw error;
    }
  }

  /**
   * Upload image for ControlNet
   */
  async uploadImage(file) {
    try {
      console.log("📤 Uploading image:", file.name, file.size, "bytes");
      
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch(`${API_BASE_URL}/upload-image`, {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const error = await response.json().catch(() => ({}));
        throw new Error(error.detail || 'Image upload failed');
      }

      const result = await response.json();
      console.log("📥 Image uploaded:", result);
      
      return result;
    } catch (error) {
      console.error('❌ Upload Error:', error);
      throw error;
    }
  }

  /**
   * Query products from PKG
   */
  async queryProducts(roomType, roomSize) {
    try {
      const response = await fetch(`${API_BASE_URL}/pkg/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          prompt: 'Query products',
          room_type: roomType,
          room_size: roomSize,
          style_preferences: []
        })
      });

      if (!response.ok) {
        throw new Error('Product query failed');
      }

      return await response.json();
    } catch (error) {
      console.error('Query Error:', error);
      throw error;
    }
  }

  /**
   * Health check
   */
  async healthCheck() {
    try {
      const response = await fetch(`${API_BASE_URL}/health`);
      return await response.json();
    } catch (error) {
      console.error('Health check failed:', error);
      return { status: 'offline' };
    }
  }
}

// Export singleton instance
export const api = new ArcanaAPI();