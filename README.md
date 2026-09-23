# AI-Powered E-Commerce System

A full-stack, modern AI-Powered E-Commerce Application built with **Python**, **Django 5**, **PostgreSQL**, and **Vanilla HTML5/CSS3/JavaScript**.

---

## 🌟 Key Features

1. **User Authentication (FR-1)**
   - Registration, Login, Logout with custom User model.
   - Dual roles: `Customer` and `Administrator`.

2. **Product Catalog & Search (FR-2 & FR-3)**
   - Dynamic product grid with category filter pills, price sorting, and pagination.
   - Real-time debounced AJAX search bar over titles, tags, and descriptions.

3. **Shopping Cart Management (FR-4)**
   - Asynchronous AJAX Add/Update/Remove actions without page refreshes.
   - Dual support for logged-in accounts and guest browser sessions.

4. **Order Processing & History (FR-5)**
   - Checkout workflow with shipping detail capture and automatic stock deduction.
   - Customer Order History timeline and status tracking (`Pending`, `Processing`, `Shipped`, `Delivered`).

5. **AI Recommendation Engine (FR-6 & AI Requirements)**
   - **TF-IDF & Cosine Similarity Engine**: Computes similarity vectors over product metadata.
   - **AI Explanation Generator**: Explains in natural language *why* a product was recommended.
   - **Trending Engine**: Analyzes view counts and purchase velocity.
   - **Personalized Recommendations**: Tailored based on customer browsing history and active cart items.

6. **Administrator Control Center**
   - Manage inventory (Create, Edit, Delete products).
   - Process orders and update delivery status.
   - View revenue metrics and active platform stats.

---

## 🛠 Tech Stack

- **Backend**: Python 3.14, Django 5.x, Django REST Framework
- **Database**: PostgreSQL (with automatic SQLite fallback for rapid local testing)
- **Frontend**: HTML5, Vanilla CSS3 (Glassmorphism design system), Vanilla JavaScript (ES6+ AJAX)
- **AI / Data Science**: Scikit-Learn (TF-IDF Vectorizer & Cosine Similarity)

---

## 🚀 Quick Start Instructions

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Seed Sample Data & Accounts**:
   ```bash
   python manage.py seed_data
   ```
   *Created Demo Credentials:*
   - **Admin Panel**: `username: admin` | `password: admin123`
   - **Customer**: `username: customer` | `password: customer123`

4. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```
   Open `http://127.0.0.1:8000/` in your browser.

---

## 📂 Deliverables & Documentation

- [ER Diagram Specification](file:///c:/Users/yossi/Documents/antigravity/wise-hubble/docs/ER_DIAGRAM.md)
- [API Documentation](file:///c:/Users/yossi/Documents/antigravity/wise-hubble/docs/API_DOCUMENTATION.md)
