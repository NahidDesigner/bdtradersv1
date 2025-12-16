# 🎯 BD Tenant SaaS - Base Version

## ✅ Clean, Minimal, Docker-Optimized Base Version

This is the **base version** of the BD Tenant SaaS platform - optimized for Docker containers, minimal dependencies, and ready to scale.

## 🚀 Quick Start

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose -f docker-compose.base.yaml up -d

# View logs
docker-compose -f docker-compose.base.yaml logs -f

# Stop services
docker-compose -f docker-compose.base.yaml down
```

### What's Included

**Backend:**
- ✅ FastAPI with async SQLAlchemy
- ✅ PostgreSQL database
- ✅ JWT authentication
- ✅ OTP-based login
- ✅ Multi-tenant support
- ✅ Core API endpoints

**Frontend:**
- ✅ React + Vite
- ✅ Tailwind CSS
- ✅ i18n (Bangla + English)
- ✅ Core pages (Login, Dashboard, Products, Orders)
- ✅ Product landing pages

**Docker:**
- ✅ Optimized Dockerfiles
- ✅ Health checks
- ✅ Auto-configuration
- ✅ Network isolation

## 📋 Base Features

### Authentication
- OTP-based login (phone number)
- JWT token authentication
- User registration

### Store Management
- Create and manage stores
- Store settings (name, logo, brand color)
- Multi-store support per user

### Products
- Create, read, update, delete products
- Product images
- Pricing and stock management
- Product landing pages

### Orders
- Create orders (public checkout)
- View orders (store owner)
- Update order status
- Order details

## 🗂️ File Structure

```
.
├── backend/
│   ├── Dockerfile.base          # Base backend Dockerfile
│   ├── requirements-base.txt     # Minimal dependencies
│   └── app/                      # Application code
├── frontend/
│   ├── Dockerfile.base           # Base frontend Dockerfile
│   ├── package-base.json         # Minimal dependencies
│   └── src/                      # Application code
├── docker-compose.base.yaml      # Base Docker Compose
└── BASE_VERSION_README.md        # This file
```

## 🔧 Configuration

### Auto-Configuration

The base version uses **sensible defaults** - no manual configuration needed!

**Default values:**
- Database: `postgres` / `bdtenant2024secure` / `bdtenant`
- JWT: Auto-generated secrets (change in production!)
- CORS: Allow all origins
- Ports: Backend 8000, Frontend 80

### Environment Variables (Optional)

You can override defaults by setting environment variables:

```bash
# Database
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_DB=bdtenant

# Security (change in production!)
SECRET_KEY=your-secret-key
JWT_SECRET=your-jwt-secret

# Frontend
VITE_API_URL=http://localhost:8000
VITE_BASE_DOMAIN=localhost
```

## 📦 Dependencies

### Backend (Minimal)
- FastAPI, Uvicorn
- SQLAlchemy, PostgreSQL driver
- Pydantic, JWT, Bcrypt
- Basic file handling

### Frontend (Minimal)
- React, React Router
- Axios
- Tailwind CSS
- i18n (react-i18next)

**Removed for base version:**
- ❌ Email notifications
- ❌ WhatsApp notifications
- ❌ Facebook Pixel
- ❌ Analytics charts
- ❌ PWA features
- ❌ Redis/Celery

## 🚀 Deployment

### Local Development

```bash
# Start services
docker-compose -f docker-compose.base.yaml up -d

# Access:
# Frontend: http://localhost
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Production (Coolify)

1. **Push to GitHub**
2. **In Coolify:**
   - Create new Docker Compose resource
   - Use `docker-compose.base.yaml`
   - Set environment variables (optional)
   - Deploy!

## 📈 Scaling Guide

See `SCALING_GUIDE.md` for:
- Adding email notifications
- Adding WhatsApp notifications
- Adding analytics
- Adding Facebook Pixel
- Adding Redis/Celery
- Performance optimization

## 🎯 Next Steps

1. **Test the base version:**
   ```bash
   docker-compose -f docker-compose.base.yaml up -d
   ```

2. **Access the app:**
   - Frontend: `http://localhost`
   - Backend API: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

3. **Create a store:**
   - Register/Login
   - Create a store
   - Add products
   - Test checkout

4. **Scale as needed:**
   - Follow `SCALING_GUIDE.md`
   - Add features incrementally

## 📝 Notes

- **Base version is production-ready** but minimal
- **All core features work** out of the box
- **Easy to scale** by adding dependencies and features
- **Docker-optimized** for fast builds and small images
- **Auto-configuration** means zero setup time

## 🐛 Troubleshooting

### Database Connection Issues

```bash
# Check postgres is running
docker-compose -f docker-compose.base.yaml ps

# Check logs
docker-compose -f docker-compose.base.yaml logs postgres
docker-compose -f docker-compose.base.yaml logs backend
```

### Frontend Not Loading

```bash
# Rebuild frontend
docker-compose -f docker-compose.base.yaml build frontend
docker-compose -f docker-compose.base.yaml up -d frontend
```

### Port Conflicts

Change ports in `docker-compose.base.yaml`:
```yaml
ports:
  - "8001:8000"  # Backend
  - "8080:80"    # Frontend
```

## ✅ Success!

Your base version is ready! Start with this, then scale as needed.

