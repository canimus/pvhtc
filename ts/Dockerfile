FROM node:10.13.0-alpine

ENV TIME_ZONE=Europe/Amsterdam

RUN apk --update add tzdata

WORKDIR /usr/src/app

COPY tsconfig.json .
COPY package*.json ./
COPY src/ ./src/

RUN npm install
RUN npm run build
RUN cat dist/hello.js
RUN rm -rf src
RUN ls -la

CMD ["npm", "run", "main"]