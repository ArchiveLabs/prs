# prs

A Public Readium Service for Archive.org and OpenLibrary.org

## Installation

```
git clone git@github.com:ArchiveLabs/prs.git
cd prs
./run.sh
```

## Configuration

The first time `run.sh` is executed, it will call
`docker/configure.sh` to produce a file called `prs.env` with
environment variables set. You may edit this file to achieve your
desired configuration. `prs.env` is loaded by `run.sh` and is also
made available through docker `compose.yml`. Finally, when the python
application starts, many of these `env` variables are loaded via
`configs/__init__.py`.

* `PRS_BASE_URL` can be (optionally) used to specify a base url "/api" -> "https://example.com/api"

## Uvicorn

By default, the application will run publicly on the port specified by
`PRS_PORT` which defaults to `8080`. Internally within docker, the
Uvicorn service will run on `8083`.

## Nginx (Reverse Proxy)

Here is an example an nginx config for reverse proxying to PRS that should "Just Work &trade;" out of the box:

```
server {
    server_name example.com;
    listen 443 ssl http2;

    root /var/www/example.com/;

    # For Public Readium Service
    location / {
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Host $host;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_pass http://127.0.0.1:8080;  # or whatever PRS_PORT you've chosen
        proxy_redirect off;
    }

    # ssl_certificate(s) ...
}
```

## Generating Manifests

/ia/{ia_id}/manifest.json

e.g. /ia/honore-de-balzac_father-goriot_ellen-marriage/manifest.json

## Reading an Epub

/ia/{ia_id}/read

e.g. /ia/honore-de-balzac_father-goriot_ellen-marriage/read
