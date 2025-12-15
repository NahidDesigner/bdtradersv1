# 🚨 URGENT: Fix Database Password Error

## The Error
```
password authentication failed for user "postgres"
```

Your backend can't connect to the database because the passwords don't match.

## ✅ Quick Fix (Choose ONE method)

### Method 1: Use Individual Variables (Easier - Recommended)

**In Coolify, for `postgres` service, set:**
```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = YourSecurePassword123
POSTGRES_DB = bdtenant
```

**In Coolify, for `backend` service, set:**
```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = YourSecurePassword123  (SAME as postgres service!)
POSTGRES_DB = bdtenant
POSTGRES_HOST = postgres
POSTGRES_PORT = 5432
```

**DO NOT set `DATABASE_URL`** - the backend will build it automatically from the above variables.

### Method 2: Use DATABASE_URL Directly

**In Coolify, for `postgres` service, set:**
```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = YourSecurePassword123
POSTGRES_DB = bdtenant
```

**In Coolify, for `backend` service, set:**
```
DATABASE_URL = postgresql://postgres:YourSecurePassword123@postgres:5432/bdtenant
```

Replace `YourSecurePassword123` with your actual password (same in both places).

## 📋 Step-by-Step in Coolify

1. **Go to your project** → "BD traders V1"
2. **Click on `postgres` service** (or find it in the services list)
3. **Go to "Environment Variables"** tab
4. **Check/Set these:**
   - `POSTGRES_USER` = `postgres`
   - `POSTGRES_PASSWORD` = `[your-password]` (write it down!)
   - `POSTGRES_DB` = `bdtenant`
5. **Save**
6. **Go to `backend` service**
7. **Go to "Environment Variables"** tab
8. **Set these (use SAME password from step 4):**
   - `POSTGRES_USER` = `postgres`
   - `POSTGRES_PASSWORD` = `[same-password-as-step-4]`
   - `POSTGRES_DB` = `bdtenant`
   - `POSTGRES_HOST` = `postgres`
   - `POSTGRES_PORT` = `5432`
9. **If `DATABASE_URL` exists, DELETE it** (or make sure password matches)
10. **Save**
11. **Click "Redeploy"**

## ⚠️ Important

- **Passwords are case-sensitive**
- **No spaces** before/after password
- **Same password** in postgres service AND backend service
- If you use `DATABASE_URL`, the password in the URL must match `POSTGRES_PASSWORD` in postgres service

## 🎯 Example

**Postgres service:**
```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = MyPass123!
POSTGRES_DB = bdtenant
```

**Backend service (Method 1 - Recommended):**
```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = MyPass123!  ← SAME!
POSTGRES_DB = bdtenant
POSTGRES_HOST = postgres
POSTGRES_PORT = 5432
```

**Backend service (Method 2 - Alternative):**
```
DATABASE_URL = postgresql://postgres:MyPass123!@postgres:5432/bdtenant
```

## ✅ After Fixing

1. **Save** all environment variables
2. **Redeploy** the application
3. **Check logs** - should see "Application startup complete"
4. **No more password errors!**

## 🆘 Still Not Working?

1. **Double-check** passwords match exactly (copy-paste to avoid typos)
2. **Try a simple password** first (no special characters) like `testpass123`
3. **Check** if postgres service has `POSTGRES_PASSWORD` set
4. **Verify** backend service has matching password
5. **Look at logs** for any other errors

