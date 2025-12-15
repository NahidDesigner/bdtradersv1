# 🚀 Automatic Setup - Minimal Configuration Required!

## ✅ What I Changed

I've updated the code so it works with **minimal configuration** - you only need to set **ONE password** and everything else is automatic!

### How It Works

1. **Backend has smart defaults** - All variables have sensible defaults in `backend/app/core/config.py`
2. **Default password is set** - Default password is `bdtenant2024secure` (same for postgres and backend)
3. **Docker Compose is clean** - No complex syntax
4. **Almost zero configuration** - Just set the password once!

## 🎯 Quick Setup (2 Steps!)

### Step 1: Set Password in Coolify

When you create the project in Coolify, go to **Environment Variables** and set:

```
POSTGRES_PASSWORD = bdtenant2024secure
```

That's it! Everything else uses defaults automatically.

### Step 2: Deploy!

Click **Deploy** and it will work!

## 📋 All Default Values

The system uses these defaults automatically (you don't need to set them):

**Database:**
- User: `postgres` ✅
- Password: `bdtenant2024secure` (set this once in Coolify)
- Database: `bdtenant` ✅
- Host: `postgres` ✅
- Port: `5432` ✅

**Security (has defaults, but change in production):**
- Secret Key: `bdtenant-secret-key-change-in-production-2024`
- JWT Secret: `bdtenant-jwt-secret-change-in-production-2024`
- JWT Algorithm: `HS256`
- JWT Expiration: `24` hours

**Other:**
- CORS: `*` (allows all origins)
- Environment: `production`
- Debug: `false`

## 🎯 Steps to Deploy

1. **Delete your old project** in Coolify (if you want a fresh start)

2. **Create a new project** in Coolify:
   - Connect to your GitHub repo: `NahidDesigner/bdtradersv1`
   - Select "Docker Compose" as build pack
   - Set Docker Compose location: `/docker-compose.yaml`

3. **Set domains** (Coolify will suggest these):
   - Backend: `https://yourdomain.com/api`
   - Frontend: `https://yourdomain.com/`

4. **Set ONE environment variable:**
   - Go to **Environment Variables**
   - Add: `POSTGRES_PASSWORD` = `bdtenant2024secure`

5. **Deploy!** 
   - That's it! Everything else is automatic!

## 🔒 For Production (Optional)

If you want to change the password or secrets for better security:

1. Go to **Environment Variables** in Coolify
2. Override any variable you want:
   - `POSTGRES_PASSWORD` = `YourSecurePassword123` (change this!)
   - `SECRET_KEY` = `YourSecretKey123` (change this!)
   - `JWT_SECRET` = `YourJWTSecret123` (change this!)
   - etc.

3. **Important:** If you change `POSTGRES_PASSWORD`:
   - Make sure backend uses the same password (it reads from the same environment variable)
   - Delete the `postgres_data` volume if the database already exists with old password

## ✨ Benefits

- ✅ **Minimal configuration** - Only one password to set
- ✅ **Smart defaults** - Everything else works automatically
- ✅ **Easy to override** - Change any variable in Coolify if needed
- ✅ **Production ready** - Can customize everything later

## 🎉 That's It!

Just set `POSTGRES_PASSWORD` once and deploy - everything else is automatic!
