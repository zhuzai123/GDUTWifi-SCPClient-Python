# -*- coding: utf-8 -*-
# Cli.py

import paramiko
import time
from scp import SCPClient

class SCPCli(object):
    # class调用方法
    def __init__(self, host, port, username, password, timeout=600):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

     # 登录方法
    def login(self):
        self.sshcli = paramiko.SSHClient()
        self.sshcli.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.sshcli.connect(
            self.host, 
            port=self.port, 
            username=self.username, 
            password=self.password
            )
        self.ssh_channel = self.sshcli.invoke_shell()
        self.scp_file_transfer = SCPClient(self.sshcli.get_transport())

    # 登出方法
    def logout(self):
        self.sshcli.close()

    # 发送ssh命令方法
    def send_command(self, cmd):
        cmd += '\n'
        self.ssh_channel.send(cmd)

    # 上传文件方法
    def upload_file(self, local_file, remote_file):
        self.scp_file_transfer.put(local_file, remote_file)

    # 下载文件方法
    def download_file(self, remote_file, local_file):
        self.scp_file_transfer.get(remote_file, local_file)
