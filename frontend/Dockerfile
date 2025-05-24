# Estágio de construção
FROM node:18.17.1-alpine AS builder

# 1. Configuração inicial
RUN apk add --no-cache python3 make g++ git
WORKDIR /app

# 2. Instalação otimizada de dependências
COPY package.json package-lock.json ./
RUN npm ci --no-audit --prefer-offline

# 3. Cópia dos arquivos fonte
COPY . .

# 4. Build com verificação detalhada
RUN npm run build -- --output-path=dist --configuration=production; \
    BUILD_EXIT_CODE=$?; \
    if [ ! -d "dist" ]; then \
      echo "=== BUILD DEBUG INFORMATION ==="; \
      echo "Current directory contents:"; ls -la; \
      echo "angular.json contents:"; cat angular.json | grep outputPath; \
      echo "npm build output:"; cat npm-debug.log 2>/dev/null || echo "No debug log"; \
      exit 1; \
    fi; \
    exit $BUILD_EXIT_CODE

# Estágio de produção
FROM nginx:1.25.2-alpine
COPY --from=builder /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d
EXPOSE 80