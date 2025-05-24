# Estágio de construção
FROM node:18.17.1-alpine AS builder

# 1. Configura ambiente e instala dependências do sistema
RUN apk add --no-cache python3 make g++

# 2. Configura diretório de trabalho
WORKDIR /app

# 3. Copia apenas os arquivos necessários para instalação
COPY package.json package-lock.json ./

# 4. Instala dependências com cache
RUN npm ci --no-audit --prefer-offline

# 5. Copia todo o código fonte
COPY . .

# 6. Executa o build com tratamento de erros detalhado
RUN npm run build -- --output-path=dist --configuration=production 2>&1 | tee build.log || \
    (echo "=== BUILD FAILED ===" && cat build.log && exit 1)

# Estágio de produção
FROM nginx:1.25.2-alpine

# 7. Remove configuração padrão do Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# 8. Copia arquivos construídos e configuração Nginx
COPY --from=builder /app/dist/frontend /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d

# 9. Expõe porta e define health check
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD wget --quiet --tries=1 --spider http://localhost:80 || exit 1