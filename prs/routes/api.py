#!/usr/bin/env python

"""
    API routes for PRS,

    :copyright: (c) 2025 by AUTHORS
    :license: see LICENSE for more details
"""

import base64
import requests
import internetarchive as ia
from urllib.parse import quote
from fastapi import (
    APIRouter,
    Request,
    HTTPException,
    status
)
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from prs.configs import SERVICE_URL, PORT, READIUM_HOST_PORT

router = APIRouter()

def ia_get_epub_filepath(item_id):
    item = ia.get_item(item_id)
    for file in item.files:
        if file['name'].endswith('.epub'):
            return f"https://archive.org/download/{item_id}/{file['name']}"

def ol_get_epub_filepath(olid):
    # fetch olid from openlibrary and get url (if ends with epub)
    pass

def encode_book_path(source: str, book_id: str) -> str:
    source_to_filepath = {
        "ia": ia_get_epub_filepath,
        #"ol": lambda: f"" # use openlibrary.org/search.json to get url of ebook
    }    
    filepath = source_to_filepath[source](book_id)
    encoded_filepath = base64.b64encode(filepath.encode()).decode()
    return encoded_filepath.replace('/', '_').replace('+', '-').replace('=', '')

def prs_uri(request: Request):
    if SERVICE_URL:
        return SERVICE_URL
    if host := request.headers.get('x-forwarded-host'):
        return f"{request.url.scheme}://{host}"
    port = f":{PORT}" if PORT not in {80, 443} else ""
    return f"{request.url.scheme}://{request.url.hostname}{port}"

@router.get('/', status_code=status.HTTP_200_OK)
async def apis(request: Request):
    return {
        f"{prs_uri(request)}/api": {
            "description": "List all APIs",
        },
        f"{prs_uri(request)}/api/:id/manifest.json": {
            "description": "Generate readium manifest for resource",
            "args": {"source": ["ia", "ol"], "format": ["epub", "pdf"]}
        }
    }

@router.get("/{source}/{book_id}/read")
async def redirect_reader(request: Request, source: str, book_id: str):
    manifest_url = f"{prs_uri(request)}/api/{source}/{book_id}/manifest.json"
    manifest_uri = quote(manifest_url, safe='')
    return RedirectResponse(f"https://playground.readium.org/read/manifest/{manifest_uri}")

@router.get("/{source}/{book_id}/manifest.json")
async def get_manifest(request: Request, source: str, book_id: str):
    def patch_manifest(manifest):
        manifest_uri = f"{prs_uri(request)}/api/{source}/{book_id}/manifest.json"
        encoded_manifest_uri = quote(manifest_uri, safe='')
        for i in range(len(manifest['links'])):
            if manifest['links'][i].get('rel') == 'self':
                manifest['links'][i]['href'] = encoded_manifest_uri
        return manifest

    # TODO: s3 permission/auth checks go here for protected epubs, or decorate this route

    readium_uri = f"http://{READIUM_HOST_PORT}/{encode_book_path(source, book_id)}/manifest.json"
    manifest = requests.get(readium_uri).json()
    return patch_manifest(manifest)

# Proxy for all other readium requests
@router.get("/{source}/{book_id}/{readium_uri:path}")
async def proxy_readium(request: Request, source: str, book_id: str, readium_uri: str, format: str=".epub"):
    # TODO: permission/auth checks go here, or decorate this route
    readium_url = f"http://{READIUM_HOST_PORT}/{encode_book_path(source, book_id)}/{readium_uri}"
    r = requests.get(readium_url, params=dict(request.query_params))
    if readium_url.endswith('.json'):
        return r.json()
    content_type = r.headers.get("Content-Type", "application/octet-stream")
    return Response(content=r.content, media_type=content_type)

