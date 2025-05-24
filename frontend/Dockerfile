# Estágio de construção (builder)
FROM node:18 AS builder
WORKDIR /app

# 1. Copia os arquivos de dependência primeiro (para melhorar cache)
COPY package.json package-lock.json ./

# 2. Instala dependências
RUN npm ci --quiet

# 3. Copia o restante dos arquivos
COPY . .

# 4. Executa o build de produção (Angular 15+)
RUN npm run build -- --configuration=production --progress=false

# Estágio de produção
FROM nginx:alpine

# Copia os arquivos construídos
COPY --from=builder /app/dist/frontend /usr/share/nginx/html

# Configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80