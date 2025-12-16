# ⚡ Quick Start - Base Version

## 🚀 Get Running in 2 Minutes!

### Step 1: Start Services

```bash
# Using base Docker Compose
docker-compose -f docker-compose.base.yaml up -d
```

**That's it!** The base version uses auto-configuration - no setup needed!

### Step 2: Access the App

**Frontend:**
```
http://localhost
```

**Backend API:**
```
http://localhost:8000
```

**API Documentation:**
```
http://localhost:8000/docs
```

### Step 3: Test It

1. **Register a new user:**
   - Go to frontend
   - Click "Register"
   - Enter phone number
   - Get OTP (check backend logs for OTP in dev mode)

2. **Create a store:**
   - After login, create your first store
   - Set store name and slug

3. **Add a product:**
   - Go to Products page
   - Add a product with image, price, description

4. **View landing page:**
   - Visit: `http://localhost/product/{product-slug}`
   - See your product landing page

5. **Test checkout:**
   - Add to cart
   - Fill checkout form
   - Place order

## 🎯 What's Working

✅ User authentication (OTP + JWT)  
✅ Store management  
✅ Product management  
✅ Order management  
✅ Product landing pages  
✅ Checkout system  
✅ Multi-tenant support  

## 📝 Default Credentials

**Database:**
- User: `postgres`
- Password: `bdtenant2024secure`
- Database: `bdtenant`

**Change in production!**

## 🔧 Customization

### Change Database Password

```bash
# Set environment variable
export POSTGRES_PASSWORD=your-secure-password

# Restart
docker-compose -f docker-compose.base.yaml down
docker-compose -f docker-compose.base.yaml up -d
```

### Change API URL (Frontend)

```bash
# Set environment variable
export VITE_API_URL=http://your-backend-url:8000

# Rebuild frontend
docker-compose -f docker-compose.base.yaml build frontend
docker-compose -f docker-compose.base.yaml up -d frontend
```

## 📊 View Logs

```bash
# All services
docker-compose -f docker-compose.base.yaml logs -f

# Specific service
docker-compose -f docker-compose.base.yaml logs -f backend
docker-compose -f docker-compose.base.yaml logs -f frontend
docker-compose -f docker-compose.base.yaml logs -f postgres
```

## 🛑 Stop Services

```bash
docker-compose -f docker-compose.base.yaml down
```

## 🗑️ Remove Everything (Including Data)

```bash
docker-compose -f docker-compose.base.yaml down -v
```

## ✅ Success!

Your base version is running! Now you can:
- Test all features
- Customize as needed
- Scale by following `SCALING_GUIDE.md`

## 🚀 Next Steps

1. **Test the app** - Make sure everything works
2. **Customize** - Change branding, colors, etc.
3. **Scale** - Add features from `SCALING_GUIDE.md`
4. **Deploy** - Deploy to Coolify or your server

## 📖 More Info

- **Full documentation:** `BASE_VERSION_README.md`
- **Scaling guide:** `SCALING_GUIDE.md`
- **Architecture:** `ARCHITECTURE.md`

