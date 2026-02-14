# Task T-205: Next.js frontend Docker image (multi-stage build)

FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package.json package-lock.json* yarn.lock* ./

# Task T-205: Install dependencies
RUN if [ -f yarn.lock ]; then yarn --frozen-lockfile; else npm ci; fi

# Copy source code
COPY . .

# Task T-205: Build Next.js app
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=production

# Copy only necessary files from builder
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/package.json ./package.json
COPY --from=builder /app/public ./public

# Task T-205: Expose port 3000
EXPOSE 3000

# Task T-205: Start Next.js server
CMD ["npm", "run", "start"]
