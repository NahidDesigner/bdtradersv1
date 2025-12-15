# Root Dockerfile for Coolify
# This is a fallback - Coolify should use docker-compose.yml instead
# If you see this, configure Coolify to use Docker Compose mode

FROM alpine:latest

RUN echo "This project uses Docker Compose. Please configure Coolify to use docker-compose.yml instead of this Dockerfile." && \
    echo "In Coolify, select 'Docker Compose' as the deployment type, not 'Dockerfile'."

WORKDIR /app

CMD ["echo", "Please use docker-compose.yml for deployment"]

