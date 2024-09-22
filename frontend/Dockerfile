FROM node as builder

# Create app directory
WORKDIR /usr/src/app

# Install app dependencies
COPY package*.json ./

RUN npm install --legacy-peer-deps

COPY . .
EXPOSE 3000
RUN npm run build
CMD [ "npm", "start" ]