# -*- coding: utf-8 -*-
# SCPCli.py

import paramiko
from scp import SCPClient

class SCPCli(object):

    # class调用方法
    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def login(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(hostname = self.host, port = self.port, username = self.username, password = self.password)

        return self.ssh

    # 输入ssh命令并返回结果方法
    def exec_command(self, cmd):
        stdin, stdout, stderr = self.ssh.exec_command(cmd)

        return stdout.read().decode('utf-8')

    # 下载文件方法
    def download_file(self, remote_file, local_file):
        scp_download_file = SCPClient(self.ssh.get_transport())

        return scp_download_file.get(remote_file, local_file)

    # 上传文件方法
    def upload_file(self, local_file, remote_file):
        scp_upload_file = SCPClient(self.ssh.get_transport())
        
        return scp_upload_file.put(local_file, remote_file)
