# Coolify Setup Guide

This guide will help you deploy the BD Tenant SaaS platform to Coolify quickly and easily.

## Prerequisites

1. Coolify instance running (v3+)
2. A domain with wildcard DNS configured
3. GitHub repository (public or connected to Coolify)

## Quick Setup Steps

### 1. Prepare Your Repository

Ensure your repository has:
- ✅ `docker-compose.yml` in the root
- ✅ `backend/Dockerfile`
- ✅ `frontend/Dockerfile`
- ✅ All source code

### 2. Create New Resource in Coolify

1. Go to your Coolify dashboard
2. Click "New Resource"
3. Select "Docker Compose"
4. Connect your GitHub repository
5. Select the repository and branch

### 3. Configure Environment Variables

Coolify will automatically detect your services. Set these environment variables:

#### Backend Service

**Required:**
```bash
SECRET_KEY=your-secret-key-min-32-characters-long
JWT_SECRET=your-jwt-secret-min-32-characters-long
```

**Database (choose one):**

Option A - Use Coolify's Database Service:
```bash
DATABASE_URL=<provided-by-coolify-database-service>
```

Option B - Use Docker Compose PostgreSQL:
```bash
POSTGRES_DB=bdtenant
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
```

**CORS (Important for subdomains):**
```bash
CORS_ORIGINS=https://yourdomain.com,https://*.yourdomain.com,https://app.yourdomain.com
BASE_DOMAIN=yourdomain.com
```

**Optional (Email, WhatsApp, etc.):**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

#### Frontend Service

**Required:**
```bash
VITE_API_URL=https://api.yourdomain.com
# OR if backend is on same domain:
VITE_API_URL=https://yourdomain.com/api
VITE_BASE_DOMAIN=yourdomain.com
```

**Note:** Frontend environment variables are baked into the build at build time. If you change them, you need to rebuild.

### 4. Configure Domain & Subdomains

#### Main App Domain
- Set domain for `frontend` service: `app.yourdomain.com`
- Set domain for `backend` service: `api.yourdomain.com` (optional, or use same domain with `/api` path)

#### Wildcard Subdomain Setup

Coolify supports wildcard subdomains. Configure:

1. In your DNS provider, add:
   ```
   *.yourdomain.com  A  <coolify-server-ip>
   yourdomain.com    A  <coolify-server-ip>
   ```

2. In Coolify, for the frontend service:
   - Add domain: `*.yourdomain.com`
   - Coolify will automatically handle wildcard routing

### 5. Database Setup

**Option A: Use Coolify Database Service (Recommended)**

1. Create a new PostgreSQL database in Coolify
2. Copy the connection string
3. Set `DATABASE_URL` environment variable in backend service
4. Remove `postgres` service from docker-compose.yml (or keep it for local dev)

**Option B: Use Docker Compose PostgreSQL**

1. Keep `postgres` service in docker-compose.yml
2. Set `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`
3. Tables will auto-create on first startup

### 6. Build & Deploy

1. Click "Deploy" in Coolify
2. Coolify will:
   - Build Docker images
   - Start services
   - Run health checks
   - Expose services

### 7. Verify Deployment

1. **Health Check**: Visit `https://api.yourdomain.com/health` (or your backend URL)
   - Should return: `{"status": "healthy"}`

2. **Frontend**: Visit `https://app.yourdomain.com`
   - Should show login page

3. **Test Subdomain**: Create a store with slug `teststore`
   - Visit `https://teststore.yourdomain.com`
   - Should show tenant store (or 404 if tenant doesn't exist)

## Important Configuration Notes

### Frontend Build Variables

Frontend environment variables (`VITE_*`) are **baked into the build** at build time. This means:

- If you change `VITE_API_URL`, you must **rebuild** the frontend
- Coolify will rebuild on every deploy, so set these correctly before first deploy

### CORS Configuration

For subdomain-based multi-tenancy, CORS must allow all subdomains:

```bash
CORS_ORIGINS=https://yourdomain.com,https://*.yourdomain.com,https://app.yourdomain.com
```

Or use wildcard (less secure, but works):
```bash
CORS_ORIGINS=*
```

### Database Connection

If using Coolify's managed database:
- The `DATABASE_URL` will be provided automatically
- Make sure to use the full connection string
- Format: `postgresql://user:password@host:port/database`

### Health Checks

Both services have health check endpoints:
- Backend: `/health` (returns `{"status": "healthy"}`)
- Frontend: `/` (nginx serves index.html)

Coolify will automatically monitor these.

## Troubleshooting

### Subdomain Not Working

1. **Check DNS**: Verify wildcard DNS is configured
   ```bash
   dig teststore.yourdomain.com
   ```

2. **Check Coolify Domain**: Ensure wildcard domain is added in Coolify

3. **Check Nginx/Reverse Proxy**: Coolify handles this automatically, but verify routing

### Frontend Can't Connect to Backend

1. **Check VITE_API_URL**: Must match your backend URL
2. **Check CORS**: Backend must allow frontend origin
3. **Check Network**: Services must be on same network (Coolify handles this)

### Database Connection Failed

1. **Check DATABASE_URL**: Verify connection string is correct
2. **Check Network**: Database must be accessible from backend
3. **Check Credentials**: Verify username/password

### Build Fails

1. **Check Dockerfile**: Ensure paths are correct
2. **Check Dependencies**: Verify package.json and requirements.txt
3. **Check Build Logs**: Coolify shows detailed build logs

## Production Checklist

- [ ] Environment variables set
- [ ] Database configured and accessible
- [ ] DNS configured (wildcard + main domain)
- [ ] SSL certificates active (Coolify auto-provisions)
- [ ] CORS configured correctly
- [ ] Health checks passing
- [ ] Test subdomain working
- [ ] Email service configured (if using)
- [ ] WhatsApp service configured (if using)
- [ ] OTP service configured (if using)
- [ ] Backups configured (for database)

## Advanced: Custom Nginx Configuration

If you need custom nginx configuration for subdomain routing:

1. Coolify uses Traefik as reverse proxy by default
2. For custom routing, you can:
   - Use Coolify's domain labels
   - Or deploy a custom nginx service (not recommended)

## Support

If you encounter issues:

1. Check Coolify logs for each service
2. Verify environment variables are set correctly
3. Check DNS propagation
4. Verify database connectivity
5. Review application logs in Coolify

## Quick Reference

**Backend Health Check:**
```
GET https://api.yourdomain.com/health
```

**Frontend:**
```
https://app.yourdomain.com
```

**Tenant Store:**
```
https://storename.yourdomain.com
```

**API Base:**
```
https://api.yourdomain.com/api/v1
```

