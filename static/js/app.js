/* ==========================================================================
   AI-POWERED E-COMMERCE SYSTEM - VANILLA JAVASCRIPT CONTROLLER
   Handles: Live AJAX Search, Cart Actions, Toast Alerts, Modal Interactions
   ========================================================================== */

document.addEventListener('DOMContentLoaded', () => {
  initLiveSearch();
  initCartActions();
  initAIChatbot();
});

/**
 * Live Search Component
 */
function initLiveSearch() {
  const searchInput = document.getElementById('nav-search-input');
  const resultsDropdown = document.getElementById('search-results-dropdown');

  if (!searchInput || !resultsDropdown) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.trim();

    clearTimeout(debounceTimer);
    if (query.length < 2) {
      resultsDropdown.style.display = 'none';
      return;
    }

    debounceTimer = setTimeout(() => {
      fetch(`/api/search/?q=${encodeURIComponent(query)}`)
        .then(response => response.json())
        .then(data => {
          resultsDropdown.innerHTML = '';

          if (!data.results || data.results.length === 0) {
            resultsDropdown.innerHTML = '<div style="padding: 1rem; color: #94a3b8; text-align: center;">No matching products found</div>';
          } else {
            data.results.forEach(item => {
              const row = document.createElement('a');
              row.href = item.url;
              row.className = 'search-result-item';
              row.innerHTML = `
                <img src="${item.image_url}" alt="${item.title}">
                <div>
                  <div style="font-weight: 600; color: #fff;">${item.title}</div>
                  <div style="font-size: 0.8rem; color: #94a3b8;">${item.category} • $${item.price}</div>
                </div>
              `;
              resultsDropdown.appendChild(row);
            });
          }
          resultsDropdown.style.display = 'block';
        })
        .catch(err => console.error('Search error:', err));
    }, 250);
  });

  document.addEventListener('click', (e) => {
    if (!searchInput.contains(e.target) && !resultsDropdown.contains(e.target)) {
      resultsDropdown.style.display = 'none';
    }
  });
}

/**
 * Asynchronous Cart Actions
 */
function initCartActions() {
  document.addEventListener('submit', (e) => {
    const form = e.target;
    if (form.classList.contains('ajax-add-to-cart')) {
      e.preventDefault();
      const actionUrl = form.action;
      const formData = new FormData(form);

      fetch(actionUrl, {
        method: 'POST',
        headers: {
          'X-Requested-With': 'XMLHttpRequest',
          'X-CSRFToken': getCsrfToken(),
        },
        body: formData,
      })
        .then(res => res.json())
        .then(data => {
          if (data.success) {
            showToast(data.message || 'Added to cart!', 'success');
            updateCartCounter(data.cart_total_items);
          } else {
            showToast(data.message || 'Could not add item', 'error');
          }
        })
        .catch(err => {
          console.error(err);
          showToast('An error occurred. Please try again.', 'error');
        });
    }
  });
}

function updateCartCounter(count) {
  const counterEl = document.getElementById('nav-cart-count');
  if (counterEl) {
    counterEl.textContent = count;
  }
}

/**
 * Toast Notification Utility
 */
function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('toast-container');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'toast-container';
    toastContainer.style.cssText = `
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 9999;
      display: flex;
      flex-direction: column;
      gap: 10px;
    `;
    document.body.appendChild(toastContainer);
  }

  const toast = document.createElement('div');
  const bgColor = type === 'success' ? 'rgba(16, 185, 129, 0.9)' : type === 'error' ? 'rgba(239, 68, 68, 0.9)' : 'rgba(99, 102, 241, 0.9)';

  toast.style.cssText = `
    background: ${bgColor};
    color: #fff;
    padding: 12px 20px;
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.9rem;
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    backdrop-filter: blur(8px);
    transition: all 0.3s ease;
    transform: translateY(20px);
    opacity: 0;
  `;
  toast.textContent = message;

  toastContainer.appendChild(toast);

  setTimeout(() => {
    toast.style.transform = 'translateY(0)';
    toast.style.opacity = '1';
  }, 10);

  setTimeout(() => {
    toast.style.transform = 'translateY(20px)';
    toast.style.opacity = '0';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function getCsrfToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

/**
 * AI Recommendation Chatbot Widget Controller
 */
function initAIChatbot() {
  const toggleBtn = document.getElementById('ai-chat-toggle');
  const chatWindow = document.getElementById('ai-chat-window');
  const closeBtn = document.getElementById('ai-chat-close');
  const chatForm = document.getElementById('ai-chat-form');
  const chatInput = document.getElementById('ai-chat-input');

  if (!toggleBtn || !chatWindow) return;

  toggleBtn.addEventListener('click', () => {
    const isVisible = chatWindow.style.display === 'flex';
    chatWindow.style.display = isVisible ? 'none' : 'flex';
  });

  if (closeBtn) {
    closeBtn.addEventListener('click', () => {
      chatWindow.style.display = 'none';
    });
  }

  if (chatForm) {
    chatForm.addEventListener('submit', (e) => {
      e.preventDefault();
      const msg = chatInput.value.trim();
      if (!msg) return;
      chatInput.value = '';
      sendChatQuery(msg);
    });
  }
}

function sendChatQuery(msgText) {
  const chatBody = document.getElementById('ai-chat-body');
  const chatWindow = document.getElementById('ai-chat-window');
  if (chatWindow && chatWindow.style.display !== 'flex') {
    chatWindow.style.display = 'flex';
  }

  const chipsArea = document.getElementById('chat-chips-area');
  if (chipsArea) chipsArea.style.display = 'none';

  const userBubble = document.createElement('div');
  userBubble.className = 'chat-msg user';
  userBubble.textContent = msgText;
  chatBody.appendChild(userBubble);
  chatBody.scrollTop = chatBody.scrollHeight;

  const botLoading = document.createElement('div');
  botLoading.className = 'chat-msg bot';
  botLoading.textContent = 'Analyzing recommendations for you... 🤖';
  chatBody.appendChild(botLoading);
  chatBody.scrollTop = chatBody.scrollHeight;

  fetch('/ai-recommendations/api/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCsrfToken(),
    },
    body: JSON.stringify({ message: msgText }),
  })
    .then(res => res.json())
    .then(data => {
      botLoading.remove();

      const botReply = document.createElement('div');
      botReply.className = 'chat-msg bot';
      botReply.innerHTML = data.reply;
      chatBody.appendChild(botReply);

      if (data.products && data.products.length > 0) {
        data.products.forEach(p => {
          const pCard = document.createElement('div');
          pCard.className = 'chat-product-card';
          pCard.innerHTML = `
            <img src="${p.image_url}" alt="${p.title}">
            <div style="flex: 1;">
              <a href="${p.url}" style="font-weight: 600; color: #fff; font-size: 0.85rem;">${p.title}</a>
              <div style="font-size: 0.78rem; color: #06b6d4;">$${p.price} • ${p.explanation}</div>
            </div>
            <form action="/cart/add/${p.id}/" method="post" class="ajax-add-to-cart" style="margin: 0;">
              <input type="hidden" name="csrfmiddlewaretoken" value="${getCsrfToken()}">
              <button type="submit" class="btn btn-primary btn-sm" style="padding: 0.25rem 0.6rem; font-size: 0.75rem;">+ Cart</button>
            </form>
          `;
          chatBody.appendChild(pCard);
        });
      }

      chatBody.scrollTop = chatBody.scrollHeight;
    })
    .catch(err => {
      console.error(err);
      botLoading.textContent = 'Sorry, I encountered an error fetching AI recommendations.';
    });
}
