# Build stage
FROM node:lts-alpine AS builder

WORKDIR /app

COPY front_end/Chatbot/package*.json ./
RUN npm ci && npm cache clean --force

COPY front_end/Chatbot/ ./
RUN npm run build

# Runtime stage
FROM node:lts-alpine

WORKDIR /app

# Install PM2 globally
RUN npm install -g pm2 && npm cache clean --force

# Copy built app and necessary files from builder stage
COPY --from=builder /app/.output /app/.output
COPY --from=builder /app/ecosystem.config.cjs ./ecosystem.config.cjs

# Create a non-root user and switch to it
RUN addgroup -g 1001 -S nodejs && adduser -S nuxtjs -u 1001 && \
    chown -R nuxtjs:nodejs /app
USER nuxtjs

EXPOSE 3000

CMD ["pm2-runtime", "start", "ecosystem.config.cjs"]