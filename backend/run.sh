#gunicorn --workers 3 --bind unix:myproject.sock --daemon -m 007 --user www-data --worker-class gevent wsgi:app
#gunicorn --workers 3 --bind unix:myproject.sock --daemon -m 007 --user www-data --worker-class gevent wsgi:app
/usr/local/python3/bin/gunicorn -D -w 3 -t 90 -k 'gevent' -b 127.0.0.1:8080 wsgi:app