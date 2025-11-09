# Software Requirements Specification (SRS)

Project: EcommerceWeb
Date: 2025-10-23
Author: Project Team

## 1. Introduction

This document describes the software requirements for EcommerceWeb, a Django-based online storefront. The SRS covers the system purpose, scope, stakeholders, functional and non-functional requirements, data model summary, use cases, API endpoints, security considerations, deployment notes, and acceptance criteria.

### 1.1 Purpose

Provide a single-source specification describing what EcommerceWeb must do and how the system will behave, to guide development, testing and deployment.

### 1.2 Scope

EcommerceWeb provides product browsing, detailed product pages with variations (color, size), cart management, checkout and order management, user accounts, and an admin interface for managing products, categories, variations and orders.

### 1.3 Stakeholders
- Product Owner / Business
- Developers
- QA/Testers
- End users (customers)
- Site administrators

## 2. System Overview

Key features:
- Product catalog and categories
- Product detail pages with images and variations
- Cart and cart item management (add/remove/update)
- Checkout and orders
- User accounts (register/login/profile/orders)
- Admin area for management
- Static & media handling for product images

## 3. Functional Requirements

F1. Product catalog
- FR-F1.1: Users can view a list of available products filtered by category.
- FR-F1.2: Product listing supports pagination and search.

F2. Product detail & variations
- FR-F2.1: Product page displays product name, price, description, images, stock and available variations.
- FR-F2.2: A product may expose one or more variation categories (e.g., color, size).
- FR-F2.3: Variation choices are shown as controlled inputs (select lists, radio buttons); users must choose required variations before adding to cart.
- FR-F2.4: The UI must prevent contradictory or duplicate selections; if duplicate input occurs, the server will sanitize and apply a deterministic rule (see Validation rules).

F3. Cart management
- FR-F3.1: Users can add products (with selected variations) to the cart.
- FR-F3.2: Cart items are unique per product+variation combination. Adding the same product with identical variation set increases the quantity rather than creating a duplicate line.
- FR-F3.3: Users can update quantity, remove an item, or clear variations for an existing cart item when changing choices.

F4. Checkout & orders
- FR-F4.1: Checkout captures shipping details, payment method and creates an order record.
- FR-F4.2: After successful checkout, cart is cleared and order confirmation is displayed and emailed.

F5. User accounts
- FR-F5.1: Users can register, login, logout, reset password and view their order history.

F6. Admin
- FR-F6.1: Site admins can create/edit/delete products, categories, variations and view orders.

## 4. Non-Functional Requirements

- NFR-1: Security — use Django's authentication, CSRF protection, hashed passwords and HTTPS in production.
- NFR-2: Performance — pages should load in under 2 seconds for normal product listings (small data set) on development hardware.
- NFR-3: Scalability — design facilitates moving static/media to a CDN or object storage.
- NFR-4: Maintainability — code follows Django conventions and includes tests for core flows.
- NFR-5: Availability — accurate error handling and graceful degradation for transient failures.

## 5. Data Model Summary

Primary models (as present in codebase):
- Product: product_name, slug, description, price, images, stock, category, timestamps
- Category: name, slug, description
- Variation: product(FK), variation_category (color/size), variation_value, is_active
- Cart: cart_id (session key), date_added
- CartItem: product(FK), variaton (M2M to Variation), cart(FK), quantity, is_active
- Order / Payment: order data stored in `orders` app models

Design notes:
- CartItem stores a ManyToMany relationship to Variation so a single cart item can reference multiple variation values (e.g., color + size).
- Database should include indexes on product and cart foreign keys to speed lookups.

## 6. Variation & Duplicate-selection Handling (Specific)

Problem: When the UI posts repeated or duplicate fields (example: "ATX-JEANS Size: Small Color: Red Size: Small"), the server must determine the authoritative variation set and avoid incorrect duplicates or inconsistent cart entries.

Rules and behavior:
1. Server will parse POST parameters and collect variation selections into a list of Variation objects. Duplicate keys or values are tolerated and deduplicated.
   - Example POST may contain keys: ["size","color","size"] with values ["small","red","small"].
   - Processing: iterate POST keys in order, for each key normalize value (trim, lower), and collect matching Variation objects. Use a set of (category, value) pairs to deduplicate.

2. Deterministic rule for duplicates:
   - If multiple values for the same category are provided, the server chooses the last valid, non-empty value provided (last-wins) OR the server can reject the request requiring single selection (depending on product UX). Default: last-wins for better UX.

3. Cart item uniqueness:
   - A cart line item is identified by (cart_id, product_id, sorted_variation_ids). The sorted list of variation IDs forms the canonical signature.
   - When adding to cart, compute signature and attempt to find an existing CartItem. If found, increment its quantity; otherwise create a new CartItem and attach the Variation M2M relations.

4. Validation and user feedback:
   - If required variation is missing (e.g., size required but not provided), respond with 400 and show a friendly message on product page.
   - If duplicate selections are provided and conflict (e.g., size: small and size: large), apply last-wins and display a small notice on the product page summarizing selected options.

Pseudocode for server processing (add to cart):

```
product_variation_map = {}
for key in request.POST (preserve order):
    val = normalize(request.POST[key])
    if key in valid_variation_categories:
        product_variation_map[key] = val  # last-wins

# Convert values to Variation objects (filtering duplicates)
variation_objs = []
for category, value in product_variation_map.items():
    qs = Variation.objects.filter(product=product, variation_category__iexact=category, variation_value__iexact=value)
    if qs.exists():
        variation_objs.extend(qs)  # if multiple exist, include them all but typically qs should be one

# Build signature and either find or create CartItem
signature = tuple(sorted([v.id for v in variation_objs]))
cart_item = find_cart_item_by_signature(cart, product, signature)
if cart_item:
    cart_item.quantity += 1
else:
    cart_item = CartItem.objects.create(product=product, cart=cart, quantity=1)
    cart_item.variaton.add(*variation_objs)
```

Note: `find_cart_item_by_signature` must compare the M2M set of variation IDs for each CartItem in the cart. For performance, you can normalize a JSON/text field with canonical variation ids on CartItem (stored), or compute server-side when the cart is small.

## 7. Use Cases

UC-1: Browse store and filter by category
UC-2: View product detail and select variations
UC-3: Add to cart (with validation of variations)
UC-4: Update cart quantities and remove items
UC-5: Checkout and payment
UC-6: Admin creates new product and variations

For each UC, acceptance criteria are defined in section 10.

## 8. API / Endpoint Summary

- GET /store/ — list products (supports query, pagination)
- GET /store/category/<slug>/<product_slug>/ — product detail
- POST /cart/add_cart/<product_id>/ — add product to cart (expects variation form fields)
- GET /cart/ — show cart
- POST /cart/remove_cart/<product_id>/ — decrease quantity
- POST /cart/remove_cart_item/<product_id>/ — remove item
- Checkout/endpoints in `orders` app

API notes:
- All POST endpoints require CSRF tokens for browser form posts.
- AJAX implementations must include CSRF token header.

## 9. Security & Privacy

- Use Django's authentication and permissions for admin pages.
- Enforce CSRF middleware and secure cookies.
- Store minimal customer data and adhere to privacy rules; secure PII and payment data — use third-party PCI-compliant payment processors; do not store raw card details.

## 10. Acceptance Criteria & Test Cases

AC-1: Adding product with variations
- Given a product with color and size,
- When user selects color=red and size=small and clicks Add to Cart,
- Then cart contains a single line item with product and those variation associations.

AC-2: Duplicate variation field in request (Size repeated)
- Given request contains duplicate size fields (small twice),
- When server processes the request, duplicates are deduplicated and the selected size is applied once; the cart signature uses canonical variation set and quantity increments appropriately.

AC-3: Conflicting duplicate fields (size small and size large)
- Default behavior: last-wins. Tests should confirm last provided value is used. Optionally, fail-fast depending on UX decision.

AC-4: Cart item uniqueness
- Adding same product with identical variation set increases quantity; adding same product with different variation set creates separate line.

Sample tests to include:
- Unit tests for VariationManager and Variation queries.
- Unit tests for add-to-cart flow including deduplication logic.
- Integration tests for checkout creating Order records.

## 11. Deployment Notes

- Use a production WSGI/ASGI server (gunicorn/uvicorn) behind a reverse proxy (nginx).
- Move static files to CDN and media to object storage (S3) in production.
- Keep secrets in environment variables (.env or platform-provided secret store). The project uses `python-decouple` for environment config.

## 12. Future Enhancements

- Variant inventory (track inventory per product+variation combination)
- Price adjustments per variation (e.g., large costs extra)
- Improved UI for variation selection with thumbnails
- API for headless usage

## 13. Glossary

- Variation: a product attribute (color, size) with a value.
- CartItem signature: canonical representation of product + variation ids.

---

End of SRS
