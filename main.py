import socket
import threading
import pickle
from spam_filter import is_spam
from des_cipher import des_encrypt, des_decrypt

class P2PChat:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.peers = []
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Set pickle protocol version
        self.pickle_protocol = 4  # Using protocol 4 for better compatibility

    def start_server(self):
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[SERVER] Listening on {self.host}:{self.port}")
        while True:
            conn, _ = self.server_socket.accept()
            self.peers.append(conn)
            threading.Thread(target=self.handle_client, args=(conn,)).start()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                try:
                    # Try to decode as string first
                    encrypted = data.decode()
                    decrypted = des_decrypt(encrypted)
                    print(f"\n[RECEIVED]: {decrypted}")
                except UnicodeDecodeError:
                    # If not a string, try to unpickle
                    try:
                        message = pickle.loads(data)
                        print(f"\n[RECEIVED]: {message}")
                    except pickle.UnpicklingError:
                        print("[ERROR] Could not decode message")
            except Exception as e:
                print(f"[ERROR] Connection lost: {e}")
                break

    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, peer_port))
            self.peers.append(peer_socket)
            threading.Thread(target=self.handle_client, args=(peer_socket,)).start()
            print(f"[CONNECTED] to {peer_host}:{peer_port}")
        except Exception as e:
            print(f"[ERROR] Could not connect: {e}")

    def send_messages(self):
        while True:
            msg = input("Enter message: ")
            if is_spam(msg):
                print("[WARNING] Spam detected. Message not sent.")
                continue
            try:
                encrypted = des_encrypt(msg)
                for peer in self.peers:
                    try:
                        # Send as string
                        peer.send(encrypted.encode())
                    except:
                        print("[ERROR] Failed to send message.")
            except Exception as e:
                print(f"[ERROR] Failed to process message: {e}")

    def run(self):
        threading.Thread(target=self.start_server, daemon=True).start()
        while input("Connect to peer? (y/n): ").strip().lower() == 'y':
            peer_ip = input("Peer IP: ")
            peer_port = int(input("Peer Port: "))
            self.connect_to_peer(peer_ip, peer_port)
        self.send_messages()

if __name__ == "__main__":
    ip = input("Your IP: ")
    port = int(input("Your Port: "))
    chat = P2PChat(ip, port)
    chat.run()
