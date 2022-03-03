###服务器端server.py
import socket
import os
import sys
import struct
import threading
ip_addr = '192.168.1.103'
port = 10086
back_log = 10
succeed_msg = "OK"
server_send_seq = "\n"
def socket_service_image():
    code_version = 202111072116
    print(os.getcwd())
    print("file name: %s" % (__file__), ", code Version: ", code_version)
    print("line: %s" % (sys._getframe().f_lineno))
    server_ip_port = (ip_addr, port)
    tcp_server = socket.socket(socket.AF_INET,
                        socket.SOCK_STREAM)  # 第一步：产生一个对象传俩个参数(socket.AF_INET基于网络通讯,socket.SOCK_STREAM表TCP协议)给tcp_server创建服务器套接字
    tcp_server.bind(server_ip_port)  # 第二步：把IP地址和访问和端口号绑定到套接字
    tcp_server.listen(back_log)  # 第三步：监听链接，listen(5)最多可以有五个建立好三次握手后的backlog(半连接池)等着，后面的需要排队等着

    while True:  # 第四步：服务端做连接循环的接，可以做到接收多个人发的连接
        print('服务端开始运行了')
        conn, addr = tcp_server.accept()  # 第五步：tcp_server.accept()相当于拿到了TCP三次握手的结果是个元祖解压给给conn(三次握手的连接)和addr服务端阻塞
        print('双向链接是', conn)  # 打印conn：
        print('客户端地址', addr)  # 打印addr：
        t = threading.Thread(target=deal_image, args=(conn, addr))
        t.start()
# def socket_service_image():
#     try:
#         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         # s.bind(('127.0.0.1', 6666))
#         s.bind((ip_addr, port))
#         s.listen(10)
#     except socket.error as msg:
#         print(msg)
#         sys.exit(1)
#
#     print("Wait for Connection.....................")
#
#     while True:
#         sock, addr = s.accept()  # addr是一个元组(ip,port)
#         t = threading.Thread(target=deal_image, args=(sock, addr))
#         t.start()
#


def deal_image(sock, addr):
    print("Accept connection from {0}".format(addr))  # 查看发送端的ip和端口

    while True:
        fileinfo_size = struct.calcsize('128sq')
        buf = sock.recv(fileinfo_size)  # 接收图片名
        if buf:
            filename, filesize = struct.unpack('128sq', buf)
            fn = filename.decode().strip('\x00')
            # new_filename = os.path.join('./',
            #                             'new_' + fn)  # 在服务器端新建图片名（可以不用新建的，直接用原来的也行，只要客户端和服务器不是同一个系统或接收到的图片和原图片不在一个文件夹下）
            new_filename = str(addr[0]) + "." + str(addr[1]) + ".png"

            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)  # 写入图片数据
            fp.close()

        # import muggle_ocr
        # sdk = muggle_ocr.SDK(model_type=muggle_ocr.ModelType.OCR)
        #
        # # n = "image.png"
        # with open(new_filename, "rb") as f:
        #     b = f.read()
        # num = sdk.predict(image_bytes=b)
        # if len(num) != 4:
        #     print("length error")

        num = str(1234)

        msg = succeed_msg + server_send_seq + num
        print("服务器发送的消息是： ", msg)
        sock.send(msg.encode('utf-8'))
        sock.close()
        os.remove(new_filename) #删除图片
        break


if __name__ == '__main__':
    socket_service_image()