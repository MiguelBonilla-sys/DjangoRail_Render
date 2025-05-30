web: gunicorn mysite.wsgi --bind 0.0.0.0:$PORT
worker: celery -A mysite worker --loglevel=info
beat: celery -A mysite beat --loglevel=info
