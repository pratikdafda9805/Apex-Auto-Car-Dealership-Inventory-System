// Utility functions for UI notifications, auth checking, and formatting

export function showToast(message, type = 'info') {
  const container = document.getElementById('toast-container');
  if (!container) return;

  const toast = document.createElement('div');
  const bgColors = {
    success: 'bg-emerald-600 text-white',
    error: 'bg-rose-600 text-white',
    warning: 'bg-amber-500 text-slate-900',
    info: 'bg-sky-600 text-white'
  };

  toast.className = `flex items-center space-x-3 px-4 py-3 rounded-lg shadow-xl ${bgColors[type] || bgColors.info} transform transition-all duration-300 translate-y-2 opacity-0 animate-slide-in`;
  toast.innerHTML = `
    <span class="font-medium text-sm">${escapeHtml(message)}</span>
    <button class="ml-auto font-bold text-lg opacity-75 hover:opacity-100" onclick="this.parentElement.remove()">&times;</button>
  `;

  container.appendChild(toast);

  setTimeout(() => {
    toast.classList.remove('translate-y-2', 'opacity-0');
  }, 10);

  setTimeout(() => {
    toast.classList.add('opacity-0');
    setTimeout(() => toast.remove(), 300);
  }, 4000);
}

export function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

export function formatCurrency(amount) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 0
  }).format(amount);
}

export function getUser() {
  const userStr = localStorage.getItem('user');
  if (!userStr) return null;
  try {
    return JSON.parse(userStr);
  } catch {
    return null;
  }
}

export function getToken() {
  return localStorage.getItem('access_token');
}

export function isAuthenticated() {
  return !!getToken();
}

export function isAdmin() {
  const user = getUser();
  return !!(user && user.role === 'admin');
}

export function logout() {
  localStorage.removeItem('access_token');
  localStorage.removeItem('user');
  if (typeof window !== 'undefined' && window.location) {
    window.location.href = 'login.html';
  }
}

export function requireAuth() {
  if (!isAuthenticated() && typeof window !== 'undefined' && window.location) {
    window.location.href = 'login.html';
  }
}

export function requireAdminAuth() {
  if (typeof window !== 'undefined' && window.location) {
    if (!isAuthenticated()) {
      window.location.href = 'login.html';
    } else if (!isAdmin()) {
      window.location.href = 'dashboard.html';
    }
  }
}
