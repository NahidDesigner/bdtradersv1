# Bangladesh Multi-Tenant SaaS Platform

Production-ready multi-tenant SaaS application for Bangladesh-based merchants to create product landing pages and receive orders.

## 🚀 Quick Start with Coolify

**The easiest way to deploy is using Coolify!**

1. Push this repository to GitHub
2. In Coolify, create a new Docker Compose resource
3. Connect your GitHub repository
4. Set environment variables (see `COOLIFY_SETUP.md`)
5. Deploy!

**📖 Full Coolify setup guide: [COOLIFY_SETUP.md](./COOLIFY_SETUP.md)**

## Architecture

- **Multi-tenant**: Subdomain-based tenant isolation (e.g., `storename.mysaas.com`)
- **Frontend**: React + Vite + Tailwind CSS + PWA
- **Backend**: FastAPI + PostgreSQL + SQLAlchemy
- **Language**: Bangla-first UI with English toggle

## Features

- ✅ Multi-tenant subdomain isolation
- ✅ OTP-based authentication (Bangladesh phone numbers)
- ✅ Store management
- ✅ Product landing pages
- ✅ Single-page checkout
- ✅ Order management
- ✅ Shipping classes
- ✅ Email & WhatsApp notifications
- ✅ Analytics dashboard
- ✅ Bangla-first UI with i18n
- ✅ PWA support
- ✅ Facebook Pixel integration

## Local Development

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+ (or Docker)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your settings

# Run migrations (optional, tables auto-create)
# alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install

# Copy and configure environment variables
cp .env.example .env
# Edit .env with your settings

# Start dev server
npm run dev
```

### Docker Development

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Variables

### Backend

See `backend/.env.example` for all available variables.

**Required:**
- `SECRET_KEY` - Secret key for encryption (min 32 chars)
- `JWT_SECRET` - JWT signing secret (min 32 chars)
- `DATABASE_URL` - PostgreSQL connection string

**Important for Production:**
- `CORS_ORIGINS` - Comma-separated list of allowed origins
- `BASE_DOMAIN` - Your domain (e.g., `yourdomain.com`)

### Frontend

See `frontend/.env.example` for all available variables.

**Required:**
- `VITE_API_URL` - Backend API URL
- `VITE_BASE_DOMAIN` - Base domain for subdomains

**Note:** Frontend env vars are baked into the build. Change them before building.

## Deployment

### Coolify (Recommended)

See [COOLIFY_SETUP.md](./COOLIFY_SETUP.md) for detailed instructions.

### Manual Docker

1. Configure environment variables
2. Build and run:
   ```bash
   docker-compose up -d --build
   ```

### Other Platforms

The application is Docker-based and can run on:
- Coolify (recommended)
- Railway
- Render
- DigitalOcean App Platform
- AWS ECS
- Google Cloud Run
- Any Docker-compatible platform

## Project Structure

```
.
├── backend/          # FastAPI backend
├── frontend/         # React frontend
├── nginx/           # Nginx config (optional, Coolify uses Traefik)
├── docker-compose.yml
└── README.md
```

## Documentation

- **[COOLIFY_SETUP.md](./COOLIFY_SETUP.md)** - Complete Coolify deployment guide
- **[DEPLOYMENT.md](./DEPLOYMENT.md)** - General deployment instructions
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Technical architecture details
- **[PROJECT_SUMMARY.md](./PROJECT_SUMMARY.md)** - Feature overview

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Health Checks

- Backend: `GET /health` or `GET /api/v1/health`
- Frontend: `GET /` (served by nginx)

## Support

For issues:
1. Check [COOLIFY_SETUP.md](./COOLIFY_SETUP.md) for deployment help
2. Check [ARCHITECTURE.md](./ARCHITECTURE.md) for technical details
3. Review application logs

## License

MIT
