#!/bin/bash
set -e

# Enforce strict 0700 permissions for PostgreSQL data directory created by Docker/pg_basebackup
umask 0077
chmod 700 /var/lib/postgresql/data 2>/dev/null || true

PATRONI_NODE_NAME=${PATRONI_NODE_NAME:-$(hostname)}

sed "s/\${PATRONI_NODE_NAME}/${PATRONI_NODE_NAME}/g" /patroni/patroni.yml.template > /tmp/patroni.yml

exec patroni /tmp/patroni.yml

