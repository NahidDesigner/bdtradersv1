# ⚡ QUICK FIX - Do This Now

## 🎯 The 3 Critical Steps

### 1. Add DNS Records in Cloudflare (2 minutes)

**Cloudflare Dashboard → DNS → Add Record:**

```
Type: A
Name: bdtraders
Content: 72.61.239.193
Proxy: ON
```

```
Type: A
Name: api.bdtraders
Content: 72.61.239.193
Proxy: ON
```

**Then:** SSL/TLS → Encryption mode: **"Full"**

### 2. Set Environment Variables in Coolify (3 minutes)

**Coolify → Your Project → Environment Variables**

**Backend service:**
```
CORS_ORIGINS=https://bdtraders.vibecodingfield.com,https://api.bdtraders.vibecodingfield.com,https://*.bdtraders.vibecodingfield.com
BASE_DOMAIN=bdtraders.vibecodingfield.com
```

**Frontend service:**
```
VITE_API_URL=https://api.bdtraders.vibecodingfield.com
VITE_BASE_DOMAIN=bdtraders.vibecodingfield.com
```

### 3. Redeploy (1 minute)

**Coolify → Your Project → Click "Redeploy"**

**Wait 2-3 minutes for DNS + deployment**

## ✅ Test

- `https://bdtraders.vibecodingfield.com` → Should show your app
- `https://api.bdtraders.vibecodingfield.com` → Should show API JSON

**That's it!** 🎉

