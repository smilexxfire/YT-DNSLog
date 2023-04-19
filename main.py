import socketserver
import threading
import time

from module.message import Message
from module.banner import banner

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            request_data = self.request[0]
            # 将请求封装成Message格式
            message = Message.from_bytes(request_data)
            # 记录并输出
            print("%s --- %s --- %s" % (message.question[0]['QNAME'],
                                        self.client_address[0], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
            # 转换为响应包的格式
            message.transfer_to_answer()
            # 响应给客户
            client_socket = self.request[1]
            client_socket.sendto(message.to_bytes(), self.client_address)
        except:
            print("非法的请求 from %s" % self.client_address[0])


class Server(socketserver.ThreadingMixIn, socketserver.UDPServer):
    def __init__(self, host, handler=Handler):
        super().__init__((host, 53), handler)

    def start(self):
        with self:
            server_thread = threading.Thread(target=self.serve_forever)
            server_thread.daemon = True
            server_thread.start()
            print('The DNS server is running at 0.0.0.0:53...')
            server_thread.join()


if __name__ == "__main__":
    print(banner)
    server = Server('0.0.0.0')
    server.start()