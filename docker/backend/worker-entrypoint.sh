#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

celery -A movies_backend worker -l info