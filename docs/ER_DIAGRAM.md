# Entity-Relationship (ER) Diagram
## AI-Powered E-Commerce System

Below is the complete database structure and relationships designed for PostgreSQL / Django ORM as specified in Section 3 and 6 of the SRS document.

```mermaid
erDiagram
    USER ||--o{ ORDER : "places"
    USER ||--o{ CART : "owns (1-to-1)"
    USER ||--o{ PRODUCT_VIEW_HISTORY : "generates"
    CATEGORY ||--o{ PRODUCT : "classifies"
    PRODUCT ||--o{ CART_ITEM : "contained_in"
    PRODUCT ||--o{ ORDER_ITEM : "ordered_in"
    ORDER ||--o{ ORDER_ITEM : "contains"
    CART ||--o{ CART_ITEM : "holds"

    USER {
        bigint id PK
        string username
        string email
        string password_hash
        string role "customer | administrator"
        string phone_number
        jsonb preferred_categories
        datetime date_joined
    }

    CATEGORY {
        bigint id PK
        string name "unique"
        string slug "unique"
        text description
        string image_url
    }

    PRODUCT {
        bigint id PK
        bigint category_id FK
        string title
        string slug "unique"
        text description
        decimal price "10,2"
        integer stock
        string image_url
        string tags "comma-separated for AI vector matching"
        boolean is_featured
        integer view_count
        datetime created_at
        datetime updated_at
    }

    PRODUCT_VIEW_HISTORY {
        bigint id PK
        bigint user_id FK "nullable"
        string session_key "nullable"
        bigint product_id FK
        datetime viewed_at
    }

    CART {
        bigint id PK
        bigint user_id FK "nullable, unique"
        string session_key "nullable, unique"
        datetime created_at
        datetime updated_at
    }

    CART_ITEM {
        bigint id PK
        bigint cart_id FK
        bigint product_id FK
        integer quantity
        datetime created_at
    }

    ORDER {
        bigint id PK
        bigint user_id FK "nullable"
        string full_name
        string email
        text shipping_address
        string city
        string postal_code
        string country
        decimal total_amount "10,2"
        string status "PENDING | PROCESSING | SHIPPED | DELIVERED | CANCELLED"
        datetime created_at
        datetime updated_at
    }

    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK "nullable"
        string product_title
        decimal price "10,2"
        integer quantity
    }
```

## Detailed Entity Schema Specifications

### 1. `USER` (Table: `authentication_user`)
- Extends Django's `AbstractUser`.
- `role`: Enum `['customer', 'administrator']`. Controls view permissions and admin dashboard access.

### 2. `PRODUCT` (Table: `products_product`)
- Stores e-commerce inventory items.
- `tags`: Indexed string containing keyword tokens used by the AI TF-IDF Vectorizer to compute product similarity embeddings.
- `view_count`: Incremented on every detail view to calculate trending score metrics.

### 3. `PRODUCT_VIEW_HISTORY` (Table: `products_productviewhistory`)
- Tracks user/guest item view timestamps to feed the personalized AI recommendation engine.

### 4. `CART` & `CART_ITEM` (Tables: `cart_cart`, `cart_cartitem`)
- Supports both authenticated users and anonymous guest sessions via `session_key`.

### 5. `ORDER` & `ORDER_ITEM` (Tables: `orders_order`, `orders_orderitem`)
- Preserves price snapshots at checkout time.
