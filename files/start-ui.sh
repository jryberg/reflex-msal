#!/bin/bash

DEBUG=${DEBUG:=FALSE}
DEBUG=${DEBUG^^}

source /app/.venv/bin/activate

# Create frontend
rm -rf /srv/*
reflex init
API_URL=http://localhost:8088 reflex export --loglevel debug --frontend-only --no-zip && mv .web/build/client/* /srv/ && rm -rf .web

export PYTHONUNBUFFERED=1

if [[ "${DEBUG}" == "TRUE" ]]; then
  CADDY_LOG_LEVEL=DEBUG caddy start && exec reflex run --env prod --backend-only --loglevel debug
else
  caddy start && exec reflex run --env prod --backend-only 
fi
