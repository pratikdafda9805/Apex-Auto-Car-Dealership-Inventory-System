import { vehicleAPI } from './api.js';
import { showToast, formatCurrency, getUser, logout, requireAuth, escapeHtml } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  requireAuth();

  const user = getUser();
  if (user) {
    document.getElementById('user-display').textContent = `Hi, ${user.name} (${user.role.toUpperCase()})`;
    if (user.role === 'admin') {
      const adminLink = document.getElementById('admin-nav-link');
      if (adminLink) adminLink.classList.remove('hidden');
    }
  }

  const logoutBtn = document.getElementById('logout-btn');
  if (logoutBtn) logoutBtn.addEventListener('click', logout);

  loadVehicles();

  // Search & Filter event listeners
  const applyBtn = document.getElementById('apply-filter-btn');
  if (applyBtn) applyBtn.addEventListener('click', handleFilter);

  const resetBtn = document.getElementById('reset-filter-btn');
  if (resetBtn) {
    resetBtn.addEventListener('click', () => {
      document.getElementById('filter-form').reset();
      loadVehicles();
    });
  }

  const filterForm = document.getElementById('filter-form');
  if (filterForm) {
    filterForm.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        e.preventDefault();
        handleFilter();
      }
    });
  }
});

async function loadVehicles(filters = {}) {
  const grid = document.getElementById('vehicles-grid');
  const emptyState = document.getElementById('empty-state');
  const countBadge = document.getElementById('total-count-badge');

  grid.innerHTML = '<div class="col-span-full text-center py-16 text-slate-400 text-sm animate-pulse">Loading vehicle inventory...</div>';

  try {
    let vehicles;
    if (Object.keys(filters).length > 0) {
      vehicles = await vehicleAPI.search(filters);
    } else {
      vehicles = await vehicleAPI.getAll();
    }

    grid.innerHTML = '';

    updateStats(vehicles || []);

    if (!vehicles || vehicles.length === 0) {
      if (emptyState) emptyState.classList.remove('hidden');
      if (countBadge) countBadge.textContent = '0 vehicles found';
      return;
    }

    if (emptyState) emptyState.classList.add('hidden');
    if (countBadge) countBadge.textContent = `${vehicles.length} vehicle(s) found`;

    vehicles.forEach(vehicle => {
      grid.appendChild(createVehicleCard(vehicle));
    });
  } catch (err) {
    showToast(err.message || 'Error loading vehicles', 'error');
    grid.innerHTML = '<div class="col-span-full text-center py-12 text-rose-400 text-sm">Failed to connect to API server.</div>';
  }
}

function updateStats(vehicles) {
  const statTotal = document.getElementById('stat-total');
  const statInStock = document.getElementById('stat-in-stock');
  const statEV = document.getElementById('stat-ev');

  if (!vehicles || vehicles.length === 0) {
    if (statTotal) statTotal.textContent = '0';
    if (statInStock) statInStock.textContent = '0';
    if (statEV) statEV.textContent = '0';
    return;
  }

  const totalModels = vehicles.length;
  const inStockUnits = vehicles.reduce((sum, v) => sum + (v.quantity || 0), 0);
  const evCount = vehicles.filter(v => (v.category || '').toUpperCase() === 'EV').length;

  if (statTotal) statTotal.textContent = totalModels.toString();
  if (statInStock) statInStock.textContent = inStockUnits.toString();
  if (statEV) statEV.textContent = evCount.toString();
}

function handleFilter() {
  const make = document.getElementById('filter-make').value.trim();
  const model = document.getElementById('filter-model').value.trim();
  const category = document.getElementById('filter-category').value;
  const min_price = document.getElementById('filter-min-price').value;
  const max_price = document.getElementById('filter-max-price').value;

  const filters = {};
  if (make) filters.make = make;
  if (model) filters.model = model;
  if (category) filters.category = category;
  if (min_price) filters.min_price = min_price;
  if (max_price) filters.max_price = max_price;

  loadVehicles(filters);
}

function getCategoryBadgeClass(category) {
  const cat = (category || '').toLowerCase();
  if (cat === 'sedan') return 'badge-sedan';
  if (cat === 'suv') return 'badge-suv';
  if (cat === 'truck') return 'badge-truck';
  if (cat === 'sports') return 'badge-sports';
  if (cat === 'ev') return 'badge-ev';
  return 'bg-indigo-500/15 text-indigo-300 border border-indigo-500/30';
}

function createVehicleCard(vehicle) {
  const card = document.createElement('div');
  card.className = 'light-card rounded-3xl p-6 flex flex-col justify-between border border-slate-200 relative overflow-hidden group';

  const isOutOfStock = vehicle.quantity <= 0;

  const stockBadge = isOutOfStock
    ? '<span class="px-3 py-1 rounded-full text-[11px] font-extrabold bg-rose-50 text-rose-700 border border-rose-200 flex items-center space-x-1"><span>🔴</span><span>SOLD OUT</span></span>'
    : `<span class="px-3 py-1 rounded-full text-[11px] font-extrabold bg-emerald-50 text-emerald-700 border border-emerald-200 flex items-center space-x-1"><span>🟢</span><span>${vehicle.quantity} IN STOCK</span></span>`;

  const categoryBadgeClass = getCategoryBadgeClass(vehicle.category);

  card.innerHTML = `
    <div>
      <div class="flex justify-between items-start mb-4">
        <span class="px-3 py-1 rounded-xl text-xs font-extrabold tracking-wide uppercase ${categoryBadgeClass}">${escapeHtml(vehicle.category)}</span>
        ${stockBadge}
      </div>

      <div class="mb-4">
        <h3 class="text-xl font-extrabold text-slate-900 mb-1 group-hover:text-emerald-600 transition duration-200">${escapeHtml(vehicle.make)} ${escapeHtml(vehicle.model)}</h3>
        <p class="text-xs text-slate-500 flex items-center space-x-2 font-medium">
          <span>📅 ${vehicle.year}</span>
          <span>&bull;</span>
          <span>🎨 ${escapeHtml(vehicle.color || 'Standard')}</span>
          <span>&bull;</span>
          <span>🛣️ ${vehicle.mileage !== null ? vehicle.mileage.toLocaleString() + ' mi' : 'New'}</span>
        </p>
      </div>

      <div class="my-4 pt-4 border-t border-slate-100 flex justify-between items-baseline">
        <div>
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 block">Listed MSRP</span>
          <span class="text-2xl font-extrabold text-slate-900 tracking-tight">${formatCurrency(vehicle.price)}</span>
        </div>
      </div>
    </div>

    <button 
      class="purchase-btn w-full mt-4 py-3.5 px-4 rounded-2xl text-xs font-bold tracking-wider uppercase transition duration-200 ${
        isOutOfStock 
          ? 'bg-slate-100 text-slate-400 cursor-not-allowed border border-slate-200' 
          : 'btn-emerald active:scale-[0.98]'
      }"
      ${isOutOfStock ? 'disabled' : ''}
      data-id="${vehicle.id}"
    >
      ${isOutOfStock ? 'Sold Out' : '🛒 Purchase Vehicle'}
    </button>
  `;

  if (!isOutOfStock) {
    const btn = card.querySelector('.purchase-btn');
    btn.addEventListener('click', () => handlePurchase(vehicle));
  }

  return card;
}

async function handlePurchase(vehicle) {
  if (!confirm(`Confirm purchase of ${vehicle.make} ${vehicle.model} for ${formatCurrency(vehicle.price)}?`)) {
    return;
  }

  try {
    const response = await vehicleAPI.purchase(vehicle.id, 1);
    showToast(response.message || `Successfully purchased ${vehicle.make} ${vehicle.model}!`, 'success');
    loadVehicles();
  } catch (err) {
    showToast(err.message || 'Failed to complete purchase', 'error');
  }
}
