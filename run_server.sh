cd api_server
gunicorn musicgen_server:app -w 3 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:30006 --timeout 300