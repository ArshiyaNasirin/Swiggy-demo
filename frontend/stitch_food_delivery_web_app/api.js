/**
 * TastingRoom Web Application - Central API & State Management
 * =============================================================
 * Contains:
 *   1. Typography Configuration (Cambria Serif Font & Material Icons)
 *   2. Global Configuration & Constants
 *   3. Backend API Client (Fetch Wrapper & Endpoints)
 *   4. Cart State Management (LocalStorage Engine & Price Calculations)
 *   5. UI Helpers (Toast Notification System)
 *   6. Navigation Auto-Wire (Sidebar & Header Bindings)
 *   7. Initialization & Lifecycle Event Handlers
 */

// =============================================================================
// 1. TYPOGRAPHY & GLOBAL STYLE CONFIGURATION
// =============================================================================
(function applyGlobalTypography() {
  const fontStyle = document.createElement('style');
  fontStyle.id = 'tastingroom-typography';
  fontStyle.textContent = `
    /* Apply Cambria typography across all standard textual and input elements */
    body, h1, h2, h3, h4, h5, h6, p, label, input, select, textarea, button:not(.material-symbols-outlined) {
      font-family: 'Cambria', Georgia, 'Times New Roman', serif;
    }
    /* Explicitly preserve Material Symbols icon font rules */
    .material-symbols-outlined, [class*="material-symbols"] {
      font-family: 'Material Symbols Outlined' !important;
      font-style: normal;
      font-weight: normal;
      display: inline-block;
      line-height: 1;
      text-transform: none;
      letter-spacing: normal;
      word-wrap: normal;
      white-space: nowrap;
      direction: ltr;
    }
  `;
  if (document.head) {
    document.head.appendChild(fontStyle);
  } else {
    document.addEventListener('DOMContentLoaded', () => document.head.appendChild(fontStyle));
  }
})();


// =============================================================================
// 2. GLOBAL CONFIGURATION & CONSTANTS
// =============================================================================
// API Base URL - Automatically routes to local FastAPI server on port 8000
const API_BASE = window.location.port === '8000' 
  ? '/api/v1' 
  : 'http://127.0.0.1:8000/api/v1';

// Default active demo user identifier
const CURRENT_USER_ID = 1;


// =============================================================================
// 3. BACKEND API CLIENT (REST Endpoints)
// =============================================================================
const API = {
  /**
   * Generic HTTP Request Wrapper
   * Handles JSON serialization, headers, and standard error handling.
   */
  async request(endpoint, options = {}) {
    const url = `${API_BASE}${endpoint}`;
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };
    
    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...defaultHeaders,
          ...(options.headers || {})
        }
      });
      
      if (!response.ok) {
        let errorDetail = response.statusText;
        try {
          const errJson = await response.json();
          errorDetail = errJson.detail || JSON.stringify(errJson);
        } catch (_) {}
        throw new Error(`API Error [${response.status}]: ${errorDetail}`);
      }
      
      return await response.json();
    } catch (err) {
      console.error(`Request failed: ${url}`, err);
      throw err;
    }
  },

  // --- Restaurant Endpoints ---
  async getRestaurants(activeOnly = false) {
    return this.request(`/restaurants/?active_only=${activeOnly}`);
  },
  
  async getRestaurant(id) {
    return this.request(`/restaurants/${id}`);
  },

  // --- Food Item Endpoints ---
  async getFoods(restaurantId = null, availableOnly = false) {
    let query = `?available_only=${availableOnly}`;
    if (restaurantId) query += `&restaurant_id=${restaurantId}`;
    return this.request(`/foods/${query}`);
  },

  async getFood(id) {
    return this.request(`/foods/${id}`);
  },

  // --- Order Endpoints ---
  async createOrder(orderPayload) {
    return this.request('/orders/', {
      method: 'POST',
      body: JSON.stringify(orderPayload)
    });
  },

  async getOrders(userId = null) {
    let query = '';
    if (userId) query = `?user_id=${userId}`;
    return this.request(`/orders/${query}`);
  },

  async getOrder(id) {
    return this.request(`/orders/${id}`);
  },

  async cancelOrder(id) {
    return this.request(`/orders/${id}/cancel`, {
      method: 'PATCH'
    });
  },

  async updateOrderStatus(id, status) {
    return this.request(`/orders/${id}/status`, {
      method: 'PATCH',
      body: JSON.stringify({ status })
    });
  },

  // --- User Profile Endpoints ---
  async getUser(id = CURRENT_USER_ID) {
    return this.request(`/users/${id}`);
  },

  async updateUser(id, userData) {
    return this.request(`/users/${id}`, {
      method: 'PUT',
      body: JSON.stringify(userData)
    });
  }
};


// =============================================================================
// 4. CART STATE MANAGEMENT (LocalStorage Engine)
// =============================================================================
const Cart = {
  STORAGE_KEY: 'tastingroom_cart',

  /**
   * Retrieve active cart data from browser localStorage.
   */
  getData() {
    try {
      const raw = localStorage.getItem(this.STORAGE_KEY);
      return raw ? JSON.parse(raw) : { restaurantId: null, restaurantName: '', items: [] };
    } catch {
      return { restaurantId: null, restaurantName: '', items: [] };
    }
  },

  /**
   * Save updated cart data to localStorage and sync badges.
   */
  save(cartData) {
    localStorage.setItem(this.STORAGE_KEY, JSON.stringify(cartData));
    this.updateCartBadge();
  },

  /**
   * Add a dish to the active cart.
   * Prompts user before clearing if adding from a different restaurant.
   */
  addItem(food, restaurantId, restaurantName) {
    const cart = this.getData();
    
    if (cart.items.length > 0 && cart.restaurantId !== restaurantId) {
      const switchConfirmed = confirm(
        `Your cart already contains items from ${cart.restaurantName || 'another restaurant'}.\nClear cart to start a new order with ${restaurantName}?`
      );
      if (!switchConfirmed) {
        return false;
      }
      cart.items = [];
    }

    cart.restaurantId = restaurantId;
    cart.restaurantName = restaurantName;

    const existingIndex = cart.items.findIndex(i => i.id === food.id);
    if (existingIndex > -1) {
      cart.items[existingIndex].quantity += 1;
    } else {
      cart.items.push({
        id: food.id,
        name: food.name,
        price: food.price,
        description: food.description || '',
        quantity: 1
      });
    }

    this.save(cart);
    showToast(`Added "${food.name}" to cart!`);
    return true;
  },

  /**
   * Increment or decrement the quantity of an item in the cart.
   */
  updateQty(foodId, delta) {
    const cart = this.getData();
    const index = cart.items.findIndex(i => i.id === foodId);
    
    if (index > -1) {
      cart.items[index].quantity += delta;
      if (cart.items[index].quantity <= 0) {
        cart.items.splice(index, 1);
      }
      if (cart.items.length === 0) {
        cart.restaurantId = null;
        cart.restaurantName = '';
      }
      this.save(cart);
    }
    return cart;
  },

  /**
   * Empty all items from the active cart.
   */
  clear() {
    this.save({ restaurantId: null, restaurantName: '', items: [] });
  },

  /**
   * Calculate total item count in cart.
   */
  getCount() {
    const cart = this.getData();
    return cart.items.reduce((sum, item) => sum + item.quantity, 0);
  },

  /**
   * Calculate subtotal price for items in cart.
   */
  getSubtotal() {
    const cart = this.getData();
    return cart.items.reduce((sum, item) => sum + (item.price * item.quantity), 0);
  },

  /**
   * Calculate standard delivery fee.
   */
  getDeliveryFee() {
    return this.getCount() > 0 ? 1.99 : 0.00;
  },

  /**
   * Calculate estimated tax (8.25%).
   */
  getTax() {
    return +(this.getSubtotal() * 0.0825).toFixed(2);
  },

  /**
   * Calculate grand total including tax and delivery.
   */
  getTotal() {
    if (this.getCount() === 0) return 0;
    return +(this.getSubtotal() + this.getDeliveryFee() + this.getTax()).toFixed(2);
  },

  /**
   * Sync header cart count badges across open pages.
   */
  updateCartBadge() {
    const count = this.getCount();
    document.querySelectorAll('.cart-badge, header button .text-label-sm').forEach(badge => {
      badge.textContent = count;
      if (count === 0) {
        badge.classList.add('opacity-0');
      } else {
        badge.classList.remove('opacity-0');
      }
    });
  }
};


// =============================================================================
// 5. UI TOAST NOTIFICATION HELPER
// =============================================================================
function showToast(message, type = 'success') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.className = 'fixed bottom-6 right-6 z-50 flex flex-col gap-2 pointer-events-none';
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  const bg = type === 'error' ? 'bg-red-600' : 'bg-primary text-on-primary';
  toast.className = `${bg} text-white px-5 py-3 rounded-full shadow-2xl flex items-center gap-2 transform transition-all duration-300 translate-y-4 opacity-0 pointer-events-auto font-medium text-sm`;
  toast.innerHTML = `
    <span class="material-symbols-outlined text-[18px]">${type === 'error' ? 'error' : 'check_circle'}</span>
    <span>${message}</span>
  `;

  toastContainer.appendChild(toast);
  requestAnimationFrame(() => {
    toast.classList.remove('translate-y-4', 'opacity-0');
  });

  setTimeout(() => {
    toast.classList.add('opacity-0', 'translate-y-2');
    setTimeout(() => toast.remove(), 300);
  }, 2500);
}


// =============================================================================
// 6. GLOBAL NAVIGATION AUTO-WIRE
// =============================================================================
function initNavigation() {
  // Navigation sidebar mapping
  const links = {
    'home': '../home/code.html',
    'restaurants': '../restaurants/code.html',
    'orders': '../orders/code.html',
    'profile': '../profile/code.html'
  };

  document.querySelectorAll('aside nav a').forEach(a => {
    const path = a.getAttribute('data-path');
    if (path && links[path]) {
      a.href = links[path];
    }
  });

  // Header shopping bag button -> shopping cart view
  document.querySelectorAll('header button').forEach(btn => {
    if (btn.querySelector('.material-symbols-outlined')?.textContent.trim() === 'shopping_bag') {
      btn.style.cursor = 'pointer';
      btn.onclick = () => {
        window.location.href = '../shopping_cart/code.html';
      };
    }
  });

  // Header user profile avatar -> profile view
  document.querySelectorAll('header .cursor-pointer').forEach(el => {
    if (el.querySelector('.material-symbols-outlined')?.textContent.trim() === 'person') {
      el.onclick = () => {
        window.location.href = '../profile/code.html';
      };
    }
  });

  // Sync initial cart counter badge
  Cart.updateCartBadge();
}


// =============================================================================
// 7. INITIALIZATION & LIFECYCLE EVENT HANDLERS
// =============================================================================
document.addEventListener('DOMContentLoaded', initNavigation);
