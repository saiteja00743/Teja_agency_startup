# Gunicorn Production Config

import multiprocessing

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Workers — (2 × CPU cores) + 1 is the recommended formula
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
loglevel = "info"
accesslog = "-"   # stdout
errorlog  = "-"   # stderr
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "teja-labs"

# Security
limit_request_line = 4096
limit_request_fields = 100
limit_request_field_size = 8190

# Graceful restart
graceful_timeout = 30
max_requests = 1000
max_requests_jitter = 100
