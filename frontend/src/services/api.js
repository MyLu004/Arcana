// src/services/api.js

const API_BASE_URL = 'http://localhost:8000';

export const api = {
  /**
   * Upload image to backend
   * @param {File} file - Image file to upload
   * @returns {Promise<{url: string}>} - Public URL of uploaded image
   */
  async uploadImage(file) {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload/image`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Upload failed: ${response.status}`);
    }

    return await response.json();
  },

  /**
   * Generate design with multi-agent orchestration
   * @param {string} prompt - User's design prompt
   * @param {string} roomType - Type of room (living_room, bedroom, office, kitchen)
   * @param {string} roomSize - Size of room (small, medium, large)
   * @param {number|null} budgetMax - Maximum budget in USD (null for no limit)
   * @param {string|null} controlImageUrl - Public URL of control image
   * @returns {Promise<Object>} - Design result from backend
   */
  async generateDesign(prompt, roomType = 'living_room', roomSize = 'medium', budgetMax = null, controlImageUrl = null) {
    console.log("API Request:", {
      prompt,
      room_type: roomType,
      room_size: roomSize,
      budget_max: budgetMax, // ← Budget included!
      control_image_url: controlImageUrl
    });

    const requestBody = {
      prompt,
      room_type: roomType,
      room_size: roomSize,
      style_preferences: [],
      budget_max: budgetMax // CRITICAL: Budget sent to backend
    };

    // Add control_image_url if provided
    if (controlImageUrl) {
      requestBody.control_image_url = controlImageUrl;
    }

    const response = await fetch(`${API_BASE_URL}/agent/design/multi`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestBody),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      throw new Error(error.detail || `Generation failed: ${response.status}`);
    }

    const result = await response.json();
    console.log("API Response:", result);
    
    return result;
  },

  /**
   * Get available products from PKG
   * @returns {Promise<Array>} - List of products
   */
  async getProducts() {
    const response = await fetch(`${API_BASE_URL}/products`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch products: ${response.status}`);
    }

    return await response.json();
  },

  /**
   * Health check
   * @returns {Promise<Object>} - Health status
   */
  async healthCheck() {
    const response = await fetch(`${API_BASE_URL}/health`, {
      method: 'GET',
    });

    if (!response.ok) {
      throw new Error(`Health check failed: ${response.status}`);
    }

    return await response.json();
  }
};

export default api;