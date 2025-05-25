# Estágio de construção
FROM node:18.19-alpine AS builder

RUN apk add --no-cache python3 make g++

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci --no-audit --prefer-offline

COPY . .

RUN npm install -g @angular/cli
RUN npm run build -- --configuration=production

# Verifica se build foi criado corretamente
RUN ls -la /app/dist || (echo "Dist directory not found!" && exit 1)

# Estágio de produção
FROM nginx:1.25.2-alpine

RUN rm -rf /etc/nginx/conf.d/default.conf

# ⬇️ Aqui está o ponto principal: copiar do caminho correto do Angular
COPY --from=builder /app/dist/frontend /usr/share/nginx/html

COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1
