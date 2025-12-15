# 🔧 Fix: Connection Refused Error

## The Problem

The backend is getting "Connection refused" when trying to connect to postgres. This usually means:
1. `POSTGRES_HOST` is not set or is wrong
2. Backend is starting before postgres is fully ready

## ✅ Quick Fix

### Step 1: Set POSTGRES_HOST in Coolify

Go to **Environment Variables** in Coolify and make sure you have:

```
POSTGRES_HOST = postgres
```

**Important:** The value must be exactly `postgres` (the Docker service name), not `localhost` or anything else.

### Step 2: Verify Other Database Variables

Make sure these are set (or use defaults):

```
POSTGRES_USER = postgres
POSTGRES_PASSWORD = bdtenant2024secure
POSTGRES_DB = bdtenant
POSTGRES_PORT = 5432
POSTGRES_HOST = postgres  ← This is the key one!
```

### Step 3: Redeploy

After setting `POSTGRES_HOST = postgres`, redeploy the application.

## 🔍 What I Fixed in the Code

1. **Added retry logic** - Backend now retries connection up to 10 times with exponential backoff
2. **Default POSTGRES_HOST** - If not set, defaults to `postgres` (the service name)
3. **Better error messages** - More helpful logging to debug connection issues

## 📋 Complete Environment Variables Checklist

Make sure these are set in Coolify:

**Required:**
- [ ] `POSTGRES_PASSWORD` = `bdtenant2024secure` (or your password)
- [ ] `POSTGRES_HOST` = `postgres` ← **This is critical!**

**Optional (have defaults):**
- `POSTGRES_USER` = `postgres` (default)
- `POSTGRES_DB` = `bdtenant` (default)
- `POSTGRES_PORT` = `5432` (default)

## 🎯 Why POSTGRES_HOST Must Be "postgres"

In Docker Compose, services communicate using their **service names** as hostnames. Since your postgres service is named `postgres` in `docker-compose.yaml`, the backend must connect to `postgres`, not `localhost`.

## ✅ After Fixing

1. Set `POSTGRES_HOST = postgres` in Coolify
2. Redeploy
3. Check logs - should see "Database connection successful!"

The retry logic will handle any timing issues, and the default ensures it works even if you forget to set it.

