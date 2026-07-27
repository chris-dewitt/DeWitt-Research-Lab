FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    ATTICUS_HOST=0.0.0.0 \
    PORT=8080

WORKDIR /app

COPY packages/drl-protocol /app/packages/drl-protocol
COPY packages/drl-ai-core /app/packages/drl-ai-core
COPY services/atlas /app/services/atlas
COPY services/fedlens /app/services/fedlens
COPY services/balancelab-ai /app/services/balancelab-ai
COPY services/evalforge /app/services/evalforge
COPY services/atticus-control-plane /app/services/atticus-control-plane

RUN pip install --no-cache-dir \
    /app/packages/drl-protocol \
    /app/packages/drl-ai-core \
    /app/services/atlas \
    /app/services/fedlens \
    /app/services/balancelab-ai \
    /app/services/evalforge \
    /app/services/atticus-control-plane

USER 65532:65532
EXPOSE 8080

ENTRYPOINT ["atticus-server"]
