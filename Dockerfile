# VRBLL Chat Backend Dockerfile
FROM node:20-alpine
WORKDIR /app
COPY . .
RUN npm install && npm install ws uuid
CMD ["node", "wsServer.ts"]
