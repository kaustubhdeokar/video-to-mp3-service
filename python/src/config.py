# config.py
import os

# MYSQL_HOST_DOCKER = os.environ.get("MYSQL_HOST", "db")  # Use 'db' as default since it's the service name in docker-compose
MYSQL_HOST = os.environ.get("MYSQL_HOST", "localhost")
MYSQL_USER = os.environ.get("MYSQL_USER", "root")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "Kaustubh1")
MYSQL_DB = os.environ.get("MYSQL_DB", "pymicroservice")
MYSQL_PORT = int(os.environ.get("MYSQL_PORT", 3306))