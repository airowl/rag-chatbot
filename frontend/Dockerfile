FROM node:22-alpine
WORKDIR /app

# Copia i file di dipendenze prima del codice
COPY package*.json ./
RUN npm install

# Copia tutto il codice
COPY . .

# Esponi la porta
EXPOSE 5173

# Comando per development
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
