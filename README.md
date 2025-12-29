# CodeShift Test Programs

Simple Python programs for testing code translation workflows.

## Programs

### file_watcher.py
Monitors a directory for file changes (create/modify/delete).

```bash
# Run locally
python file_watcher.py

# Run with custom settings
WATCH_DIR=/path/to/watch POLL_INTERVAL=5 python file_watcher.py
```

### health_server.py
Minimal HTTP server with health check endpoint.

```bash
# Run locally
python health_server.py

# Run on different port
PORT=9000 python health_server.py

# Test endpoints
curl http://localhost:8080/health
curl http://localhost:8080/echo
curl -X POST http://localhost:8080/echo -d '{"test": true}'
```

## Docker Usage

Both programs are designed to run as long-lived containers:

```bash
# Health server
docker run -p 8080:8080 health-server:latest

# File watcher (mount a volume to watch)
docker run -v /path/to/watch:/tmp/watched file-watcher:latest
```

## Translation Targets

These programs use only Python stdlib, making them ideal for translation to:
- Rust (no external crates needed)
- Go (stdlib only)
- TypeScript/Node.js
