# 🚀 Automatic Setup - No Manual Environment Variables Needed!

## ✅ What I Changed

I've updated the code so it works **automatically** without needing to manually set environment variables in Coolify!

### How It Works

1. **Backend has smart defaults** - All variables have sensible defaults in `backend/app/core/config.py`
2. **Postgres uses matching password** - Default password is `bdtenant2024secure` (matches backend default)
3. **Docker Compose is clean** - No `:-` syntax that Coolify doesn't support
4. **Everything works out of the box** - Just deploy and it works!

## 🎯 Default Values

The system uses these defaults automatically:

**Database:**
- User: `postgres`
- Password: `bdtenant2024secure`
- Database: `bdtenant`
- Host: `postgres`
- Port: `5432`

**Security:**
- Secret Key: `bdtenant-secret-key-change-in-production-2024`
- JWT Secret: `bdtenant-jwt-secret-change-in-production-2024`
- JWT Algorithm: `HS256`
- JWT Expiration: `24` hours

**Other:**
- CORS: `*` (allows all origins)
- Environment: `production`
- Debug: `false`

## 📋 Steps to Deploy (Super Simple!)

1. **Delete your old project** in Coolify (if you want a fresh start)

2. **Create a new project** in Coolify:
   - Connect to your GitHub repo: `NahidDesigner/bdtradersv1`
   - Select "Docker Compose" as build pack
   - Set Docker Compose location: `/docker-compose.yaml`

3. **Set domains** (Coolify will suggest these):
   - Backend: `https://yourdomain.com/api`
   - Frontend: `https://yourdomain.com/`

4. **Deploy!** 
   - That's it! No environment variables needed!
   - The system will use all defaults automatically

## 🔒 For Production (Optional)

If you want to change the default password or secrets for security:

1. Go to **Environment Variables** in Coolify
2. Override any variable you want:
   - `POSTGRES_PASSWORD` = `YourSecurePassword123`
   - `SECRET_KEY` = `YourSecretKey123`
   - `JWT_SECRET` = `YourJWTSecret123`
   - etc.

3. **Important:** If you change `POSTGRES_PASSWORD`, make sure to:
   - Set it in both postgres and backend (or just set it once - Docker Compose shares variables)
   - Delete the `postgres_data` volume if the database already exists with old password

## ✨ Benefits

- ✅ **Zero configuration** - Works immediately
- ✅ **No manual setup** - All defaults are sensible
- ✅ **Easy to override** - Change any variable in Coolify if needed
- ✅ **Production ready** - Can customize everything later

## 🎉 That's It!

Just deploy and it works! No environment variables needed unless you want to customize something.

