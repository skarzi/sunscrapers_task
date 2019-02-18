#!/usr/bin/env bash

set -o errexit
set -o pipefail

cmd="$@"

if [ -z "${POSTGRES_USER}" ]; then
    export POSTGRES_USER=postgres
fi

export DATABASE_URL="postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"


postgres_ready() {
python << END
import sys
import psycopg2

try:
    psycopg2.connect(
        dbname="${POSTGRES_DB}",
        user="${POSTGRES_USER}",
        password="${POSTGRES_PASSWORD}",
        host="${POSTGRES_HOST}",
        port="${POSTGRES_PORT}")
except psycopg2.OperationalError:
    sys.exit(-1)

sys.exit(0)
END
}


counter=0
until postgres_ready; do
  >&2 echo 'PostgreSQL is unavailable (sleeping 1s)...'
  sleep 1
  if [ $counter -gt "60" ]; then
    echo "Cannot connect to PostgreSQL - exiting..."
    exit 1
  fi
  counter=$(expr $counter + 1)
done

>&2 echo "PostgreSQL is up - continuing..."

exec $cmd
