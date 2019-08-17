# -*- coding: utf-8 -*-
# wifi_main.py

import os
import re
import time
import getpass
import subprocess
import paramiko
from scp import SCPClient

class SCPCli(object):
    # 创建配置方法
    def set_conf(self, host, port, username, password, timeout=600):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

     # 登入方法
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
        self.ssh_channel.send(cmd + '\n')

    # 上传文件方法
    def upload_file(self, local_file, remote_file):
        self.scp_file_transfer.put(local_file, remote_file)

    # 下载文件方法
    def download_file(self, remote_file, local_file):
        self.scp_file_transfer.get(remote_file, local_file)

# 错误触发
class RunError(Exception):
    pass

# Windows执行命令行指令函数
def cmd(cmd):
    res = subprocess.Popen(
        cmd, shell=True,
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
        )
    out = res.stdout.read()
    err = res.stderr.read()

    return out, err

# 获取配置函数
def get_config():
    os.system("cls")
    print('*' * (dis_lenth + 20))
    print('\n   本免费程序使用Python开发，利用ssh与sch协议与对端设备进行指令执行\n')
    print('*' * (dis_lenth + 20) + '\n' + ' ' * (dis_lenth + 4) + 'POWERED BY GTLWIFI')
    while(1):
        net_add = input('请输入网络地址(默认: 192.168.1.1) : ')    # 获取网络地址
        if net_add == '':
            net_add = '192.168.1.1'
        print('网络地址: ' + net_add + '\nPing...')
        cmdout, cmderr = cmd('ping ' + net_add + ' -w 1000 -n 1')
        cmdout = cmdout.decode('GBK')
        cmderr = cmderr.decode('GBK')
        ping = re.findall('.*?(\d+)ms', cmdout, re.S)
        if ping == []:
            print('目标错误或不可达\n')
        else:
            print('目标延迟: ' + ping[0] + 'ms')
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
    client = SCPCli()
    client.set_conf(net_add, int(port), username, password)

    return client

# 功能选择函数
def mode_select(dis_lenth):
    os.system("cls")
    print('-' * int(dis_lenth) + '\n\n' + ' ' * (dis_lenth - 16) + 'POWERED BY GTLWIFI')
    print('更改服务器登录信息请输入 "0" ...\n\n 功能选择: \n')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' |' + '{:^21}'.format('1. 无线SSID与密码修改') + '|' + '{:^22}'.format('2. Dr.com帐号密码修改') + '|')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' |' + '{:^22}'.format('3. 登录密码修改') + '|' + '{:^24}'.format('4. 重启系统') + '|')
    print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
    print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
    while(1):
        try:
            mode = int(input('\n请输入所需功能 Num : '))
            if 0 <= mode <= 4:
                break
            else:
                print('输入有误, 请重新输入! ')
                continue
        except KeyboardInterrupt:
            exit(0)
        except:
            print('输入有误, 请重新输入! ')

    return str(mode)

# /etc/config/目录配置文件读写函数
def rw_config_file(client, config_name, write_content=''):
    if write_content == '':    # 读
        try:
            client.download_file('/etc/config/' + config_name, 
                                 os.getcwd() + '\\' + config_name)
            with open(os.getcwd() + '\\' + config_name, 'r', 
                      encoding='utf-8') as config_file:

                config_file_content = config_file.read()
            os.remove(os.getcwd() + '\\' + config_name)

            return config_file_content

        except:
            time.sleep(0.5)
            print('\n找不到对应的配置文件, 设备或配置文件可能不被支持')
            client.download_file('/etc/config/' + config_name, 
                                 os.getcwd() + '\\' + config_name)

    else:    # 写
        with open(os.getcwd() + '\\' + config_name, 'w', 
                  encoding='utf-8') as config_file:

            config_file.truncate()
            config_file.write(write_content)
        try:
            client.upload_file(os.getcwd() + '\\' + config_name, 
                               '/etc/config/' + config_name)
            print('\n配置修改正在提交.', end='')
            time.sleep(0.5)
            print('.', end='')
            time.sleep(0.5)
            print('.', end='')
        except:
            time.sleep(0.5)
            print('\n文件上传失败')
            client.upload_file(os.getcwd() + '\\' + config_name, 
                               '/etc/config/' + config_name)
        finally:
            os.remove(os.getcwd() + '\\' + config_name)

# 无线修改
class op_wireless(SCPCli):
    def work(self):
        # 读取文件并存储到临时副本
        wireless_content = rw_config_file(client, 'wireless')

        before_iface_list = \
            re.findall("config wifi-iface.*?mode 'ap'.*?\n\n|config wifi-iface.*?mode 'ap'.*", 
                       wireless_content, re.S)
        for i in range(len(before_iface_list)):
            before_iface_list[i] = re.sub("\s+$", 
                                          "", 
                                          before_iface_list[i])
        after_iface_list = before_iface_list.copy()

        if len(after_iface_list) == 0:
            print('\n当前设备无 Wifi 或不支持该设备...')
        else:
            # 遍历修改各个Wifi配置
            for i in range(len(after_iface_list)):
                # 创建字典并列出Wifi配置
                wifi_config_dict = {i:{}}
                try:
                    wifi_config_dict[i]['encryption'] = \
                        re.search("\toption encryption '(.*?)'", 
                                  after_iface_list[i]).group(1)
                except:
                    wifi_config_dict[i]['encryption'] = 'none'
                try:
                    wifi_config_dict[i]['ssid'] = \
                        re.search("\toption ssid '(.*?)'", 
                                  after_iface_list[i]).group(1)
                except:
                    pass
                try:
                    wifi_config_dict[i]['key'] = \
                        re.search("\toption key '(.*?)'", 
                                  after_iface_list[i]).group(1)
                except:
                    pass
                print('\n当前: ')
                if wifi_config_dict[i]['encryption'] == 'none':
                    print('\nWifi\0' + str(i + 1) + '\0无加密')
                
                    if 'ssid' in wifi_config_dict[i]:
                        print('Wifi\0' + str(i + 1) + '\0的SSID为: ' + \
                            str(wifi_config_dict[i]['ssid']))
                    else:
                        print('Wifi\0' + str(i + 1) + '\0无SSID')
                
                    if 'key' in wifi_config_dict[i]:
                        print('Wifi\0' + str(i + 1) + '\0的密码为: ' + \
                            str(wifi_config_dict[i]['key']))
                    else:
                        print('Wifi\0' + str(i + 1) + '\0无密码')
                else:
                    print('\nWifi\0' + str(i + 1) + '\0的加密为: ' + \
                        str(wifi_config_dict[i]['encryption']))
                
                    if 'ssid' in wifi_config_dict[i]:
                        print('Wifi\0' + str(i + 1) + '\0的SSID为: ' + \
                            str(wifi_config_dict[i]['ssid']))
                    else:
                        print('Wifi\0' + str(i + 1) + '\0无SSID')

                    if 'key' in wifi_config_dict[i]:
                        print('Wifi\0' + str(i + 1) + '\0的密码为: ' + \
                            str(wifi_config_dict[i]['key']))
                    else:
                        print('Wifi\0' + str(i + 1) + '\0无密码')
                # 修改
                if input('\n是否需要更改当前 Wifi ' + str(i + 1) + \
                    ' 的设置?\n输入 1 并轻敲回车更改, 不需更改请直接轻敲回车: ') == '1':
                    if len(after_iface_list) >= 2:
                        print('\n检测到当前设备有多个 Wifi , 建议对不同 Wifi 添加适当后缀以区分... ')
                    new_encry = input('\n是否需要更改当前 Wifi ' + str(i + 1) + \
                        ' 的加密?\n输入 1 并轻敲回车启用WPA加密, 输入 2 并轻敲回车禁用加密, 不需更改请直接轻敲回车: ')

                    if new_encry == '1':
                        wifi_config_dict[i]['encryption'] = 'psk-mixed'
                    elif new_encry == '2':
                        wifi_config_dict[i]['encryption'] = 'none'

                    if 'ssid' in wifi_config_dict[i]:
                        new_ssid = input('\n是否需要更改当前 Wifi ' + str(i + 1) + \
                            ' 的SSID?\n更改请直接输入新的SSID并轻敲回车, 不需更改请直接轻敲回车: ')
                        if new_ssid != '':
                            wifi_config_dict[i]['ssid'] = new_ssid
                    else:
                        wifi_config_dict[i]['ssid'] = input('\n请设置当前 Wifi ' + str(i + 1) + \
                            ' 的SSID\n输入新的SSID并轻敲回车: ')

                    if wifi_config_dict[i]['encryption'] == 'psk-mixed':
                        if 'key' in wifi_config_dict[i]:
                            new_key = input('\n是否需要更改当前 Wifi ' + str(i + 1) + \
                                ' 的密码?\n更改请直接输入新的密码并轻敲回车, 不需更改请直接轻敲回车: ')
                            if new_key != '':
                                wifi_config_dict[i]['key'] = new_key
                        else:
                            wifi_config_dict[i]['key'] = \
                                input('\n请设置当前 Wifi ' + str(i + 1) + \
                                ' 的密码\n输入新的密码并轻敲回车: ')
                    elif wifi_config_dict[i]['encryption'] == 'none':
                        wifi_config_dict[i].pop('key', 2)
                    # 应用到字典
                    after_iface_list[i] = re.sub("\toption encryption '.*?'", 
                                                 "\toption encryption '" + \
                                                     wifi_config_dict[i]['encryption'] + "'", 
                                                 after_iface_list[i])

                    if 'ssid' in wifi_config_dict[i]:
                        if "option ssid '" in after_iface_list[i]:
                            after_iface_list[i] = re.sub("\toption ssid '.*?'", 
                                                         "\toption ssid '" + \
                                                             wifi_config_dict[i]['ssid'] + "'", 
                                                         after_iface_list[i])
                        else:
                            after_iface_list[i] = re.sub("'$", 
                                                         "'\n\toption ssid '" + \
                                                             wifi_config_dict[i]['ssid'] + "'", 
                                                         after_iface_list[i])
                    else:
                        after_iface_list[i] = re.sub("\n\toption ssid '.*?'", 
                                                     "", after_iface_list[i])

                    if 'key' in wifi_config_dict[i]:
                        if "option key '" in after_iface_list[i]:
                            after_iface_list[i] = re.sub("\toption key '.*?'", 
                                                         "\toption key '" + \
                                                             wifi_config_dict[i]['key'] + "'", 
                                                         after_iface_list[i])
                        else:
                            after_iface_list[i] = re.sub("'$", 
                                                         "'\n\toption key '" + \
                                                             wifi_config_dict[i]['key'] + "'", 
                                                         after_iface_list[i])

                    else:
                        after_iface_list[i] = re.sub("\n\toption key '.*?'", 
                                                     "", after_iface_list[i])
                # 应用到文件临时副本
                if before_iface_list[i] != after_iface_list[i]:
                    wireless_content = re.sub(before_iface_list[i], 
                                              after_iface_list[i], 
                                              wireless_content)
                os.system("cls")
            print('\n**********以下为配置文件内容**********')
            print(wireless_content)
            print('**********以上为配置文件内容**********')
            # 应用到文件
            if after_iface_list != before_iface_list:
                rw_config_file(client, 'wireless', wireless_content)
                client.send_command('wifi up')

# Dr.com修改
class op_drcom(SCPCli):
    def work(self):
        # 读取文件并存储到临时副本
        gdut_drcom_content = rw_config_file(client, 'gdut_drcom')
        after_drcom = before_drcom = re.sub("\s+$", 
                              "", re.search("config gdut_drcom.*?\n\n|config gdut_drcom.*", 
                                            gdut_drcom_content, re.S).group())
        if len(after_drcom) == 0:
            print('\n当前设备无 Dr.com 或不支持该设备...')
        else:
            # 创建字典并列出Dr.com配置
            drcom_config_dict = {}
            try:
                drcom_config_dict['username'] = re.search("\toption username '(.*?)'", 
                                                          after_drcom).group(1)
            except:
                pass
            try:
                drcom_config_dict['password'] = re.search("\toption password '(.*?)'", 
                                                          after_drcom).group(1)
            except:
                pass
    
            print('\n当前: ')
            if 'username' in drcom_config_dict:
                print('\nDr.com的用户名为: ' + str(drcom_config_dict['username']))
            else:
                print('\nDr.com无用户名')

            if 'password' in drcom_config_dict:
                print('Dr.com的密码为: ' + str(drcom_config_dict['password']))
            else:
                print('Dr.com无密码')
            # 修改
            if input('\n是否需要更改当前 Dr.com 的设置?\n\
    输入 1 并轻敲回车更改, 不需更改请直接轻敲回车: ') == '1':

                if 'username' in drcom_config_dict:
                    new_username = input('\n是否需要更改当前 Dr.com 的用户名?\n\
    更改请直接输入新的用户名并轻敲回车, 不需更改请直接轻敲回车: ')
                else:
                    new_username = input('\n请设置当前 Dr.com 的用户名\n\
    输入新的SSID并轻敲回车, 不需设置请直接轻敲回车: ')
                if new_username != '':
                    drcom_config_dict['username'] = new_username

                if 'password' in drcom_config_dict:
                    new_password = input('\n是否需要更改当前 Dr.com 的密码?\n\
    更改请直接输入新的密码并轻敲回车, 不需更改请直接轻敲回车: ')
                else:
                    new_password = input('\n请设置当前 Dr.com 的密码\n\
    输入新的密码并轻敲回车, 不需设置请直接轻敲回车: ')
                if new_password != '':
                    drcom_config_dict['password'] = new_password
                # 应用到字典
                if 'username' in drcom_config_dict:
                    if "option username '" in after_drcom:
                        after_drcom = re.sub("\toption username '.*?'", 
                                             "\toption username '" + \
                                                 drcom_config_dict['username'] + "'", 
                                             after_drcom)
                    else:
                        after_drcom = re.sub("'$", 
                                             "'\n\toption username '" + \
                                                 drcom_config_dict['username'] + "'", 
                                             after_drcom)

                if 'password' in drcom_config_dict:
                    if "option password '" in after_drcom:
                        after_drcom = re.sub("\toption password '.*?'", 
                                                "\toption password '" + \
                                                    drcom_config_dict['password'] + "'", 
                                                after_drcom)
                    else:
                        after_drcom = re.sub("'$", 
                                                "'\n\toption password '" + \
                                                    drcom_config_dict['password'] + "'", 
                                                after_drcom)
                # 应用到文件临时副本
                gdut_drcom_content = re.sub(before_drcom, 
                                            after_drcom, 
                                            gdut_drcom_content)
            os.system("cls")
            print('\n**********以下为配置文件内容**********')
            print(gdut_drcom_content)
            print('**********以上为配置文件内容**********')
            # 应用到文件
            if after_drcom != before_drcom:
                rw_config_file(client, 'gdut_drcom', gdut_drcom_content)
                client.send_command('/etc/init.d/gdut-drcom restart')

# 登录密码修改
class op_passwd(SCPCli):
    def work(self):
        if input('\n是否需要更改当前登录密码?\n\
    输入 1 并轻敲回车更改, 不需更改请直接轻敲回车: ') == '1':
            while(1):
                new_passwd = getpass.getpass('\n请输入新密码: ')
                if new_passwd == getpass.getpass('\n请再次输入密码: '):
                    break
                else:
                    os.system("cls")
                    print('\n密码不匹配，请重新输入')
            client.send_command('passwd\n')
            time.sleep(0.2)
            client.send_command(new_passwd + '\n')
            time.sleep(0.2)
            client.send_command(new_passwd + '\n\n')
            print('\n登录密码已修改，稍后请更改服务器登录信息')

# 重启
class op_reboot(SCPCli):
    def work(self):
        if input('\n重启将断开设备的网络连接, 是否需要重启?\n\
    输入 1 并轻敲回车重启, 不需重启请直接轻敲回车: ') == '1':
            client.send_command('reboot\n')
            print('\n设备即将重启！')
            time.sleep(0.6)
            client.logout()

# 主函数
if __name__ == '__main__':
    dis_lenth = 60
    client = get_config()
    while(1):
        try:
            while(1):
                client.login()
                mode = mode_select(dis_lenth)
                if mode == '0':
                    client = get_config()
                    continue
                # 程序功能执行
                os.system("cls")
                switch = {
                    '1': [op_wireless],
                    '2': [op_drcom],
                    '3': [op_passwd],
                    '4': [op_reboot]
                    }
                run_func = switch[mode][0]()
                run_func.work()
                # 执行完成
                mode = input(
                    '\n执行完成，轻敲回车继续执行其他功能，输入 "0" 更改服务器登录信息: ')
                if mode == '0':
                    client = get_config()
                print('正在登陆...')
        except KeyboardInterrupt:
            exit(0)
        except Exception as e:
            template = 'Error type: {0} . \n\nArguments:\n{1!r}'
            err_message = template.format(type(e).__name__, e.args)
            print('\n发生错误! 请检查程序输入或与设备的网络连接...\n\n' + err_message)
            mode = input('\n轻敲回车重新登录，输入 "0" 更改服务器登录信息: ')
            if mode == '0':
                client = get_config()
        except:
            break
    exit(0)
