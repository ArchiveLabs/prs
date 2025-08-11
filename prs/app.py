#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from prs.routes import api
from prs.configs import OPTIONS, DOCKER_GATEWAY
from prs import __version__ as VERSION

app = FastAPI(
    title="Public Readium Service (PRS) API Server",
    description="Archive Labs Public Readium Service",
    version=VERSION,
)
if DOCKER_GATEWAY:
    app.add_middleware(
        ProxyHeadersMiddleware, trusted_hosts=[DOCKER_GATEWAY]
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api.router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("prs.app:app", **OPTIONS)
