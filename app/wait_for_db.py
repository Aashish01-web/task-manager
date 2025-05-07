import os
import time
import socket

host = os.getenv("POSTGRES_HOST", "db")
port = int(os.getenv("POSTGRES_PORT", 5432))

print(f"🔄 Waiting for PostgreSQL at {host}:{port}...")

while True:
    try:
        with socket.create_connection((host, port), timeout=2):
            print("Starting the application")
            break
    except OSError:
        time.sleep(0.5)
        print("Waiting for PostgreSQL")