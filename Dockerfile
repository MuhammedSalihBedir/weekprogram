FROM python:3.13-alpine

RUN apk add --no-cache \
    pango \
    ttf-dejavu \
    poppler-utils

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app

COPY . /app

RUN addgroup -S appgroup && \
    adduser -S -G appgroup appuser && \
    chown -R appuser:appgroup /app
USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
