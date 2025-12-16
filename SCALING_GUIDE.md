# 📈 Scaling Guide - From Base to Full Version

## 🎯 Overview

This guide shows how to scale from the **base version** to the **full version** with all features.

## 📦 Step-by-Step Scaling

### Step 1: Add Email Notifications

**1. Update Backend Dependencies:**

```bash
# Add to backend/requirements-base.txt
aiosmtplib==3.0.1
jinja2==3.1.2
```

**2. Update Environment Variables:**

```yaml
# In docker-compose.base.yaml or Coolify
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

**3. Add Email Service:**

Copy `backend/app/services/email.py` from full version.

**4. Update Order Creation:**

Add email notification when order is created.

**5. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build backend
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 2: Add WhatsApp Notifications

**1. Update Backend Dependencies:**

```bash
# Add to backend/requirements-base.txt
httpx==0.25.2
```

**2. Update Environment Variables:**

```yaml
WHATSAPP_API_KEY=your-api-key
WHATSAPP_API_URL=https://api.whatsapp.com
WHATSAPP_PHONE_NUMBER_ID=your-phone-id
```

**3. Add WhatsApp Service:**

Copy `backend/app/services/whatsapp.py` from full version.

**4. Update Order Creation:**

Add WhatsApp notification when order is created.

**5. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build backend
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 3: Add Analytics Dashboard

**1. Update Frontend Dependencies:**

```bash
# Add to frontend/package-base.json
"recharts": "^2.10.3"
"date-fns": "^2.30.0"
```

**2. Add Analytics API Endpoint:**

Copy `backend/app/api/v1/analytics.py` from full version.

**3. Add Analytics Page:**

Copy `frontend/src/pages/AnalyticsPage.jsx` from full version.

**4. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 4: Add Facebook Pixel

**1. Add Facebook Pixel Component:**

Copy `frontend/src/components/FacebookPixel.jsx` from full version.

**2. Update Tenant Model:**

Add `facebook_pixel_id` field to tenant model.

**3. Add Pixel Tracking:**

Add pixel events to checkout and order confirmation.

**4. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build frontend
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 5: Add Shipping Classes

**1. Add Shipping Model:**

Copy `backend/app/models/shipping.py` from full version.

**2. Add Shipping API:**

Copy `backend/app/api/v1/shipping.py` from full version.

**3. Update Checkout:**

Add shipping class selection to checkout page.

**4. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 6: Add Redis & Celery (Background Tasks)

**1. Update Docker Compose:**

```yaml
services:
  redis:
    image: redis:7-alpine
    container_name: bd_tenant_redis
    restart: unless-stopped
    networks:
      - bd_tenant_network

  celery:
    build:
      context: ./backend
      dockerfile: Dockerfile.base
    command: celery -A app.celery worker --loglevel=info
    environment:
      # Same as backend
    depends_on:
      - redis
      - postgres
    networks:
      - bd_tenant_network
```

**2. Update Backend Dependencies:**

```bash
# Add to backend/requirements-base.txt
celery==5.3.4
redis==5.0.1
```

**3. Add Celery Configuration:**

Copy Celery setup from full version.

**4. Update Notifications:**

Move email/WhatsApp to Celery tasks.

**5. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build
docker-compose -f docker-compose.base.yaml up -d
```

---

### Step 7: Add PWA Support

**1. Update Frontend Dependencies:**

```bash
# Add to frontend/package-base.json
"vite-plugin-pwa": "^0.17.4"
```

**2. Update Vite Config:**

Add PWA plugin configuration.

**3. Add Service Worker:**

Copy service worker from full version.

**4. Rebuild:**

```bash
docker-compose -f docker-compose.base.yaml build frontend
docker-compose -f docker-compose.base.yaml up -d
```

---

## 🎯 Migration Path

### Option A: Incremental (Recommended)

1. Start with base version
2. Add features one by one
3. Test after each addition
4. Deploy incrementally

### Option B: Full Migration

1. Copy all files from full version
2. Update dependencies
3. Update environment variables
4. Rebuild and deploy

## 📋 Checklist

- [ ] Email notifications
- [ ] WhatsApp notifications
- [ ] Analytics dashboard
- [ ] Facebook Pixel
- [ ] Shipping classes
- [ ] Redis & Celery
- [ ] PWA support
- [ ] Performance optimization
- [ ] Caching
- [ ] CDN integration

## 🚀 Performance Optimization

### Backend
- Add Redis caching
- Database connection pooling
- Query optimization
- Background task processing

### Frontend
- Code splitting
- Lazy loading
- Image optimization
- CDN for static assets

### Infrastructure
- Load balancing
- Auto-scaling
- Database replication
- CDN integration

## 📝 Notes

- **Scale incrementally** - don't add everything at once
- **Test thoroughly** after each addition
- **Monitor performance** as you scale
- **Keep base version** as backup
- **Document changes** for team

## ✅ Success!

You've scaled from base to full version! Your app now has all features and is production-ready.

