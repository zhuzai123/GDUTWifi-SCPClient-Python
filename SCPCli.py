# SCPCli.py

import paramiko
from scp import SCPClient

# ssh登录函数
def login(ip, username, password, port):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname = ip, port = port, username = username, password = password)

    return ssh

# 函数输入ssh命令并返回结果
def exec_command(ssh, command):
    stdin, stdout, stderr = ssh.exec_command(command)

    return stdout.read().decode('utf-8')

# 函数下载文件
def download_file(ssh, remote_file_path, remote_file_name, local_file_path, local_file_name):
    remote = remote_file_path + remote_file_name
    local = local_file_path + local_file_name
    scp_download_file = SCPClient(ssh.get_transport())

    return scp_download_file.get(remote, local)

# 函数上传文件
def upload_file(ssh, local_file_path, local_file_name, remote_file_path, remote_file_name):
    local = local_file_path + local_file_name
    remote = remote_file_path + remote_file_name
    scp_upload_file = SCPClient(ssh.get_transport())
    
    return scp_upload_file.put(local, remote)
