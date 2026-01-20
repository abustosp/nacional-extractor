FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        p7zip-full \
        cabextract \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /data
COPY extractor.py /app/extractor.py

ENTRYPOINT ["python3", "/app/extractor.py"]
