import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
local_pc = ""
port = 12345

s.bind((local_pc, port))
s.listen()

while True:
    print("Waiting for connection...")
    conn, address = s.accept()
    print("Connection from: " + str(address))
    try:
        while True:
            command = input("Enter command: ")
            conn.sendall(command.encode())
            packet = conn.recv(100000)
            decoded = packet.decode()
            print(decoded)
    except:
        print("Connection closed")
        conn.close()