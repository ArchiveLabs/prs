#!/usr/bin/env python3

from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from prs.routes import api
from prs.configs import OPTIONS
from prs import __version__ as VERSION

app = FastAPI(
    title="Public Readium Service (PRS) API Server",
    description="Archive Labs Public Readium Service",
    version=VERSION,
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
