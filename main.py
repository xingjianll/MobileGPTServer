import socket

import getresponse
import openai

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 4396  # Port to listen on (non-privileged ports are > 1023)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("server started")

        while True:
            conn, addr = s.accept()

            with conn:
                conn.settimeout(120)
                print(f"====Connected by {addr}======")
                responseGetter = getresponse.ResponseGetter()
                responseGetter.initialize()
                responseGetter.set_apikey("")

                while True:
                    try:
                        try:
                            try:
                                data = conn.recv(16384).decode('utf-8')
                                print("received data")

                                if data[0:2] == "00":
                                    temp = data[2:].split(chr(30))
                                    if temp[0] == "user0" and temp[
                                        1] == "A2345678":
                                        conn.sendall(
                                            bytes("000\nEND4321\n", 'utf-8'))
                                        print("logged in\n")

                                    else:
                                        conn.sendall(
                                            bytes("001\nEND4321\n", 'utf-8'))
                                        print("invalid pass\n")

                                elif data[0:2] == "01":
                                    print("chat received")
                                    a = responseGetter.request_response(
                                        data[2:], "gpt-3.5-turbo", "1", 0)
                                    print("replied\n")
                                    conn.send(bytes("01" + a + "\nEND4321\n",
                                                    'utf-8'))

                                elif data[0:2] == "02":
                                    print("user exit\n\n")
                                    break

                                else:
                                    print("other exit\n\n")
                                    break
                            except TimeoutError:
                                conn.send(bytes("01" + "[Connection timed out due to inactivity, please login again]" + "\nEND4321\n",
                                                'utf-8'))
                                print("connection timeout exit\n\n")
                                break

                        except openai.InvalidRequestError:
                            print("Maximum reached")
                            conn.send(bytes(
                                "01" + "[You have reached the maximum conext limit, please login again.]" + "\nEND4321\n",
                                'utf-8'))
                    except:
                        print("unknown error exit\n\n")
                        break
