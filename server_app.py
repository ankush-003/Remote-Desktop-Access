from fastapi import FastAPI, Request, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import uvicorn
import socket

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

conn = None
connected = False

async def connect():
    global conn, connected
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_pc = ""
    port = 12345
    s.bind((local_pc, port))
    s.listen()
    print("Waiting for connection...")
    conn, address = s.accept()
    connected = True
    print("Connection from: " + str(address))
    # return address
    return RedirectResponse(url="/home")


async def get_command(command: str):
    # conn, address = s.accept()
    # print("Connection from: " + str(address))
    try:
        conn.sendall(command.encode())
        packet = conn.recv(100000)
        decoded = packet.decode()
        # print(decoded)
        return decoded
    except:
        print("Connection closed")
        conn.close()
        connected = False
        return "Connection closed"

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, background_tasks: BackgroundTasks):
    # address = await connect()
    # background_tasks.add_task(connect)
    if not connected:
        background_tasks.add_task(connect)
        
    return templates.TemplateResponse("index.html", {"request": request, "connected": connected})

@app.get("/command/{command}")
async def getCommand(command: str):
    result = await get_command(command)
    print(result)
    return result

if __name__ == '__main__':
    uvicorn.run("server_app:app", host="0.0.0.0", port=8000, reload=True)