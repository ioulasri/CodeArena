FROM node:18-alpine AS build

WORKDIR /app

# Accept build argument for API URL
ARG REACT_APP_API_URL=http://localhost:8000
ENV REACT_APP_API_URL=$REACT_APP_API_URL

# Install dependencies
COPY frontend/package*.json ./
RUN npm install

# Copy application code
COPY frontend/ .

# Build the application with environment variable injected
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built assets from build stage
COPY --from=build /app/build /usr/share/nginx/html

# Copy nginx configuration
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
