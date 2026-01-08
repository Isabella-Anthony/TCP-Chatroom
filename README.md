# TCP-Chatroom

A **TCP chatroom** built in **Python**, featuring a **multi-threaded server** that supports multiple clients chatting at the same time.

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

- Python 3.8+
- No external dependencies (uses Python standard library)

Check your version:

```bash
python3 --version

```

## How to run

Open a terminal and start the server:

```bash
python3 multi_tcp_server.py

```
- The server will start listening for incoming client connections.

Open **another** terminal and start a client:

```bash
python3 multi_tcp_client.py

```

- Repeat this step in additional terminals to connect multiple clients.

---

Usage

- Type a message in any client terminal and press Enter

- Messages are sent to the server and broadcast to all connected clients

- Press Ctrl + C in the server terminal to shut down the chatroom

