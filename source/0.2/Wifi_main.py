# -*- coding: utf-8 -*-
# Wifi_main.py

import os
import re
import getpass
import subprocess
from Cli import *

class RunError(Exception):
    pass

# 执行命令性指令函数
def cmd(cmd):
    res = subprocess.Popen(
        cmd, shell = True, 
        stdin = subprocess.PIPE, 
        stdout = subprocess.PIPE, 
        stderr = subprocess.PIPE
        )
    out = res.stdout.read()
    err = res.stderr.read()

    return out, err

# 获取配置函数
def get_config():
    os.system("cls")
    print('*' * (dis_lenth + 20))
    print('\n   本免费程序使用Python开发，利用ssh与sch协议与对端设备进行指令执行或文件传输\n')
    print('*' * (dis_lenth + 20))
    print(' ' * dis_lenth + 'POWER BY ZZ\n')
    while(1):
        net_add = input('请输入网络地址(默认: 192.168.1.1) : ')    # 获取网络地址
        if net_add == '':
            net_add = '192.168.11.2'
        print('网络地址: ' + net_add + '\nPing...')
        cmdout, cmderr = cmd('ping ' + net_add + ' -w 1500 -n 1')
        cmdout = cmdout.decode('GBK')
        cmderr = cmderr.decode('GBK')
        ping = re.findall('.*?(\d+)ms', cmdout, re.S)
        if ping == []:
            print('目标错误或不可达\n')
        else:
            print('目标延迟: ' + ping[0])
            break

    
    port = input('\n请输入网络端口(默认: 22) : ')    # 获取网络端口
    try:
        port_num = int(port)
        if 0 < port_num < 65556:
            port = port
        else:
            port = '22'
    except:
        port = '22'
    print('网络端口: ' + port)
    username = input('\n请输入用户名(默认: root) : ')    # 获取用户名
    if username == '':
        username = 'root'
    print('用户名: ' + username + '\n')
    password = getpass.getpass('请输入密码(默认: zzz) : ')    # 获取密码
    if password == '':
        password = 'zzz'

    return net_add, port, username, password

# 模式选择函数
def mode_select(dis_lenth):
    os.system("cls")
    print('-' * int((dis_lenth - 8) / 2) + '登录成功' + '-' * int((dis_lenth - 8) / 2))
    print('\n' + ' ' * dis_lenth + 'POWER BY ZZ')
    print('更改服务器登录信息请输入 "0" ...\n ')
    print(' 功能选择: \n')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' |' + '{:^24}'.format('1. SSH发送指令') + '|' + '{:^24}'.format('2. SCP上传文件') + '|')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' |' + '{:^24}'.format('3. SCP下载文件') + '|' + '{:^24}'.format('4. OpenWRT定制功能') + '|')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    while(1):
        try:
            mode = int(input('\n请输入所需功能 Num : '))
            if 0 <= mode < 5:
                break
            else:
                print('输入有误, 请重新输入! ')
                continue
        except:
            print('输入有误, 请重新输入! ')
            continue

    if mode == 4:
        os.system("cls")
        print('-' * dis_lenth)
        print('\n' + ' ' * dis_lenth + 'POWER BY ZZ')
        print('更改服务器登录信息请输入 "0" ...\n ')
        print(' OpenWRT定制功能选择: \n')
        print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' |' + '{:^21}'.format('1. 无线SSID与密码修改') + '|' + '{:^22}'.format('2. Dr.com帐号密码修改') + '|')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' |' + '{:^24}'.format('3. 重启系统') + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
        while(1):
            try:
                mode = 40 + int(input('\n请输入所需OpenWRT定制功能 Num : '))
                if 39 < mode < 44:
                    break
                else:
                    print('输入有误, 请重新输入! ')
                    continue
            except:
                print('输入有误, 请重新输入! ')
                continue

    return mode

def exec_command(para):
    cmd = ''
    try:
        while(1):
            print(client.exec_command(cmd), end = '')
            cmd = input('') + '\n'
    except KeyboardInterrupt as e:
        print('')
        pass
    except:
        raise RunError('Run shell faild! ')

def upload_file(para):
    # client.upload_file('D:\\network', '/root/network')
    pass

def download_file(para):
    # client.download_file('/etc/config/network', 'D:\\network')
    pass

def op_wireless(para):
    pass

def op_drcom(para):
    pass

def op_reboot(para):
    client.exec_command('reboot')

# 程序功能执行函数
def run(dis_lenth, mode, client):
    os.system("cls")
    mode = str(mode)
    switch = {
        '1': [exec_command, ''],
        '2': [upload_file, ''],
        '3': [download_file, ''],
        '41': [op_wireless, ''],
        '42': [op_drcom, ''],
        '43': [op_reboot, '']
        }
    func = switch[mode][0]
    func(switch[mode][1])

if __name__ == '__main__':
    dis_lenth = int(60)
    while(1):
        host, port, username, password = get_config()
        client = SCPCli(host, port, username, password)
        mode = 0
        try:
            client.login()
            while(mode != '0'):
                mode = mode_select(dis_lenth)
                if mode % 10 == 0:
                    break
                run(dis_lenth, mode, client)
                mode = input('\n命令已执行完成，输入Enter继续执行其他功能，输入 "0" 更改服务器登录信息: ')
        except Exception as e:
            os.system("cls")
            print(type(e).__name__)
            print(e.args)
            template = 'Error type: {0} . \n\nArguments:\n{1!r}'
            err_message = template.format(type(e).__name__, e.args)
            print('\n发生错误! 请检查程序输入或网络连接...\n\n' + err_message)
            mode = input('\n输入Enter重新登录，输入 "0" 更改服务器登录信息: ')
        except:
            break
        client.logout()
    exit(0)