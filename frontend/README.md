# Vstrecha

## Project Setup

### Via Docker

```sh
docker build -t vue-builder .
docker create --name temp vue-builder
docker cp temp:/app/dist .
docker rm temp
chown -R $USER:$USER ./dist
```

### Via cmd

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Type-Check, Compile and Minify for Production

```sh
npm run build
```

### Lint with [ESLint](https://eslint.org/)

```sh
npm run lint
```

## Develop project

To have a real time updates we need to proxy requests from the server to our local computer.

```sh
npm run dev
ssh -R 0.0.0.0:8080:localhost:5173 host
```

Now location /_token_/ on the server will (after auth) transfer query to the Vite dev server.

On the server side we have location with proxy on _host.docker.internal:8080_. Due to Docker network host.docker.internal expose to 172.18.0.1 which is allowed to connect to 0.0.0.0:8080 by ufw rule
