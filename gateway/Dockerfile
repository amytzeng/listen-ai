# gateway/Dockerfile
# Containerize the Node.js gateway service.

FROM node:20-alpine

# Create app directory.
WORKDIR /app

# Install dependencies first for better caching.
COPY package.json package-lock.json /app/
RUN npm ci --omit=dev

# Copy application source.
COPY . /app

# Default port from code is 8000.
EXPOSE 8000

# Provide sane defaults for standalone testing. In Docker Compose, you will
# override STAT_URL and NLP_URL to use service names.
ENV GATEWAY_PORT=8000 \
    STAT_URL=http://localhost:8002 \
    NLP_URL=http://localhost:8001 \
    JWT_SECRET=supersecret \
    DEMO_USER=admin \
    DEMO_PASS=admin123

# Start the server.
CMD ["npm", "start"]