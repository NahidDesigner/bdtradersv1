# BD Tenant SaaS Platform - Project Summary

## Overview

A production-ready multi-tenant SaaS platform for Bangladesh-based merchants to create product landing pages and receive orders. Built with React (Vite) frontend and FastAPI backend, featuring subdomain-based tenant isolation.

## Key Features

### ✅ Multi-Tenancy
- Subdomain-based tenant isolation (e.g., `storename.yourdomain.com`)
- Shared database with tenant-scoped data
- Automatic tenant resolution via middleware
- One user can own multiple stores

### ✅ Authentication
- OTP-based login using phone numbers (Bangladesh-friendly)
- Optional password-based login
- JWT authentication
- User registration

### ✅ Store Management
- Create and manage multiple stores
- Store settings (name, logo, brand color, currency)
- WhatsApp and support phone configuration
- Facebook Pixel integration
- Email/WhatsApp notification settings

### ✅ Product Management
- Create products with images
- Bangla and English titles/descriptions
- Pricing with discount support
- Stock/inventory tracking
- SEO-friendly slugs
- Published/unpublished status

### ✅ Landing Pages
- SEO-optimized product landing pages
- Mobile-responsive design
- Bangla-first UI
- Facebook Pixel tracking

### ✅ Checkout System
- Single-page checkout
- Customer information form (Bangla labels)
- Quantity selector
- Shipping class selection
- Cash on Delivery (COD)
- Order confirmation page

### ✅ Order Management
- View all orders
- Filter by status (Pending, Confirmed, Shipped, Delivered, Cancelled)
- Update order status
- Order details with customer info
- Product snapshots

### ✅ Shipping Classes
- Create multiple shipping classes
- Bangla and English names
- Cost configuration
- Active/inactive status

### ✅ Notifications
- Email notifications to store owner (Bangla templates)
- WhatsApp notifications (Bangla messages)
- Background task processing
- Configurable per store

### ✅ Analytics
- Dashboard with key metrics
- Total orders and revenue
- Pending orders count
- Today's orders and revenue
- Top products
- Orders trend over time

### ✅ Internationalization (i18n)
- Bangla as default language
- English language toggle
- All UI elements translated
- Store-level language preference

### ✅ PWA Support
- Service worker for offline caching
- Install prompt
- Mobile app-like experience

## Technology Stack

### Frontend
- React 18
- Vite
- Tailwind CSS
- React Router
- Axios
- react-i18next
- React Hook Form
- React Hot Toast
- Recharts (for analytics)

### Backend
- FastAPI
- PostgreSQL
- SQLAlchemy (async)
- Pydantic
- JWT (python-jose)
- Bcrypt (passlib)
- aiosmtplib (email)
- httpx (HTTP client)
- Jinja2 (templates)

### Infrastructure
- Docker & Docker Compose
- Nginx (reverse proxy)
- Coolify-ready deployment

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── auth.py
│   │   │       ├── tenants.py
│   │   │       ├── products.py
│   │   │       ├── orders.py
│   │   │       ├── shipping.py
│   │   │       └── analytics.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   └── security.py
│   │   ├── middleware/
│   │   │   └── tenant.py
│   │   ├── models/
│   │   │   ├── user.py
│   │   │   ├── tenant.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── shipping.py
│   │   ├── schemas/
│   │   │   ├── auth.py
│   │   │   ├── tenant.py
│   │   │   ├── product.py
│   │   │   ├── order.py
│   │   │   └── shipping.py
│   │   └── services/
│   │       ├── otp.py
│   │       ├── email.py
│   │       ├── whatsapp.py
│   │       └── facebook_pixel.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/
│   │   ├── layouts/
│   │   ├── pages/
│   │   ├── locales/
│   │   │   ├── bn/
│   │   │   └── en/
│   │   ├── utils/
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── Dockerfile
│   ├── package.json
│   └── vite.config.js
├── nginx/
│   └── nginx.conf
├── docker-compose.yml
├── README.md
├── DEPLOYMENT.md
└── ARCHITECTURE.md
```

## Database Schema

### Core Tables
- **users**: Platform users
- **tenants**: Stores/tenants
- **products**: Products (tenant-scoped)
- **orders**: Orders (tenant-scoped)
- **order_items**: Order line items
- **shipping_classes**: Shipping options (tenant-scoped)

## API Endpoints

### Authentication
- `POST /api/v1/auth/otp/request` - Request OTP
- `POST /api/v1/auth/otp/verify` - Verify OTP and login
- `POST /api/v1/auth/login` - Password login
- `POST /api/v1/auth/register` - Register user

### Tenants
- `POST /api/v1/tenants` - Create tenant
- `GET /api/v1/tenants` - List user's tenants
- `GET /api/v1/tenants/{id}` - Get tenant
- `PUT /api/v1/tenants/{id}` - Update tenant
- `GET /api/v1/tenants/slug/{slug}` - Get tenant by slug (public)

### Products
- `POST /api/v1/products` - Create product
- `GET /api/v1/products` - List products (tenant-scoped)
- `GET /api/v1/products/{id}` - Get product
- `GET /api/v1/products/slug/{slug}` - Get product by slug (public)
- `PUT /api/v1/products/{id}` - Update product
- `DELETE /api/v1/products/{id}` - Delete product

### Orders
- `POST /api/v1/orders` - Create order (public)
- `GET /api/v1/orders` - List orders (owner only)
- `GET /api/v1/orders/{id}` - Get order
- `PUT /api/v1/orders/{id}` - Update order status

### Shipping
- `POST /api/v1/shipping` - Create shipping class
- `GET /api/v1/shipping` - List shipping classes
- `PUT /api/v1/shipping/{id}` - Update shipping class
- `DELETE /api/v1/shipping/{id}` - Delete shipping class

### Analytics
- `GET /api/v1/analytics/dashboard` - Dashboard stats
- `GET /api/v1/analytics/orders/trend` - Orders trend

## Getting Started

### Development

1. **Backend**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

2. **Frontend**
```bash
cd frontend
npm install
npm run dev
```

3. **Docker**
```bash
docker-compose up -d
```

### Environment Variables

See `.env.example` files in `backend/` and `frontend/` directories.

## Deployment

See `DEPLOYMENT.md` for detailed Coolify deployment instructions.

## Important Notes

### Multi-Tenancy
- Each store runs on its own subdomain
- Tenant is automatically resolved from subdomain
- All data is tenant-scoped via `tenant_id`

### Language
- Default language: Bangla (bn)
- English toggle available
- All UI elements translated
- Store-level language preference

### Security
- JWT authentication
- Password hashing (bcrypt)
- Input validation (Pydantic)
- CORS configured
- Tenant isolation enforced

### Facebook Pixel
- Client-side tracking (PageView, Purchase)
- Server-side tracking (Meta Conversion API)
- Per-tenant configuration

## Next Steps

1. Configure environment variables
2. Set up database
3. Configure SMTP for emails
4. Configure WhatsApp API (optional)
5. Configure OTP provider
6. Deploy to Coolify
7. Set up wildcard DNS
8. Test end-to-end flow

## Support

For issues or questions:
- Check `ARCHITECTURE.md` for technical details
- Check `DEPLOYMENT.md` for deployment help
- Review code comments for implementation details

