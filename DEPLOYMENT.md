# General Deployment Guide

> **For Coolify-specific instructions, see [COOLIFY_SETUP.md](./COOLIFY_SETUP.md)**

This guide covers general deployment instructions for various platforms.

This guide explains how to deploy the BD Tenant SaaS platform to Coolify.

## Prerequisites

1. A Coolify instance running
2. A domain with wildcard DNS configured
3. PostgreSQL database (can be provisioned via Coolify)
4. SMTP credentials (for email notifications)
5. WhatsApp API credentials (optional)
6. OTP provider credentials (optional)

## Step 1: Configure DNS

Set up wildcard DNS for your domain:

```
*.yourdomain.com  A  <your-server-ip>
yourdomain.com    A  <your-server-ip>
```

This allows subdomains like:
- `app.yourdomain.com` - Main application
- `storename.yourdomain.com` - Tenant stores

## Step 2: Prepare GitHub Repository

1. Push your code to a public GitHub repository
2. Ensure all environment variables are documented in `.env.example` files

## Step 3: Deploy in Coolify

### Create New Project

1. In Coolify, create a new project
2. Select "Docker Compose" as the deployment type
3. Connect your GitHub repository

### Configure Environment Variables

Set the following environment variables in Coolify:

#### Backend Variables

```bash
DATABASE_URL=postgresql://user:password@postgres:5432/bdtenant
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET=your-jwt-secret-min-32-chars
CORS_ORIGINS=https://yourdomain.com,https://*.yourdomain.com
BASE_DOMAIN=yourdomain.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=noreply@yourdomain.com
```

#### Frontend Variables

```bash
VITE_API_URL=https://api.yourdomain.com
VITE_BASE_DOMAIN=yourdomain.com
```

### Configure Docker Compose

Coolify will automatically detect `docker-compose.yml`. Ensure:

1. PostgreSQL service is configured
2. Backend service has correct environment variables
3. Frontend service has correct environment variables
4. Nginx service is configured for reverse proxy

### Update Nginx Configuration

Update `nginx/nginx.conf` with your actual domain:

```nginx
server_name app.*;
server_name ~^(?<subdomain>.+)\.yourdomain\.com$;
```

## Step 4: Database Setup

The application will automatically create tables on first startup. Alternatively:

1. Connect to PostgreSQL container
2. Run migrations manually (if using Alembic)

## Step 5: SSL/HTTPS Setup

Coolify can automatically provision SSL certificates via Let's Encrypt:

1. Enable SSL in Coolify settings
2. Configure domain verification
3. SSL certificates will be auto-renewed

## Step 6: Verify Deployment

1. Visit `https://app.yourdomain.com` - Should show main app
2. Create a test store with slug `teststore`
3. Visit `https://teststore.yourdomain.com` - Should show tenant store
4. Test OTP login
5. Create a product
6. Test checkout flow

## Step 7: Configure Services

### Email Service

Update SMTP settings in store settings or environment variables.

### WhatsApp Service

Configure WhatsApp API credentials in environment variables or store settings.

### OTP Service

Configure OTP provider (Twilio, local SMS gateway, etc.) in environment variables.

## Troubleshooting

### Subdomain Not Working

1. Check DNS propagation: `dig teststore.yourdomain.com`
2. Verify Nginx configuration
3. Check Coolify reverse proxy settings
4. Ensure wildcard DNS is configured correctly

### Database Connection Issues

1. Verify `DATABASE_URL` is correct
2. Check PostgreSQL container is running
3. Verify network connectivity between containers

### CORS Errors

1. Update `CORS_ORIGINS` in backend environment variables
2. Include all subdomains: `https://*.yourdomain.com`

### Tenant Not Found

1. Verify tenant slug matches subdomain
2. Check tenant is active in database
3. Verify middleware is extracting subdomain correctly

## Production Checklist

- [ ] SSL certificates configured
- [ ] Environment variables set
- [ ] Database backups configured
- [ ] Email service tested
- [ ] WhatsApp service tested (if enabled)
- [ ] OTP service tested
- [ ] Facebook Pixel configured (if needed)
- [ ] Monitoring/logging set up
- [ ] Rate limiting configured
- [ ] File upload limits set
- [ ] CORS properly configured

## Scaling Considerations

For production scaling:

1. Use managed PostgreSQL (AWS RDS, DigitalOcean, etc.)
2. Use Redis for session/OTP storage
3. Configure Celery workers for background tasks
4. Use CDN for static assets
5. Implement database connection pooling
6. Use load balancer for multiple backend instances

## Support

For issues, check:
- Application logs in Coolify
- Nginx access/error logs
- Backend logs
- Database logs

