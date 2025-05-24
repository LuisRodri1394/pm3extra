# Estágio de construção (builder)
FROM node:16 AS builder
WORKDIR /app

# Primeiro copia apenas os arquivos necessários para instalação
COPY package.json package-lock.json ./

# Instala dependências com cache
RUN npm ci --quiet

# Copia o restante dos arquivos
COPY . .

# Executa o build com output detalhado
RUN npm run build -- --prod --progress=false

# Estágio de produção
FROM nginx:alpine

# Copia os arquivos construídos
COPY --from=builder /app/dist/frontend /usr/share/nginx/html

# Configuração do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80