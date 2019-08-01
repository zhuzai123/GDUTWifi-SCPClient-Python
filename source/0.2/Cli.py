# -*- coding: utf-8 -*-
# Cli.py

import re
import paramiko
import time
from scp import SCPClient

class SCPCli(object):

    # class调用方法
    def __init__(self, host, port, username, password, timeout = 600):
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password
        self.timeout = timeout

    def login(self):
        transport = paramiko.Transport((self.host, self.port))
        transport.connect(
            username = self.username, 
            password = self.password
            )
        self.ssh = transport.open_session()
        self.ssh.settimeout(self.timeout)
        self.ssh.get_pty()
        self.ssh.invoke_shell()

        self.scp = paramiko.SSHClient()
        self.scp.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.scp.connect(
            hostname = self.host, 
            port = self.port, 
            username = self.username, 
            password = self.password
            )

    def logout(self):
        self.ssh.close()
        self.scp.close()
        
    # 输入ssh命令并返回结果方法
    def exec_command(self, cmd):
        p = re.compile('#')
        self.ssh.send(cmd)
        while(1):
            result = ''
            time.sleep(0.1)
            ret = self.ssh.recv(65535)
            ret = ret.decode('utf-8')
            result += ret
            if p.search(ret):
                break
        return result

    # 上传文件方法
    def upload_file(self, local_file, remote_file):
        scp_upload_file = SCPClient(self.scp.get_transport())
        
        return scp_upload_file.put(local_file, remote_file)

    # 下载文件方法
    def download_file(self, remote_file, local_file):
        scp_download_file = SCPClient(self.scp.get_transport())

        return scp_download_file.get(remote_file, local_file)
