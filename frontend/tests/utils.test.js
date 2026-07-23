import { jest, describe, test, expect, beforeEach } from '@jest/globals';
import { escapeHtml, formatCurrency, isAuthenticated, isAdmin } from '../js/utils.js';

describe('Frontend Utility Functions', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  test('escapeHtml prevents XSS injections', () => {
    const raw = '<script>alert("xss")</script> & "quotes"';
    const escaped = escapeHtml(raw);
    expect(escaped.includes('<script>')).toBe(false);
    expect(escaped).toContain('&lt;script&gt;');
    expect(escaped).toContain('&amp;');
  });

  test('formatCurrency formats numbers into USD currency string', () => {
    expect(formatCurrency(28500)).toBe('$28,500');
  });

  test('isAuthenticated returns true when access_token exists', () => {
    expect(isAuthenticated()).toBe(false);
    localStorage.setItem('access_token', 'sample-jwt-token');
    expect(isAuthenticated()).toBe(true);
  });

  test('isAdmin returns true only when user role is admin', () => {
    expect(isAdmin()).toBe(false);
    localStorage.setItem('user', JSON.stringify({ role: 'user' }));
    expect(isAdmin()).toBe(false);
    localStorage.setItem('user', JSON.stringify({ role: 'admin' }));
    expect(isAdmin()).toBe(true);
  });
});
