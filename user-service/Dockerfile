# user-service/Dockerfile
FROM node:18-alpine

# Create app directory
WORKDIR /usr/src/app

# Copies package.json and installs dependencies
COPY package.json ./
RUN npm install

# Copy source code
COPY . .

# Expose the port this service listens on
EXPOSE 3000

# Command to Run App
CMD ["node", "app.js"]