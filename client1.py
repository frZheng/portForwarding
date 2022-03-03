# #import socket
# from socket import *
# import time
# import threading
#
# def connect_to(message = "测试"):
#     ip_addr = 'www.lrdkzz.com'
#     port = 9876
#     server_ip_port=(ip_addr,port)
#     # back_log=5
#     buffer_size=1024
#     print(message)
#     tcp_client=socket(AF_INET,SOCK_STREAM)   #第一步：客户端产生一个对象传俩个参数(socket.AF_INET基于网络通讯,socket.SOCK_STREAM表TCP协议)给tcp_client创建客户端套接字
#     tcp_client.connect(server_ip_port)              #第二步：客户端连接服务器端的IP和端口
#
#     # while True:                              #第三步：给发消息和收消息加上循环可以循环发收消息
#     if 1:
#         # msg=input('>>: ').strip()            #第四步：客户端让用户输入方式发消息
#         msg = str(time.strftime("%Y-%m-%d %H:%M:%S ", time.localtime())) + message
#         # if not msg:continue                  #第五步：客户端做判断如果输入为空从新输入
#         tcp_client.send(msg.encode('utf-8')) #第六步：客户端把用户输入的消息进行二进制编码给服务端的msg(socket发消息会从用户态内存send给内核态内存，发到内核态的内存由操作系统接收，操作系统操作网卡发送出去)
#         print('客户端已经发送消息')
#         data = tcp_client.recv(buffer_size)    #第七步：客户端接收服务端字节格式
#         print('收到服务端发来的消息',data.decode('utf-8'))  #通过解码看服务端发送的消息
#
#     tcp_client.close()                       #第八步：关闭客户端套接字
# if __name__ == '__main__':
#     for i in range(100):
#         t = threading.Thread(target=connect_to, args=())
#         t.start()
#     # connect_to("hello")


'''
Fuction：客户端发送图片和数据
Date：2018.9.8
Author：snowking
'''
###客户端client.py
import socket
import os
import sys
import struct
server_send_seq = "\n"

ip_addr = '192.168.1.102'
port = 1987
buffer_size = 1024
succeed_msg = "OK"

def sock_client_image():
    max_try = 5
    # while True:
    for i in range(max_try):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip_addr, port))  # 服务器和客户端在不同的系统或不同的主机下时使用的ip和端口，首先要查看服务器所在的系统网卡的ip
            # s.connect(('127.0.0.1', 6666))  #服务器和客户端都在一个系统下时使用的ip和端口
        except socket.error as msg:
            print(msg)
            print(sys.exit(1))
        # filepath = input('input the file: ')  # 输入当前目录下的图片名 xxx.jpg
        filepath = "image.png"
        fhead = struct.pack(b'128sq', bytes(os.path.basename(filepath), encoding='utf-8'),
                            os.stat(filepath).st_size)  # 将xxx.jpg以128sq的格式打包
        s.send(fhead)

        fp = open(filepath, 'rb')  # 打开要传输的图片
        while True:
            data = fp.read(buffer_size)  # 读入图片数据
            if not data:
                print('{0} send over...'.format(filepath))
                break
            s.send(data)  # 以二进制格式发送图片数据



        print('客户端已经发送消息')
        data = s.recv(buffer_size)  # 第七步：客户端接收服务端字节格式
        rec_msg = data.decode('utf-8')
        print('收到服务端发来的消息', rec_msg)  # 通过解码看服务端发送的消息
        rec_msg_list = rec_msg.split(server_send_seq)
        if rec_msg_list[0] == succeed_msg:
            s.close()
            break
        else:
            print("connect_to error")
            continue
        s.close()
        # break    #循环发送


if __name__ == '__main__':
    sock_client_image()