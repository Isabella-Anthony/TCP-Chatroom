# TCP-Chatroom

A simple **TCP chatroom** built in **Python**, featuring a **multi-threaded server** that supports multiple clients chatting at the same time.

---

## Features

- TCP-based client/server chat
- Multiple clients supported concurrently (threaded server)
- Broadcast-style messaging (one client → server → all clients)
- Two versions included:
  - **Basic**: `server.py` + `client.py`
  - **Multi-client / threaded**: `multi_tcp_server.py` + `multi_tcp_client.py`

---

## Project Structure

- `server.py` — Basic TCP server
- `client.py` — Basic TCP client
- `multi_tcp_server.py` — Multi-threaded TCP server (handles multiple clients concurrently)
- `multi_tcp_client.py` — Client for multi-threaded server (and/or multi-client testing)

---

## Requirements

- Python 3.8+ (recommended)
- No external dependencies (uses Python standard library)

Check your version:

```bash
python3 --version


