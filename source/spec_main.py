# -*- coding: utf-8 -*-
# spec_main.py

import paramiko
import sys

# windows does not have termios...
def interactive_shell(chan):
    windows_shell(chan)

def windows_shell(chan):
    import threading
    sys.stdout.write("Line-buffered terminal emulation. Press F6 or ^Z to send EOF.\r\n\r\n")
    def writeall(sock):
        while True:
            data = sock.recv(256)
            if not data:
                sys.stdout.write('\r\n*** EOF ***\r\n\r\n')
                sys.stdout.flush()
                break
            sys.stdout.write(data.decode())
            sys.stdout.flush()
    writer = threading.Thread(target=writeall, args=(chan,))
    writer.start()

    try:
        while True:
            d = sys.stdin.read(1)
            if not d:
                break
            chan.send(d)

    except EOFError:
        # user hit ^Z or F6
        pass

#建立ssh连接
ssh=paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect('192.168.1.1',port=22,username='admin',password='zzz')

#建立交互式shell连接
channel=ssh.invoke_shell()

#建立交互式管道
interactive.interactive_shell(channel)

#关闭连接
channel.close()
ssh.close()