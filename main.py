import socket
import getresponse
HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
PORT = 4396  # Port to listen on (non-privileged ports are > 1023)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("server started")
    responseGetter = getresponse.ResponseGetter()
    responseGetter.initialize()
    responseGetter.set_apikey("")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(16384).decode('utf-8')
                    print(data)
                    if data[0:2] == "00":
                        temp = data[2:].split(chr(30))
                        print(temp)
                        if temp[0] == "user0" and temp[1] == "A2345678":
                            print("connected")
                            conn.sendall(bytes("000\nEND4321\n", 'utf-8'))
                        else:
                            conn.sendall(bytes("001\nEND4321\n", 'utf-8'))
                    elif data[0:2] == "01":
                        a = responseGetter.request_response(data[2:], "gpt-3.5-turbo", "1", 0)
                        print(a)
                        conn.send(bytes("01" + a + "\nEND4321\n", 'utf-8'))
                    elif data[0:2] == "02":
                        break
                    else:
                        break
