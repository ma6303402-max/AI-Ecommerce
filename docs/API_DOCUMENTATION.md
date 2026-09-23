# API Documentation
## AI-Powered E-Commerce Platform REST API

This document describes the RESTful endpoints available in the AI-Powered E-Commerce Application.

---

## 1. Authentication Endpoints

### `POST /auth/login/`
Authenticates a user session.
- **Request Body**: `username`, `password`
- **Response**: Redirect / 200 OK with session cookie.

### `POST /auth/register/`
Registers a new customer account.
- **Request Body**: `username`, `email`, `password`, `phone_number`
- **Response**: 201 Created & Session Established.

---

## 2. Product Catalog & Search API

### `GET /api/search/?q={query}`
Performs live asynchronous search over product titles, descriptions, and AI tags.
- **Query Params**: `q` (string, min 2 chars)
- **Response**:
```json
{
  "results": [
    {
      "id": 1,
      "title": "Aura AI Vision Smart Companion Robot",
      "price": "499.99",
      "image_url": "https://images.unsplash.com/...",
      "url": "/product/aura-ai-vision-smart-companion-robot/",
      "category": "AI Gadgets & Robotics"
    }
  ]
}
```

---

## 3. AI Recommendation Engine APIs

### `GET /ai-recommendations/api/product/{product_id}/`
Retrieves content-based TF-IDF recommendations for a specific product along with natural language rationale explanations.
- **Response**:
```json
{
  "source_product": "Aura AI Vision Smart Companion Robot",
  "recommendations": [
    {
      "id": 2,
      "title": "Quantum Neural AI Pocket Translator",
      "price": "189.50",
      "image_url": "https://images.unsplash.com/...",
      "url": "/product/quantum-neural-ai-pocket-translator/",
      "similarity_score": 0.85,
      "explanation": "Recommended because both items share key features (ai, neural) and matching specifications.",
      "category": "AI Gadgets & Robotics"
    }
  ]
}
```

### `GET /ai-recommendations/api/personalized/`
Retrieves personalized recommendations computed from the customer's view history and shopping cart contents.

---

## 4. Shopping Cart API

### `POST /cart/add/{product_id}/`
Adds an item to the shopping cart or updates its quantity.
- **Header**: `X-Requested-With: XMLHttpRequest` (for AJAX)
- **Form Data**: `quantity` (int)
- **Response**:
```json
{
  "success": true,
  "message": "Added 'Pulse ANC Neural Spatial Headphones' to cart!",
  "cart_total_items": 3,
  "cart_total_price": "798.99"
}
```

### `POST /cart/update/{item_id}/`
Updates item quantity in cart.

### `POST /cart/remove/{item_id}/`
Removes an item from cart.

---

## 5. Orders API

### `POST /orders/checkout/`
Processes cart checkout and converts cart items to an Order.
- **Form Data**: `full_name`, `email`, `shipping_address`, `city`, `postal_code`, `country`
- **Response**: Order object & confirmation screen.
