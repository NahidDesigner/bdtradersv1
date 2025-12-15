FROM node:18-alpine as builder

WORKDIR /app

# Build arguments for environment variables
ARG VITE_API_URL=http://localhost:8000
ARG VITE_BASE_DOMAIN=localhost

# Set environment variables for build
ENV VITE_API_URL=$VITE_API_URL
ENV VITE_BASE_DOMAIN=$VITE_BASE_DOMAIN

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application (environment variables are baked in at build time)
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Add health check script
RUN echo '#!/bin/sh' > /healthcheck.sh && \
    echo 'wget --quiet --tries=1 --spider http://localhost/ || exit 1' >> /healthcheck.sh && \
    chmod +x /healthcheck.sh

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]

