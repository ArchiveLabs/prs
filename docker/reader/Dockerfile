FROM node:20-slim AS base

# Set environment variables for PNPM (optional, but good practice)
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"

WORKDIR /app

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/edrlab/thorium-web.git
RUN corepack enable

WORKDIR /app/thorium-web

RUN --mount=type=cache,id=pnpm_store,target=/pnpm/store pnpm install --frozen-lockfile

RUN pnpm build

EXPOSE 3000

CMD ["pnpm", "start"]