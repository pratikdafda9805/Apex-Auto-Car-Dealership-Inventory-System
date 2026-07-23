// Central API client wrapper for FastAPI backend
const API_BASE_URL = 'http://localhost:8000/api';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('access_token');
  const headers = {
    'Content-Type': 'application/json',
    ...(options.headers || {})
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const config = {
    ...options,
    headers
  };

  try {
    const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

    if (response.status === 401) {
      // Clear token & redirect to login if unauthorized
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      if (!window.location.pathname.endsWith('login.html') && !window.location.pathname.endsWith('register.html')) {
        window.location.href = 'login.html';
      }
    }

    const data = await response.json();

    if (!response.ok) {
      const errorMsg = data.detail || (Array.isArray(data.detail) ? data.detail[0].msg : 'API Request failed');
      throw new Error(errorMsg);
    }

    return data;
  } catch (err) {
    throw err;
  }
}

export const authAPI = {
  register: (name, email, password) =>
    request('/auth/register', {
      method: 'POST',
      body: JSON.stringify({ name, email, password })
    }),

  login: (email, password) =>
    request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password })
    })
};

export const vehicleAPI = {
  getAll: () => request('/vehicles'),

  search: (params) => {
    const query = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null && params[key] !== '') {
        query.append(key, params[key]);
      }
    });
    const queryString = query.toString();
    return request(`/vehicles/search${queryString ? '?' + queryString : ''}`);
  },

  create: (vehicleData) =>
    request('/vehicles', {
      method: 'POST',
      body: JSON.stringify(vehicleData)
    }),

  update: (id, vehicleData) =>
    request(`/vehicles/${id}`, {
      method: 'PUT',
      body: JSON.stringify(vehicleData)
    }),

  delete: (id) =>
    request(`/vehicles/${id}`, {
      method: 'DELETE'
    }),

  purchase: (id, quantity = 1) =>
    request(`/vehicles/${id}/purchase`, {
      method: 'POST',
      body: JSON.stringify({ quantity })
    }),

  restock: (id, quantity) =>
    request(`/vehicles/${id}/restock`, {
      method: 'POST',
      body: JSON.stringify({ quantity })
    })
};
