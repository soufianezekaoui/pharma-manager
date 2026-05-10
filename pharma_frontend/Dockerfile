# ── Stage 1: Builder ──────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package.json only (no lock file — it was out of sync)
COPY package.json ./

# Install deps fresh — generates a correct lock file inside the container
RUN npm install

# Copy source and build
COPY . .
RUN npm run build

# ── Stage 2: Production server (nginx) ───────────────────────────────────────
FROM nginx:1.27-alpine AS runtime

# Remove default nginx page
RUN rm -rf /usr/share/nginx/html/*

# Copy built React app from builder
COPY --from=builder /app/dist /usr/share/nginx/html

# SPA routing + API proxy config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
