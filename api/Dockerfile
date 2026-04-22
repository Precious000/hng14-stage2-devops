# ---------- BUILD ----------
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# ---------- FINAL ----------
FROM node:20-alpine

WORKDIR /app

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

COPY --from=builder /app /app

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 3000

HEALTHCHECK CMD wget --spider -q http://localhost:3000 || exit 1

CMD ["npm", "start"]
