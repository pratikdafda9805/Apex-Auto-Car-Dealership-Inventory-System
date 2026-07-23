import { vehicleAPI } from './api.js';
import { showToast, formatCurrency, logout, requireAdminAuth, escapeHtml } from './utils.js';

let vehiclesList = [];

document.addEventListener('DOMContentLoaded', () => {
  requireAdminAuth();

  document.getElementById('logout-btn').addEventListener('click', logout);

  loadAdminVehicles();

  // Modal event listeners
  const vehicleModal = document.getElementById('vehicle-modal');
  const restockModal = document.getElementById('restock-modal');

  document.getElementById('open-add-modal-btn').addEventListener('click', () => openAddModal());
  document.getElementById('close-modal-btn').addEventListener('click', () => vehicleModal.classList.add('hidden'));
  document.getElementById('cancel-modal-btn').addEventListener('click', () => vehicleModal.classList.add('hidden'));
  document.getElementById('close-restock-btn').addEventListener('click', () => restockModal.classList.add('hidden'));

  document.getElementById('vehicle-form').addEventListener('submit', handleSaveVehicle);
  document.getElementById('restock-form').addEventListener('submit', handleRestockSubmit);
});

async function loadAdminVehicles() {
  const tbody = document.getElementById('admin-table-body');
  tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-slate-400">Loading inventory...</td></tr>';

  try {
    vehiclesList = await vehicleAPI.getAll();
    renderTable(vehiclesList);
  } catch (err) {
    showToast(err.message || 'Error loading vehicles for admin', 'error');
    tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-rose-400">Failed to load inventory.</td></tr>';
  }
}

function renderTable(vehicles) {
  const tbody = document.getElementById('admin-table-body');
  tbody.innerHTML = '';

  if (!vehicles || vehicles.length === 0) {
    tbody.innerHTML = '<tr><td colspan="7" class="text-center py-8 text-slate-500">No vehicles in inventory. Click "Add New Vehicle" above.</td></tr>';
    return;
  }

  vehicles.forEach(v => {
    const tr = document.createElement('tr');
    tr.className = 'hover:bg-emerald-50/40 transition duration-150 border-b border-slate-100';

    const isLowStock = v.quantity <= 2;

    const cat = (v.category || '').toLowerCase();
    let badgeClass = 'bg-slate-100 text-slate-700 border border-slate-200';
    if (cat === 'sedan') badgeClass = 'badge-sedan';
    if (cat === 'suv') badgeClass = 'badge-suv';
    if (cat === 'truck') badgeClass = 'badge-truck';
    if (cat === 'sports') badgeClass = 'badge-sports';
    if (cat === 'ev') badgeClass = 'badge-ev';

    tr.innerHTML = `
      <td class="p-4 pl-6 font-extrabold text-slate-900">${escapeHtml(v.make)} ${escapeHtml(v.model)}</td>
      <td class="p-4"><span class="px-2.5 py-1 rounded-xl text-xs font-extrabold uppercase tracking-wider ${badgeClass}">${escapeHtml(v.category)}</span></td>
      <td class="p-4 text-slate-600 font-bold">${v.year}</td>
      <td class="p-4 font-extrabold text-slate-900">${formatCurrency(v.price)}</td>
      <td class="p-4 font-extrabold ${isLowStock ? 'text-rose-600' : 'text-emerald-600'}">${v.quantity} units ${isLowStock ? '⚠️' : ''}</td>
      <td class="p-4 text-slate-500 font-medium">${escapeHtml(v.color || 'N/A')} &bull; ${v.mileage !== null ? v.mileage.toLocaleString() + ' mi' : 'New'}</td>
      <td class="p-4 pr-6 text-right space-x-2">
        <button class="restock-btn px-3 py-1.5 text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 rounded-xl hover:bg-emerald-100 transition shadow-xs" data-id="${v.id}">Restock</button>
        <button class="edit-btn px-3 py-1.5 text-xs font-bold bg-slate-100 text-slate-700 border border-slate-200 rounded-xl hover:bg-slate-200 transition shadow-xs" data-id="${v.id}">Edit</button>
        <button class="delete-btn px-3 py-1.5 text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 rounded-xl hover:bg-rose-100 transition shadow-xs" data-id="${v.id}">Delete</button>
      </td>
    `;

    tr.querySelector('.restock-btn').addEventListener('click', () => openRestockModal(v));
    tr.querySelector('.edit-btn').addEventListener('click', () => openEditModal(v));
    tr.querySelector('.delete-btn').addEventListener('click', () => handleDelete(v));

    tbody.appendChild(tr);
  });
}

function openAddModal() {
  document.getElementById('modal-title').textContent = 'Add New Vehicle';
  document.getElementById('vehicle-form').reset();
  document.getElementById('vehicle-id').value = '';
  document.getElementById('vehicle-modal').classList.remove('hidden');
}

function openEditModal(vehicle) {
  document.getElementById('modal-title').textContent = `Edit ${vehicle.make} ${vehicle.model}`;
  document.getElementById('vehicle-id').value = vehicle.id;
  document.getElementById('form-make').value = vehicle.make;
  document.getElementById('form-model').value = vehicle.model;
  document.getElementById('form-year').value = vehicle.year;
  document.getElementById('form-category').value = vehicle.category;
  document.getElementById('form-price').value = vehicle.price;
  document.getElementById('form-quantity').value = vehicle.quantity;
  document.getElementById('form-color').value = vehicle.color || '';
  document.getElementById('form-mileage').value = vehicle.mileage !== null ? vehicle.mileage : '';
  document.getElementById('vehicle-modal').classList.remove('hidden');
}

function openRestockModal(vehicle) {
  document.getElementById('restock-vehicle-id').value = vehicle.id;
  document.getElementById('restock-vehicle-info').textContent = `Current Stock for ${vehicle.make} ${vehicle.model}: ${vehicle.quantity} units`;
  document.getElementById('restock-qty').value = '';
  document.getElementById('restock-modal').classList.remove('hidden');
}

async function handleSaveVehicle(e) {
  e.preventDefault();

  const id = document.getElementById('vehicle-id').value;
  const payload = {
    make: document.getElementById('form-make').value.trim(),
    model: document.getElementById('form-model').value.trim(),
    year: parseInt(document.getElementById('form-year').value, 10),
    category: document.getElementById('form-category').value,
    price: parseFloat(document.getElementById('form-price').value),
    quantity: parseInt(document.getElementById('form-quantity').value, 10),
    color: document.getElementById('form-color').value.trim() || null,
    mileage: document.getElementById('form-mileage').value ? parseInt(document.getElementById('form-mileage').value, 10) : null
  };

  try {
    if (id) {
      await vehicleAPI.update(id, payload);
      showToast('Vehicle details updated successfully!', 'success');
    } else {
      await vehicleAPI.create(payload);
      showToast('New vehicle added to inventory!', 'success');
    }
    document.getElementById('vehicle-modal').classList.add('hidden');
    loadAdminVehicles();
  } catch (err) {
    showToast(err.message || 'Failed to save vehicle', 'error');
  }
}

async function handleRestockSubmit(e) {
  e.preventDefault();

  const id = document.getElementById('restock-vehicle-id').value;
  const qty = parseInt(document.getElementById('restock-qty').value, 10);

  try {
    const res = await vehicleAPI.restock(id, qty);
    showToast(res.message || 'Restocked successfully!', 'success');
    document.getElementById('restock-modal').classList.add('hidden');
    loadAdminVehicles();
  } catch (err) {
    showToast(err.message || 'Failed to restock vehicle', 'error');
  }
}

async function handleDelete(vehicle) {
  if (!confirm(`Are you sure you want to PERMANENTLY delete ${vehicle.make} ${vehicle.model} from inventory?`)) {
    return;
  }

  try {
    await vehicleAPI.delete(vehicle.id);
    showToast(`${vehicle.make} ${vehicle.model} deleted.`, 'success');
    loadAdminVehicles();
  } catch (err) {
    showToast(err.message || 'Failed to delete vehicle', 'error');
  }
}
