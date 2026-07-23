import { authAPI } from './api.js';
import { showToast } from './utils.js';

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const registerForm = document.getElementById('register-form');

  if (loginForm) {
    const fillUserBtn = document.getElementById('fill-user-btn');
    const fillAdminBtn = document.getElementById('fill-admin-btn');
    const togglePasswordBtn = document.getElementById('toggle-password-btn');

    if (togglePasswordBtn) {
      togglePasswordBtn.addEventListener('click', () => {
        const passwordInput = document.getElementById('password');
        if (passwordInput.type === 'password') {
          passwordInput.type = 'text';
        } else {
          passwordInput.type = 'password';
        }
      });
    }

    if (fillUserBtn) {
      fillUserBtn.addEventListener('click', () => {
        document.getElementById('email').value = 'user@dealership.com';
        document.getElementById('password').value = 'User@123';
      });
    }

    if (fillAdminBtn) {
      fillAdminBtn.addEventListener('click', () => {
        document.getElementById('email').value = 'admin@dealership.com';
        document.getElementById('password').value = 'Admin@123';
      });
    }

    loginForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      const submitBtn = document.getElementById('submit-btn');
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-75');

      try {
        const data = await authAPI.login(email, password);
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        showToast('Login successful! Redirecting...', 'success');
        setTimeout(() => {
          if (data.user.role === 'admin') {
            window.location.href = 'admin.html';
          } else {
            window.location.href = 'dashboard.html';
          }
        }, 800);
      } catch (err) {
        showToast(err.message || 'Failed to login', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75');
      }
    });
  }

  if (registerForm) {
    registerForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const name = document.getElementById('name').value.trim();
      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      const submitBtn = document.getElementById('submit-btn');
      submitBtn.disabled = true;
      submitBtn.classList.add('opacity-75');

      try {
        const data = await authAPI.register(name, email, password);
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('user', JSON.stringify(data.user));

        showToast('Registration successful! Welcome to Apex Auto.', 'success');
        setTimeout(() => {
          window.location.href = 'dashboard.html';
        }, 800);
      } catch (err) {
        showToast(err.message || 'Failed to register', 'error');
      } finally {
        submitBtn.disabled = false;
        submitBtn.classList.remove('opacity-75');
      }
    });
  }
});
