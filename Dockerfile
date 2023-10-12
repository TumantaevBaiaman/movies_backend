# BUILDER
FROM python:3.9-alpine as builder
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add --no-cache postgresql-dev gcc libc-dev libffi-dev python3-dev musl-dev jpeg-dev zlib-dev
COPY . .
RUN pip install --upgrade pip \
    && pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# FINAL
FROM python:3.9-alpine
WORKDIR /app
RUN addgroup -S app && adduser -S app -G app
RUN apk update && apk add gcc musl-dev libffi-dev
COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache /wheels/*
COPY . .
RUN chmod +x ./entrypoint.sh && chown -R app:app .
USER app
EXPOSE 8000
ENTRYPOINT [ "./entrypoint.sh" ]