#!/bin/bash
# Build script for Coolify (if needed)
# This is a fallback - Coolify should use docker-compose.yml directly

echo "Building BD Tenant SaaS Platform..."

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
    echo "ERROR: docker-compose.yml not found!"
    exit 1
fi

# Build using docker-compose
docker-compose build

if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
else
    echo "❌ Build failed!"
    exit 1
fi

