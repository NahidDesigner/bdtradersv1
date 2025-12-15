# 🔧 Fix: "Role root does not exist" Error

## The Problem

The backend is trying to connect to postgres with user "root", but postgres doesn't have a "root" user. The default user is "postgres".

**Error:**
```
password authentication failed for user "root"
Role "root" does not exist.
```

## ✅ Quick Fix

### Step 1: Check POSTGRES_USER in Coolify

Go to **Environment Variables** in Coolify and check:

1. **If `POSTGRES_USER` is set to "root":**
   - Change it to: `postgres`
   - Or **delete it** (the backend will use the default "postgres")

2. **If `POSTGRES_USER` is not set:**
   - The backend will now automatically use "postgres" (I fixed this in the code)

### Step 2: Verify All Database Variables

Make sure these are set correctly:

```
POSTGRES_USER = postgres        ← Must be "postgres", not "root"!
POSTGRES_PASSWORD = bdtenant2024secure
POSTGRES_DB = bdtenant
POSTGRES_HOST = postgres
POSTGRES_PORT = 5432
```

### Step 3: Redeploy

After fixing `POSTGRES_USER`, redeploy the application.

## 🔍 What I Fixed in the Code

I updated the backend to:
1. **Auto-correct "root" to "postgres"** - If POSTGRES_USER is "root", it automatically changes to "postgres"
2. **Default to "postgres"** - If POSTGRES_USER is empty or not set, defaults to "postgres"
3. **Better validation** - Ensures the user is always "postgres"

## 📋 Complete Environment Variables Checklist

**Required:**
- [ ] `POSTGRES_USER` = `postgres` (NOT "root"!)
- [ ] `POSTGRES_PASSWORD` = `bdtenant2024secure` (or your password)
- [ ] `POSTGRES_HOST` = `postgres`

**Optional (have defaults):**
- `POSTGRES_DB` = `bdtenant` (default)
- `POSTGRES_PORT` = `5432` (default)

## 🎯 Why This Happened

PostgreSQL doesn't have a "root" user like Linux. The default superuser is **"postgres"**. If `POSTGRES_USER` was set to "root" in Coolify, it would try to connect with that user, which doesn't exist.

## ✅ After Fixing

1. Set `POSTGRES_USER = postgres` in Coolify (or delete it to use default)
2. Redeploy
3. Check logs - should see "Database connection successful!" with user "postgres"

The code now automatically fixes this, but it's better to set it correctly in Coolify.

