import socket
import getresponse
import openai

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 4396  # Port to listen on (non-privileged ports are > 1023)


def set_keepalive_l(sock, after_idle_sec=3, interval_sec=5, max_fails=1):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

def set_keepalive_o(sock, after_idle_sec=3, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    sends a keepalive ping once every 3 seconds (interval_sec)
    """
    # scraped from /usr/include, not exported by python's socket module
    TCP_KEEPALIVE = 0x10
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, interval_sec)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("server started")

        while True:
            conn, addr = s.accept()

            with conn:
                print(f"====Connected by {addr}======")
                set_keepalive_o(conn, 5, 5, 1)
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
                                    if temp[0] == "user0" and temp[1] == "A2345678":
                                        conn.sendall(bytes("000\nEND4321\n", 'utf-8'))
                                        print("logged in\n")

                                    else:
                                        conn.sendall(bytes("001\nEND4321\n", 'utf-8'))
                                        print("invalid pass\n")

                                elif data[0:2] == "01":
                                    print("chat received")
                                    a = responseGetter.request_response(data[2:], "gpt-3.5-turbo", "1", 0)
                                    print("replied\n")
                                    conn.send(bytes("01" + a + "\nEND4321\n", 'utf-8'))

                                elif data[0:2] == "02":
                                    print("user exit\n\n")
                                    break

                                else:
                                    print("other exit\n\n")
                                    break
                            except TimeoutError:
                                conn.send(bytes("01" + "[Connection timeout, please login again.]" + "\nEND4321\n", 'utf-8'))
                                print("connection timeout exit\n\n")
                                break

                        except openai.InvalidRequestError:
                            print("Maximum reached")
                            conn.send(bytes("01" + "[You have reached the maximum conext limit, please login again.]" + "\nEND4321\n", 'utf-8'))
                    except:
                        print("unknown error exit\n\n")
                        break

