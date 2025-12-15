# 🚀 Quick Start: Deploy to Coolify in 5 Minutes

## Step 1: Push to GitHub
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

## Step 2: Create Resource in Coolify

1. Open Coolify dashboard
2. Click **"New Resource"**
3. Select **"Docker Compose"**
4. Connect your GitHub repository
5. Select repository and branch

## Step 3: Set Environment Variables

### Backend Service

**Required (minimum):**
```bash
SECRET_KEY=generate-a-random-32-character-string-here
JWT_SECRET=generate-another-random-32-character-string-here
DATABASE_URL=postgresql://user:pass@postgres:5432/bdtenant
CORS_ORIGINS=*
BASE_DOMAIN=yourdomain.com
```

**Optional (for email notifications):**
```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
```

### Frontend Service

```bash
VITE_API_URL=https://api.yourdomain.com
# OR if backend is on same domain:
VITE_API_URL=https://yourdomain.com/api
VITE_BASE_DOMAIN=yourdomain.com
```

## Step 4: Configure Domains

1. **Frontend**: Set domain to `app.yourdomain.com` (or your main domain)
2. **Backend**: Set domain to `api.yourdomain.com` (optional, or use `/api` path)

### For Wildcard Subdomains (Tenant Stores)

1. In DNS, add: `*.yourdomain.com A <coolify-ip>`
2. In Coolify frontend service, add domain: `*.yourdomain.com`

## Step 5: Deploy!

Click **"Deploy"** and wait for build to complete.

## Step 6: Verify

1. Visit `https://app.yourdomain.com` - Should show login page
2. Visit `https://api.yourdomain.com/health` - Should return `{"status": "healthy"}`

## That's It! 🎉

Your application is now live. 

**Next Steps:**
1. Register a user account
2. Create your first store
3. Add products
4. Test the checkout flow

## Troubleshooting

**Build fails?**
- Check environment variables are set
- Verify Dockerfile paths are correct

**Can't connect to backend?**
- Check `VITE_API_URL` matches your backend URL
- Verify CORS_ORIGINS includes your frontend domain

**Database connection error?**
- Verify DATABASE_URL is correct
- Check database service is running
- Verify network connectivity

**Need more help?**
See [COOLIFY_SETUP.md](./COOLIFY_SETUP.md) for detailed instructions.

