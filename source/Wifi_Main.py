# Wifi.py

import os
import re
import getpass
import subprocess
import SCPCli

# 执行命令性指令函数
def cmd(cmd):
    res = subprocess.Popen(cmd, shell = True, 
             stdin = subprocess.PIPE, 
             stdout = subprocess.PIPE, 
             stderr = subprocess.PIPE)
    out = res.stdout.read()
    err = res.stderr.read()

    return out, err

# 获取配置函数
def get_config():
    net_add = input('请输入网络地址(默认: 192.168.1.1) : ')    # 获取网络地址
    if net_add == '':
        net_add = '192.168.1.1'
    print('网络地址: ' + net_add + '\nPing...')

    cmdout, cmderr = cmd('ping ' + net_add + ' -n 2')
    cmdout = cmdout.decode('GBK')
    cmderr = cmderr.decode('GBK')
    ping = re.findall('.*?(\d+)ms', cmdout, re.S)
    if ping == []:
        print('目标错误或不可达')
    else:
        print('目标延迟: ' + ping[0])

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
    print('用户名: ' + username)
    password = getpass.getpass('请输入密码(默认: zzz) : ')    # 获取密码
    if password == '':
        password = 'zzz'

    return net_add, port, username, password

# 模式选择函数
def mode_select(dis_lenth):
    i = os.system("cls")
    print('-' * int((dis_lenth - 8) / 2) + '登录成功' + '-' * int((dis_lenth - 8) / 2))
    print('\n' + ' ' * dis_lenth + 'POWER BY ZZ')
    print('更改服务器登录信息请按 "Ctrl + C" ...\n ')
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
            if 0 < mode < 5:
                break
            else:
                print('输入有误, 请重新输入! ')
                continue
        except:
            print('输入有误, 请重新输入! ')
            continue

    if int(mode) == 4:
        i = os.system("cls")
        print('-' * dis_lenth)
        print('\n' + ' ' * dis_lenth + 'POWER BY ZZ')
        print('更改服务器登录信息请按 "Ctrl + C" ...\n ')
        print(' OpenWRT定制功能选择: \n')
        print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' |' + '{:^21}'.format('1. 无线SSID与密码修改') + '|' + '{:^22}'.format('2. Dr.com帐号密码修改') + '|')
        print(' |' + ' ' * int((dis_lenth - 4) / 2) + '|' + ' ' * int((dis_lenth - 4) / 2) + '|')
        print(' +' + '-' * int((dis_lenth - 4) / 2) + '+' + '-' * int((dis_lenth - 4) / 2) + '+')

        while(1):
            try:
                mode = 10 + int(input('\n请输入所需OpenWRT定制功能 Num : '))
                if 10 < mode < 13:
                    break
                else:
                    print('输入有误, 请重新输入! ')
                    continue
            except:
                print('输入有误, 请重新输入! ')
                continue

    return mode

# 程序功能函数
def work(dis_lenth, mode):
    i = os.system("cls")
    print('-' * dis_lenth)
    print('\n' + ' ' * dis_lenth + 'POWER BY ZZ')
    print('更改服务器登录信息请按 "Ctrl + C" ...\n ')


    

if __name__ == '__main__':
    dis_lenth = int(60)
    print('*' * (dis_lenth + 20))
    print('\n   本免费程序使用Python开发，利用ssh与sch协议与对端设备进行指令执行或文件传输\n')
    print('*' * (dis_lenth + 20))
    print(' ' * dis_lenth + 'POWER BY ZZ\n')

    while(1):
        try:
            net_add, port, username, password = get_config()

            while(1):
                try:
                    ssh = SCPCli.login(net_add, username, password, port)
                    mode = mode_select(dis_lenth)
                    work(dis_lenth, mode)
                    ssh.close()

                except KeyboardInterrupt as e:
                    break

                except Exception as e:
                    i = os.system("cls")
                    template = 'Error type: {0} . \nArguments:\n{1!r}'
                    message = template.format(type(e).__name__, e.args)
                    print('\n发生意外错误! 请检查程序输入或网络连接...\n\n' + message)
                
                    reboot = input('\n请按Enter重新执行程序, 否则程序将结束: ')
                    if reboot == '':
                        continue
                    else:
                        break

                except:
                    i = os.system("cls")
                    print('\n进程出错...\n\n')
                    break

        except KeyboardInterrupt as e:
            i = os.system("cls")
            print('\n程序已被 "Ctrl + C" 指令中断...\n\n')

            reboot = input('\n请按Enter重新执行程序, 否则程序将结束: ')
            if reboot == '':
                continue
            else:
                break

        except:
            i = os.system("cls")
            print('\n进程出错...\n\n')
            break

# print(os.getcwd())