// src/services/api.js
import axios from 'axios';

// Create an instance of axios with default configuration
const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Base URL of our FastAPI backend
  timeout: 10000, // Request timeout: 10 seconds
  headers: {
    'Content-Type': 'application/json', // Default content type for JSON data
  }
});

// Function to handle the login API call
export const loginUser = async (email, password) => {
  try {
    // Backend /auth/token expects form data
    const formData = new URLSearchParams();
    formData.append('username', email); // FastAPI's OAuth2 expects 'username'
    formData.append('password', password);

    const response = await apiClient.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded', // Override Content-Type
      }
    });
    return response.data; // { access_token, token_type }
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail || 'Login failed');
    } else {
      throw new Error('Network error or server unavailable');
    }
  }
};

// Request password reset email
export const requestPasswordReset = async (email) => {
  try {
    const response = await apiClient.post('/auth/forgot-password', { email });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail || 'Password reset failed');
    }
    throw new Error('Network error or server unavailable');
  }
};

export const resetPassword = async (token, newPassword) => {
  try {
    const response = await apiClient.post('/auth/reset-password', {
      token,
      new_password: newPassword,
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail || 'Password reset failed');
    }
    throw new Error('Network error or server unavailable');
  }
};

export const registerUser = async ({ fullName, email, institution, password }) => {
  try {
    const response = await apiClient.post('/users/', {
      full_name: fullName,
      email,
      institution,
      password,
    });
    return response.data;
  } catch (error) {
    if (error.response && error.response.data) {
      throw new Error(error.response.data.detail || 'Registration failed');
    }
    throw new Error('Network error or server unavailable');
  }
};

// Function to handle the prediction API call
export const makePrediction = async (predictionData) => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      throw new Error("User not authenticated"); // Error if no token is found
    }

    const response = await apiClient.post('/predict/', predictionData, {
      headers: {
        Authorization: `Bearer ${token}` // Add the Authorization header
      }
    });
    return response.data; // { diagnosis_prediction: "...", confidence_score: ... }
  } catch (error) {
    console.error("Prediction API error:", error.response || error);
    if (error.response && error.response.data) {
       let detail = 'Prediction failed.';
       if (typeof error.response.data.detail === 'string') {
           detail = error.response.data.detail;
       } else if (Array.isArray(error.response.data.detail) && error.response.data.detail.length > 0) {
           detail = error.response.data.detail[0].msg || detail;
       }
       throw new Error(detail);
    } else if (error.message === "User not authenticated") {
       throw error;
    }
    else {
      throw new Error('Network error or prediction service unavailable');
    }
  }
};

// --- NEW FUNCTION ---
// Function to fetch the list of breeds from the API
export const getBreeds = async () => {
  try {
    const token = localStorage.getItem('authToken');
    if (!token) {
      // Depending on API design, this might not need auth, adjust if necessary
      throw new Error("User not authenticated");
    }
    // Fetch a large number of breeds, assuming pagination isn't implemented yet
    const response = await apiClient.get('/breeds/?limit=1000', {
      headers: { Authorization: `Bearer ${token}` }
    });
    return response.data; // Returns a list of breed objects [{id: ..., name: ...}, ...]
  } catch (error) {
    console.error("Get Breeds API error:", error.response || error);
    // Return an empty list or re-throw, depending on how you want to handle failures
    return []; // Return empty list on error for now
  }
};
// --- END NEW FUNCTION ---

export default apiClient;
