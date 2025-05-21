import socket
import pyautogui
import io

def send_screenshot(server_ip, server_port=9999):
    screenshot = pyautogui.screenshot()
    buf = io.BytesIO()
    screenshot.save(buf, format='PNG')
    img_bytes = buf.getvalue()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((server_ip, server_port))

    # Prvo šaljemo dužinu slike kao 8 bajtova (int)
    sock.send(len(img_bytes).to_bytes(8, 'big'))
    sock.sendall(img_bytes)
    sock.close()
    print("[*] Screenshot poslat!")

if __name__ == "__main__":
    server_ip = input("Unesi IP servera: ").strip()
    send_screenshot(server_ip)
