FROM python:3.11-alpine

# Set working directory
WORKDIR /app

# Copy application code
COPY app.py .

# Create non-root user for security
RUN adduser -D -u 1000 appuser && \
    chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Document exposed port
EXPOSE 8080

# === Project Atomic labels (для dockerfile-validator) ===
LABEL Name="effective-mobile-backend" \
      Version="1.0.0" \
      Release="1" \
      Architecture="x86_64" \
      Summary="Backend service for Effective Mobile test task" \
      Description="Simple Python HTTP backend responding with 'Hello from Effective Mobile!'" \
      Vendor="Effective Mobile" \
      Url="https://github.com/j0konda/effective-mobile-docker-app" \
      Maintainer="j0konda"

# === OCI standard labels (современный стандарт) ===
LABEL org.opencontainers.image.title="Effective Mobile Backend" \
      org.opencontainers.image.version="1.0.0" \
      org.opencontainers.image.description="Simple Python HTTP backend" \
      org.opencontainers.image.url="https://github.com/j0konda/effective-mobile-docker-app" \
      org.opencontainers.image.source="https://github.com/j0konda/effective-mobile-docker-app" \
      org.opencontainers.image.vendor="Effective Mobile"

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/ || exit 1

# Run the application
CMD ["python", "app.py"]