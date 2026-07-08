🛒 Django E-Commerce Platform

A full-stack e-commerce web application built with **Django**, featuring product catalog browsing, a persistent shopping cart, **Stripe** checkout, email-verified authentication, and a fully automated CI/CD pipeline.

![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-database-336791?logo=postgresql&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-payments-635BFF?logo=stripe&logoColor=white)
![Tests](https://img.shields.io/badge/tests-pytest-0A9EDC?logo=pytest&logoColor=white)
![CI](https://github.com/Adarshkumar99/Ecommerce-app-Django/actions/workflows/django.yml/badge.svg)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 📖 Overview

This project is a production-ready e-commerce backend and storefront built with Django. It covers the complete shopping flow — browsing products by category, managing a cart across guest and logged-in sessions, secure checkout with Stripe, and order tracking — with a codebase structured into clean, single-responsibility Django apps.

---

## ✨ Features

- **🔐 Authentication & Accounts**
  - User registration and login with Django's built-in auth system
  - Email verification via signed tokens (`urlsafe_base64` + `TokenGenerator`)
  - Transactional emails powered by SendGrid SMTP
  - Signal-based user profile creation

- **📦 Product Catalog**
  - Category-based product listing and filtering
  - Rich-text product descriptions via `django-ckeditor`
  - Image uploads with Cloudinary storage in production

- **🛒 Smart Shopping Cart**
  - Session-based cart for guest users
  - Automatic **guest-to-user cart merge** on login/registration
  - Context processor for cart item count available across all templates

- **💳 Secure Checkout & Payments**
  - Stripe Checkout Session integration
  - Stripe **webhook** handling for reliable order confirmation (`checkout.session.completed`)
  - Address collection before payment
  - Automatic cart clearing after a successful order

- **📑 Order Management**
  - Order and OrderItem models with status tracking (`pending`, `success`, `failed`)
  - Full order history tied to Stripe session IDs

- **⚙️ DevOps & Quality**
  - Automated test suite with `pytest` + `pytest-django`
  - Continuous Integration via **GitHub Actions**
  - One-click deployment to **Render** (`render.yaml`) with managed Postgres
  - Environment-based configuration using `.env` support
  - Production-hardened settings: Whitenoise static file serving, secure cookies, CSRF trusted origins

---

## 🏗️ Tech Stack

| Layer            | Technology                              |
|-------------------|------------------------------------------|
| Backend           | Django 4.2, Python                       |
| Database          | PostgreSQL (via `dj-database-url`)       |
| Payments          | Stripe Checkout + Webhooks               |
| Media Storage     | Cloudinary (production) / local (dev)    |
| Email             | SendGrid SMTP                            |
| Static Files      | WhiteNoise                               |
| Rich Text         | django-ckeditor                          |
| Testing           | pytest, pytest-django, pytest-mock       |
| CI/CD             | GitHub Actions, Render                   |
| Server            | Gunicorn (WSGI)                          |

---

## 📂 Project Structure

```
Ecommerce-app-Django/
├── Ecommerce/          # Project settings, root URLs, WSGI/ASGI entrypoints
├── accounts/           # Registration, login, logout, email verification
├── products/           # Product & category models, catalog views
├── cart/                # Cart models, session/guest-cart merge logic
├── checkout/            # Address capture, Stripe session creation, webhooks
├── orders/              # Order & OrderItem models
├── core/                 # Shared/home views
├── templates/            # Global HTML templates
├── static/               # Source static assets
├── conftest.py            # Shared pytest fixtures
├── render.yaml             # Render deployment blueprint
└── requirements.txt         # Python dependencies
```

Each app follows Django convention (`models.py`, `views.py`, `urls.py`, `tests/`) for clear separation of concerns.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- PostgreSQL (or use SQLite locally by adjusting `DATABASE_URL`)
- A [Stripe](https://stripe.com) account (test mode keys)
- A [SendGrid](https://sendgrid.com) account (optional, for email verification)

### 1. Clone the repository
```bash
git clone https://github.com/Adarshkumar99/Ecommerce-app-Django.git
cd Ecommerce-app-Django
```

### 2. Create a virtual environment & install dependencies
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure environment variables
Create a `.env` file in the project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgres://user:password@localhost:5432/ecommerce_db

STRIPE_SECRET_KEY=sk_test_xxxxxxxx
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxxxxx

USE_CLOUDINARY=False
CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=

SENDGRID_API_KEY=
DEFAULT_FROM_EMAIL=no-reply@example.com

CSRF_TRUSTED_ORIGINS=http://localhost:8000
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (for Django admin)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000/`.

---

## 🧪 Running Tests

The project uses `pytest` with `pytest-django`:

```bash
pytest
```

Test configuration lives in `pytest.ini` and shared fixtures in `conftest.py`. Tests are automatically run on every push via the GitHub Actions workflow in `.github/workflows/django.yml`.

---

## 💳 Stripe Webhook Setup (Local Testing)

To test the payment webhook locally with the [Stripe CLI](https://stripe.com/docs/stripe-cli):

```bash
stripe listen --forward-to localhost:8000/checkout/webhook/
```

Copy the webhook signing secret it prints into your `.env` as `STRIPE_WEBHOOK_SECRET`.

---

## ☁️ Deployment

This repo is pre-configured for one-click deployment to **Render** using `render.yaml`:

- Auto-installs dependencies, runs `collectstatic`, and applies migrations on every deploy
- Provisions a managed PostgreSQL database
- Serves static files via WhiteNoise and media via Cloudinary in production

To deploy your own instance, connect this repository to Render and it will pick up the blueprint automatically.

---

## 🗺️ Roadmap

- [ ] Order history page for logged-in users
- [ ] Product search & advanced filtering (`django-filter` is already a dependency)
- [ ] Admin dashboard for sales analytics
- [ ] Wishlist / saved items
- [ ] Product reviews & ratings

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. Feel free to check the [issues page](https://github.com/Adarshkumar99/Ecommerce-app-Django/issues).

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Adarsh Kumar**
- GitHub: [@Adarshkumar99](https://github.com/Adarshkumar99)
