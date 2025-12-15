# 🔐 Fix Database Password Authentication Error

## The Problem

Your backend is getting this error:
```
password authentication failed for user "postgres"
```

This means the password in your `DATABASE_URL` or `POSTGRES_PASSWORD` doesn't match the password set for the PostgreSQL service.

## ✅ Solution: Synchronize Passwords

You need to make sure **all three places** have the **SAME password**:

1. **Postgres service** - `POSTGRES_PASSWORD` environment variable
2. **Backend service** - `POSTGRES_PASSWORD` environment variable  
3. **Backend service** - `DATABASE_URL` (the password in the connection string)

## 🔧 Step-by-Step Fix

### Option 1: Use the Same Password Everywhere (Recommended)

1. **Choose ONE password** (e.g., `MySecurePassword123!`)

2. **In Coolify, for `postgres` service:**
   - Set `POSTGRES_PASSWORD` = `MySecurePassword123!`

3. **In Coolify, for `backend` service:**
   - Set `POSTGRES_PASSWORD` = `MySecurePassword123!` (same password)
   - Set `DATABASE_URL` = `postgresql://postgres:MySecurePassword123!@postgres:5432/bdtenant`
     - Replace `MySecurePassword123!` with your actual password

4. **Save and Redeploy**

### Option 2: Check Current Values

1. **In Coolify, check `postgres` service:**
   - Look at `POSTGRES_PASSWORD` value
   - Write it down (or reveal it)

2. **In Coolify, check `backend` service:**
   - Check `POSTGRES_PASSWORD` - should match postgres service
   - Check `DATABASE_URL` - the password in the URL should match

3. **If they don't match:**
   - Update them to all use the same password
   - Redeploy

## 📋 Quick Checklist

Make sure these match:

- [ ] `postgres` service → `POSTGRES_PASSWORD` = `your-password`
- [ ] `backend` service → `POSTGRES_PASSWORD` = `your-password` (same!)
- [ ] `backend` service → `DATABASE_URL` = `postgresql://postgres:your-password@postgres:5432/bdtenant`

**All three must have the SAME password!**

## 🎯 Example

If your password is `SecurePass123!`:

**Postgres service:**
```
POSTGRES_PASSWORD = SecurePass123!
```

**Backend service:**
```
POSTGRES_PASSWORD = SecurePass123!
DATABASE_URL = postgresql://postgres:SecurePass123!@postgres:5432/bdtenant
```

## ⚠️ Important Notes

- Passwords are case-sensitive
- No spaces before/after the password
- Special characters in passwords might need URL encoding in DATABASE_URL
- If password has special characters, you might need to URL-encode them in DATABASE_URL

## 🚀 After Fixing

1. Save all environment variables
2. Click **"Redeploy"**
3. Backend should connect to database successfully
4. Check logs - should see "Application startup complete"

## 🆘 If Still Failing

1. **Double-check** all three passwords match exactly
2. **Try a simple password** first (no special characters) to test
3. **Check logs** for any other errors
4. **Verify** postgres service is running (it is, based on your logs)

