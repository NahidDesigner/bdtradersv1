# Architecture Overview

## Multi-Tenancy Architecture

This application uses **subdomain-based multi-tenancy** with a **shared database, tenant-isolated data** approach.

### How It Works

1. **Subdomain Extraction**: The `TenantMiddleware` extracts the subdomain from the `Host` header
2. **Tenant Resolution**: The middleware queries the database to find the tenant by slug
3. **Request Context**: The tenant is stored in `request.state.tenant` for use in route handlers
4. **Data Isolation**: All queries automatically filter by `tenant_id`

### Example Flow

```
Request: GET https://storename.yourdomain.com/api/v1/products

1. TenantMiddleware extracts "storename" from Host header
2. Queries database: SELECT * FROM tenants WHERE slug = 'storename'
3. Stores tenant in request.state.tenant
4. Route handler uses tenant.id to filter products
5. Returns only products where tenant_id = tenant.id
```

## Database Schema

### Core Tables

- **users**: Platform users (can own multiple stores)
- **tenants**: Stores/tenants (one per subdomain)
- **products**: Products (scoped by tenant_id)
- **orders**: Orders (scoped by tenant_id)
- **order_items**: Order line items
- **shipping_classes**: Shipping options (scoped by tenant_id)

### Tenant Isolation

All tenant-specific tables include `tenant_id` foreign key:
- Products: `tenant_id` → tenants.id
- Orders: `tenant_id` → tenants.id
- Shipping Classes: `tenant_id` → tenants.id

## API Structure

### Authentication

- **POST /api/v1/auth/otp/request**: Request OTP for phone number
- **POST /api/v1/auth/otp/verify**: Verify OTP and login/register
- **POST /api/v1/auth/login**: Password-based login
- **POST /api/v1/auth/register**: Register new user

### Tenants

- **POST /api/v1/tenants**: Create new tenant
- **GET /api/v1/tenants**: List user's tenants
- **GET /api/v1/tenants/{id}**: Get tenant details
- **PUT /api/v1/tenants/{id}**: Update tenant
- **GET /api/v1/tenants/slug/{slug}**: Get tenant by slug (public)

### Products

- **POST /api/v1/products**: Create product (requires tenant context)
- **GET /api/v1/products**: List products (tenant-scoped)
- **GET /api/v1/products/{id}**: Get product
- **GET /api/v1/products/slug/{slug}**: Get product by slug (public)
- **PUT /api/v1/products/{id}**: Update product
- **DELETE /api/v1/products/{id}**: Delete product

### Orders

- **POST /api/v1/orders**: Create order (public, tenant-scoped)
- **GET /api/v1/orders**: List orders (owner only)
- **GET /api/v1/orders/{id}**: Get order
- **PUT /api/v1/orders/{id}**: Update order status

### Shipping

- **POST /api/v1/shipping**: Create shipping class
- **GET /api/v1/shipping**: List shipping classes (tenant-scoped)
- **PUT /api/v1/shipping/{id}**: Update shipping class
- **DELETE /api/v1/shipping/{id}**: Delete shipping class

### Analytics

- **GET /api/v1/analytics/dashboard**: Dashboard stats
- **GET /api/v1/analytics/orders/trend**: Orders trend over time

## Frontend Structure

### Routing

- **Public Routes** (`/`): Product landing pages, checkout
- **Auth Routes** (`/auth`): Login, register
- **App Routes** (`/app`): Dashboard, store management (protected)

### State Management

- **AuthContext**: User authentication state
- **TenantContext**: Current tenant (from subdomain) and user's tenants

### i18n

- Default language: Bangla (`bn`)
- Fallback language: English (`en`)
- Translations stored in `/src/locales/{lang}/translation.json`

## Security Considerations

### Authentication

- JWT tokens stored in localStorage
- Tokens include user ID and UUID
- Token expiration: 24 hours (configurable)

### Tenant Isolation

- All tenant-scoped queries filter by `tenant_id`
- Middleware validates tenant exists and is active
- Public endpoints (product pages) still require tenant context

### Input Validation

- Pydantic schemas validate all API inputs
- Phone number validation for Bangladesh format
- SQL injection protection via SQLAlchemy ORM

### CORS

- Configured for specific origins
- Supports wildcard subdomains

## Deployment Architecture

### Docker Services

1. **postgres**: PostgreSQL database
2. **backend**: FastAPI application
3. **frontend**: React application (served via Nginx)
4. **nginx**: Reverse proxy and subdomain routing

### Nginx Configuration

- Wildcard subdomain matching: `*.yourdomain.com`
- Routes to frontend for UI
- Routes `/api/*` to backend
- Preserves `Host` header for tenant resolution

### Environment Variables

- Backend: Database, JWT, SMTP, WhatsApp, OTP settings
- Frontend: API URL, base domain

## Scaling Considerations

### Current Limitations

- Single database instance
- No Redis for OTP storage (uses in-memory)
- Background tasks run in same process
- No CDN for static assets

### Production Recommendations

1. **Database**: Use managed PostgreSQL (RDS, DigitalOcean)
2. **Caching**: Add Redis for OTP, sessions
3. **Background Tasks**: Use Celery with Redis broker
4. **CDN**: CloudFlare or AWS CloudFront for static assets
5. **Load Balancing**: Multiple backend instances behind load balancer
6. **Monitoring**: Application performance monitoring (APM)
7. **Logging**: Centralized logging (ELK stack, Datadog)

## Facebook Pixel Integration

### Client-Side

- Facebook Pixel script loaded on public pages
- Tracks PageView, Purchase events
- Pixel ID configured per tenant

### Server-Side (Meta Conversion API)

- Purchase events sent to Meta Conversion API
- Deduplication via event_id
- Includes customer data (hashed)

## Notification System

### Email

- SMTP-based email sending
- Bangla email templates
- Background task execution

### WhatsApp

- Abstracted service layer
- Supports multiple providers (Twilio, WhatsApp Business API)
- Bangla message templates

## Future Enhancements

1. **Payment Gateway**: Integration with local payment providers
2. **Inventory Management**: Advanced stock tracking
3. **Multi-currency**: Support for multiple currencies
4. **Staff Roles**: Role-based access control
5. **Analytics**: Advanced analytics and reporting
6. **Mobile App**: React Native mobile app
7. **API Rate Limiting**: Per-tenant rate limits
8. **Webhooks**: Order status webhooks
9. **Product Variants**: Size, color, etc.
10. **Coupons**: Discount codes and promotions

