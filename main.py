import socket
import getresponse
import openai

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 4396  # Port to listen on (non-privileged ports are > 1023)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("server started")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        while True:
            conn, addr = s.accept()
            responseGetter = getresponse.ResponseGetter()
            responseGetter.initialize()
            responseGetter.set_apikey("")

            with conn:
                print(f"Connected by {addr}")
                while True:
                    try:
                        try:
                            data = conn.recv(16384).decode('utf-8')
                            print("received data")

                            if data[0:2] == "00":
                                temp = data[2:].split(chr(30))
                                if temp[0] == "user0" and temp[1] == "A2345678":
                                    print("logged in\n")
                                    conn.sendall(bytes("000\nEND4321\n", 'utf-8'))

                                else:
                                    print("invalid pass\n")
                                    conn.sendall(bytes("001\nEND4321\n", 'utf-8'))

                            elif data[0:2] == "01":
                                print("chat received")
                                a = responseGetter.request_response(data[2:], "gpt-4", "1", 0)
                                print("replied\n")
                                conn.send(bytes("01" + a + "\nEND4321\n", 'utf-8'))

                            elif data[0:2] == "02":
                                print("user exit\n")
                                break

                            else:
                                print("other exit\n")
                                break

                        except openai.InvalidRequestError:
                            print("Maximum reached")
                            conn.send(bytes("01" + "[You have reached the maximum conext limit, please login again.]" + "\nEND4321\n", 'utf-8'))

                    except:
                        break


