# ============================================
# Dockerfile - PgBouncer Connection Pooler
# Lightweight Alpine-based image
# ============================================

FROM alpine:3.20

# Install PgBouncer and PostgreSQL client (for pg_isready health checks)
RUN apk add --no-cache \
    pgbouncer \
    postgresql16-client

# Create necessary directories with proper permissions
RUN mkdir -p /var/log/pgbouncer /var/run/pgbouncer && \
    chown -R pgbouncer:pgbouncer /var/log/pgbouncer /var/run/pgbouncer /etc/pgbouncer

USER pgbouncer

EXPOSE 6432

ENTRYPOINT ["pgbouncer"]
CMD ["/etc/pgbouncer/pgbouncer.ini"]
