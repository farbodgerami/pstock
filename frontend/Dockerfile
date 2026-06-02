# ---------- builder ----------
FROM node:22-alpine AS builder
WORKDIR /app

# install build dependencies
# use a fixed set of deps to get reproducible builds
COPY package.json package-lock.json ./
RUN npm ci --silent

# copy source and build
COPY . .
RUN npm run build

# ---------- runtime ----------
FROM nginx:1.30.2-alpine AS runtime
# create directory for the app
RUN mkdir -p /usr/share/nginx/html

# copy built files from builder stage
# ensure files are owned by nginx user (uid 101 usually)
COPY --from=builder /app/dist /usr/share/nginx/html

# copy our custom nginx config
COPY nginx/nginx.conf /etc/nginx/conf.d/default.conf

# remove default server signature for security
RUN sed -i 's/server_tokens on;/server_tokens off;/' /etc/nginx/nginx.conf || true

# expose port 80 (and 443 if you later add TLS termination here)
EXPOSE 80

# healthcheck (curl must be installed in image; we rely on builtin wget)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qS --spider http://localhost/ || exit 1

# run as the default nginx user (image already sets user at run-time)
CMD ["nginx", "-g", "daemon off;"]
