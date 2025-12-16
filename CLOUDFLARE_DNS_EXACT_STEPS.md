# 🎯 Cloudflare DNS - Exact Steps to Fix

## ⚠️ The Problem

Your browser shows `DNS_PROBE_FINISHED_NXDOMAIN` which means **DNS isn't resolving**. The records might exist in Cloudflare, but they're not working.

## ✅ Step-by-Step Fix

### Step 1: Go to Cloudflare DNS

1. **Login to Cloudflare**
2. **Click on domain:** `vibecodingfield.com`
3. **Click:** `DNS` (left sidebar)
4. **Click:** `Records` tab

### Step 2: Delete and Recreate Records

**If records exist, DELETE them first, then recreate:**

#### Record 1: Frontend Domain

1. **Click:** `Add record` button
2. **Type:** Select `A`
3. **Name:** Type `bdtraders` (just this, nothing else)
4. **IPv4 address:** Type `72.61.239.193`
5. **Proxy status:** Click to make it **orange cloud** (Proxied) ✅
6. **TTL:** Leave as `Auto`
7. **Click:** `Save`

#### Record 2: Backend Domain

1. **Click:** `Add record` button
2. **Type:** Select `A`
3. **Name:** Type `api.bdtraders` (just this, nothing else)
4. **IPv4 address:** Type `72.61.239.193`
5. **Proxy status:** Click to make it **orange cloud** (Proxied) ✅
6. **TTL:** Leave as `Auto`
7. **Click:** `Save`

### Step 3: Verify Records

**You should now see:**

- `bdtraders` → `72.61.239.193` → **Proxied** (orange cloud)
- `api.bdtraders` → `72.61.239.193` → **Proxied** (orange cloud)

**If you see gray cloud (DNS only), click it to make it orange (Proxied)!**

### Step 4: Check SSL/TLS

1. **Click:** `SSL/TLS` (left sidebar)
2. **Encryption mode:** Select `Full` or `Full (strict)`
3. **Save**

### Step 5: Purge Cache

1. **Click:** `Caching` (left sidebar)
2. **Click:** `Configuration` tab
3. **Click:** `Purge Everything` button
4. **Confirm**

### Step 6: Wait and Test

1. **Wait 3-5 minutes**
2. **Test DNS:**
   - Go to: https://dnschecker.org
   - Type: `api.bdtraders.vibecodingfield.com`
   - Should show: `72.61.239.193`

3. **Test in browser:**
   - Visit: `https://api.bdtraders.vibecodingfield.com`
   - Should NOT show DNS error
   - Might show "no available server" (that's OK - means DNS works!)

## 🚨 Common Mistakes

❌ **Wrong:** Name = `bdtraders.vibecodingfield.com`  
✅ **Right:** Name = `bdtraders`

❌ **Wrong:** Proxy = Gray cloud (DNS only)  
✅ **Right:** Proxy = Orange cloud (Proxied)

❌ **Wrong:** SSL/TLS = Flexible  
✅ **Right:** SSL/TLS = Full or Full (strict)

## 📸 After Fixing

**Send me screenshot of:**
1. Cloudflare DNS Records (showing the 2 records)
2. What you see when visiting `https://api.bdtraders.vibecodingfield.com`

**This will tell us if DNS is fixed!**

