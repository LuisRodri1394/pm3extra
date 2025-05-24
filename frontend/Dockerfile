# Estágio de construção
FROM node:18.17.1-alpine AS builder

# 1. Instala dependências do sistema
RUN apk add --no-cache python3 make g++ git

# 2. Configura diretório de trabalho
WORKDIR /app

# 3. Copia arquivos de dependências primeiro (para cache)
COPY package.json package-lock.json ./

# 4. Instala dependências
RUN npm ci --no-audit --prefer-offline

# 5. Copia todo o código fonte
COPY . .

# 6. Executa o build com verificação explícita
RUN npm run build -- --output-path=dist --configuration=production && \
    [ -d "dist" ] || (echo "Error: dist directory was not created!" && exit 1)

# Estágio de produção
FROM nginx:1.25.2-alpine

# 7. Remove configuração padrão do Nginx
RUN rm -rf /etc/nginx/conf.d/default.conf

# 8. Copia arquivos construídos (com verificação)
COPY --from=builder /app/dist /usr/share/nginx/html

# 9. Copia configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80