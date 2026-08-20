import asyncio
from typing import Set
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from utils.solver import solve_challenge

app = FastAPI(title="CTF Automation Live Dashboard")

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

active_connections: Set[WebSocket] = set()
is_running = False


async def broadcast(event_type: str, data: dict):
    message = {"type": event_type, **data}
    dead_connections = set()
    for ws in active_connections:
        try:
            await ws.send_json(message)
        except Exception:
            dead_connections.add(ws)
    active_connections.difference_update(dead_connections)


async def run_automation_task(host: str, port: int):
    global is_running
    is_running = True
    await broadcast("status", {"status": "CONNECTING", "host": host, "port": port})

    try:
        reader, writer = await asyncio.open_connection(host, port)
        await broadcast("status", {"status": "CONNECTED", "host": host, "port": port})

        buf = ""
        solved_count = 0

        while is_running:
            raw_data = await reader.read(4096)
            if not raw_data:
                await broadcast("log", {"level": "info", "message": "Server closed TCP connection."})
                break

            data = raw_data.decode("utf-8", errors="ignore")

            if "[Challenge" in data:
                buf = data
            else:
                buf += data

            await broadcast("server_payload", {"raw": data})

            if "CTF{" in data or "flag:" in data.lower():
                await broadcast("flag_captured", {"payload": data})
                break

            ans = solve_challenge(buf)
            if ans != "UNKNOWN":
                await asyncio.sleep(0.1)
                writer.write(f"{ans}\n".encode("utf-8"))
                await writer.drain()

                solved_count += 1
                await broadcast("solution_sent", {
                    "answer": ans,
                    "solved_count": solved_count,
                    "challenge_chunk": buf.strip()
                })
                buf = ""

        writer.close()
        await writer.wait_closed()

    except Exception as e:
        await broadcast("status", {"status": "ERROR", "error": str(e)})
    finally:
        is_running = False
        await broadcast("status", {"status": "DISCONNECTED"})


@app.get("/", response_class=HTMLResponse)
async def get_index():
    with open("frontend/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global is_running
    await websocket.accept()
    active_connections.add(websocket)
    try:
        while True:
            cmd = await websocket.receive_json()
            action = cmd.get("action")
            if action == "START" and not is_running:
                host = cmd.get("host", "127.0.0.1")
                port = int(cmd.get("port", 5000))
                asyncio.create_task(run_automation_task(host, port))
            elif action == "STOP":
                is_running = False
    except WebSocketDisconnect:
        active_connections.remove(websocket)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)