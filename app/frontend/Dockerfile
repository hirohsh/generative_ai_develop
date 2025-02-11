FROM node:22-bookworm-slim as base
WORKDIR /app

FROM base as builder
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM base as develop
ENV NODE_ENV=development

FROM gcr.io/distroless/nodejs22-debian12:debug-nonroot as staging
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app/.next/standalone ./
COPY --from=builder --chown=nonroot:nonroot /app/.next/static ./.next/static
COPY --from=builder  /app/public ./public
USER nonroot
EXPOSE 3000
ENTRYPOINT ["/nodejs/bin/node", "server.js" ]

FROM gcr.io/distroless/nodejs22-debian12:nonroot as production
ENV NODE_ENV=production
WORKDIR /app
COPY --from=builder --chown=nonroot:nonroot /app/.next/standalone ./
COPY --from=builder --chown=nonroot:nonroot /app/.next/static ./.next/static
COPY --from=builder  /app/public ./public
USER nonroot
EXPOSE 3000
ENTRYPOINT ["/nodejs/bin/node", "server.js" ]
