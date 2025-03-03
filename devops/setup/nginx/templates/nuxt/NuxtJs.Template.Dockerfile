# Build stage
FROM node:lts-alpine AS builder

WORKDIR /app

# Add build arguments for environment variables
ARG NODE_ENV=production
ARG BASE_URL=/ui/

# Set environment variables
ENV NODE_ENV=${NODE_ENV}
ENV BASE_URL=${BASE_URL}
ENV NUXT_APP_BASE_URL=${BASE_URL}

# TODO: APP_FOLDER
COPY front_end/APP_FOLDER/package*.json ./
RUN npm ci && npm cache clean --force

COPY front_end/APP_FOLDER/ ./
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

# Create ecosystem.config.cjs (copy from other app)
# npm run build
