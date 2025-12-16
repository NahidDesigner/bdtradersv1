# 📋 Original Project Requirements - BD Tenant SaaS Platform

## 🎯 Primary Request

**Create a production-ready multi-tenant SaaS web application for Bangladesh-based merchants to create product landing pages and receive orders.**

## 📱 Application Requirements

### Core Requirements
- **Web and mobile-native look** - Modern, responsive design with mobile-first approach
- **UI Language**: Primarily in **Bangla by default**, with optional **English language toggle**
- **Multi-tenant**: Each store runs on its own **subdomain** (e.g., `storename.yourdomain.com`)
- **Scalable**: Built for growth and performance
- **Secure**: Production-ready security practices
- **Deployable**: Via **Coolify** from a public GitHub repository

## 🏗️ Technical Deliverables Requested

### 1. Database Schema
- Complete database structure
- Multi-tenant data isolation
- Relationships between tables
- Indexes and constraints

### 2. Backend API Structure
- FastAPI backend
- RESTful API endpoints
- Authentication system
- Multi-tenant middleware
- Database models and schemas

### 3. Frontend Folder Structure
- React application structure
- Component organization
- Routing setup
- State management
- i18n structure

### 4. Tenant Middleware Logic
- Subdomain-based tenant identification
- Automatic tenant resolution
- Tenant-scoped data access
- Security and isolation

### 5. Wildcard Subdomain Handling
- DNS configuration
- Reverse proxy setup
- Subdomain routing
- Tenant resolution from subdomain

### 6. Sample Environment Variables
- Backend environment variables
- Frontend environment variables
- Database configuration
- Security keys
- Third-party integrations

### 7. Deployment Instructions for Coolify
- Step-by-step Coolify setup
- Docker configuration
- Environment variable setup
- Domain configuration
- Troubleshooting guide

### 8. i18n Structure + Initial Bangla Copy
- Translation file structure
- Bangla translations for all screens
- English translations
- Language toggle functionality

## 🎨 Design Requirements

### UI/UX
- **Mobile-native look**: Bottom navigation, card-based UI, touch-friendly
- **Bold, interactive components**: Using JavaScript and CSS
- **Fonts**: Outfit and Manrope (varying fonts)
- **Color scheme**: Bold, vibrant colors (not dull pastels)
- **Bangla-first**: All UI elements in Bangla by default
- **English toggle**: Easy language switching

### Layout
- Bottom navigation for mobile
- Card-based product displays
- Touch-friendly buttons and inputs
- Responsive design for all screen sizes

## 🔑 Key Features Required

### Authentication
- OTP-based login (phone number, Bangladesh-friendly)
- Optional password-based login
- User registration
- JWT authentication
- Multiple stores per user

### Store Management
- Create and manage stores
- Store settings (name, logo, brand color)
- Currency (BDT default)
- WhatsApp/support phone
- Facebook Pixel integration
- Default store language

### Product Management
- Create products with images
- Bangla and English titles/descriptions
- Pricing with discount support
- Stock/inventory tracking
- SEO-friendly slugs
- Published/unpublished status

### Landing Pages
- SEO-optimized product landing pages
- Mobile-responsive
- Bangla-first copy
- Facebook Pixel tracking
- Single-page checkout

### Checkout System
- On-page checkout form
- Bangla labels
- Mobile number (required)
- Cash on Delivery (COD) only
- Bangla confirmation screen
- Facebook Pixel & Meta Conversion API events

### Order Management
- View all orders
- Filter by status (Bangla statuses)
- Update order status
- Order data snapshot
- CSV export

### Shipping
- Multiple shipping classes
- Bangla examples
- Dynamic cost calculation

### Notifications
- Email notifications to owner (Bangla templates)
- WhatsApp notifications (Bangla messages)
- Configurable per store
- Background task processing

### Analytics
- Per-store dashboard
- Bangla labels
- Lightweight event tracking
- Charts and metrics

## 🛠️ Technology Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Mobile-native components
- Axios for API calls
- PWA support
- i18n (react-i18next)

### Backend
- Python (FastAPI)
- PostgreSQL
- SQLAlchemy ORM
- JWT Authentication
- Background tasks (email & WhatsApp)
- Pydantic for validation

### Infrastructure
- Docker & Docker Compose
- Coolify deployment
- Nginx for static files
- Wildcard subdomain handling

## 🔒 Security Requirements

- Input validation
- Rate limiting
- CSRF protection
- CORS configuration
- Secure headers
- Tenant isolation
- JWT token security

## 📦 Deployment Requirements

- **Platform**: Coolify
- **Source**: Public GitHub repository
- **Method**: Docker Compose
- **Auto-setup**: Minimal manual configuration
- **Environment variables**: Auto-configured with defaults
- **Health checks**: For all services
- **Scaling**: Ready for horizontal scaling

## 🌐 Multi-Tenancy Requirements

- **Subdomain-based**: Each store on its own subdomain
- **Shared database**: Tenant-isolated data
- **Automatic resolution**: Middleware extracts tenant from subdomain
- **Data isolation**: All queries scoped by `tenant_id`
- **Super admin**: Platform-wide access for admins

## 📱 Mobile Requirements

- **Mobile-native look**: Bottom navigation, card UI
- **Touch-friendly**: Large buttons, easy navigation
- **PWA support**: Installable, offline-capable
- **Responsive**: Works on all screen sizes

## 🌍 Localization Requirements

- **Default language**: Bangla (bn)
- **Secondary language**: English (en)
- **Toggle**: Easy language switching
- **Store-level**: Each store can have default language
- **Complete translations**: All UI elements translated

## 🚀 Performance Requirements

- **Fast loading**: Optimized builds
- **Efficient queries**: Database optimization
- **Caching**: Where appropriate
- **CDN ready**: Static assets optimized
- **Scalable**: Ready for growth

## 📊 Additional Features

- Facebook Pixel integration
- Meta Conversion API
- Email templates (Bangla)
- WhatsApp message templates (Bangla)
- Analytics dashboard
- Order export (CSV)
- Product image uploads
- SEO optimization

## ✅ Success Criteria

1. ✅ Application runs on Coolify
2. ✅ Multi-tenant subdomain isolation works
3. ✅ Bangla-first UI with English toggle
4. ✅ Mobile-native design
5. ✅ Product landing pages work
6. ✅ Checkout system functional
7. ✅ Order management works
8. ✅ Notifications configured
9. ✅ Analytics dashboard functional
10. ✅ All features production-ready

## 📝 Notes

- **Auto-configuration**: System should work with minimal setup
- **Sensible defaults**: All environment variables have defaults
- **Documentation**: Complete setup and deployment guides
- **Error handling**: Graceful error handling throughout
- **Logging**: Comprehensive logging for debugging

---

## 🎯 Current Status

✅ **Completed**: Full-featured application with all requirements  
✅ **Base Version**: Minimal, clean version for Docker containers  
✅ **Deployed**: Working on Coolify at `bdtraders.vibecodingfield.com`  
✅ **Scalable**: Ready to add features incrementally  

---

This document captures the original comprehensive requirements for the BD Tenant SaaS Platform.

