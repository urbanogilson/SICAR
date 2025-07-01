#!/usr/bin/env bash
# entrypoint.download.sh

set -e

STATE=${STATE:-DF}
FOLDER=${FOLDER:-data/$STATE}
mkdir -p "$FOLDER"
POLYGON=${POLYGON:-APPS}
TRIES=${TRIES:-25}
DEBUG=${DEBUG:-False}
TIMEOUT=${TIMEOUT:-30}
MAX_RETRIES=${MAX_RETRIES:-5}

mkdir -p "$FOLDER"
python examples/download_state.py \
  --state "$STATE" \
  --polygon "$POLYGON" \
  --folder "$FOLDER" \
  --tries "$TRIES" \
  --debug "$DEBUG" \
  --timeout "$TIMEOUT" \
  --max_retries "$MAX_RETRIES"
