FROM node:lts AS development

WORKDIR /app

COPY package*.json ./

COPY . /app
    
RUN npm install next react react-dom npm-git-install

CMD npm run dev