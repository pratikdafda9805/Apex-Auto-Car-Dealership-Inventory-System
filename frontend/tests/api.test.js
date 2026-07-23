import { jest, describe, test, expect, beforeEach } from '@jest/globals';
import { authAPI, vehicleAPI } from '../js/api.js';

global.fetch = jest.fn();

describe('Frontend API Client', () => {
  beforeEach(() => {
    fetch.mockClear();
    localStorage.clear();
  });

  test('authAPI.login sends POST request to /auth/login', async () => {
    const mockResponse = { access_token: 'fake-jwt', user: { name: 'Bob' } };
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => mockResponse
    });

    const result = await authAPI.login('bob@example.com', 'password123');
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/auth/login', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ email: 'bob@example.com', password: 'password123' })
    }));
    expect(result).toEqual(mockResponse);
  });

  test('vehicleAPI.getAll attaches Bearer token header', async () => {
    localStorage.setItem('access_token', 'token-12345');
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => [{ id: '1', make: 'Toyota' }]
    });

    await vehicleAPI.getAll();
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/vehicles', expect.objectContaining({
      headers: expect.objectContaining({
        Authorization: 'Bearer token-12345'
      })
    }));
  });

  test('vehicleAPI.search constructs proper query parameters', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => []
    });

    await vehicleAPI.search({ make: 'Honda', min_price: 20000 });
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/vehicles/search?make=Honda&min_price=20000', expect.anything());
  });

  test('vehicleAPI.purchase sends POST request to /vehicles/{id}/purchase', async () => {
    fetch.mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: async () => ({ message: 'Purchased' })
    });

    await vehicleAPI.purchase('veh-1', 1);
    expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/vehicles/veh-1/purchase', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ quantity: 1 })
    }));
  });
});
