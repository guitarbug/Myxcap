# This script provides an example to access xcap through
# python, tcl communicates with xcap.exe through an udp
# socket, which is listened by xcap.exe on port 48765,
# python may use the same way as tcl to communicate with
# xcap.exe.

#
#    char buf[8192];
#    int len = recvfrom(socket, buf, sizeof(buf), 0, ...);
#    char *argv[128];
#    int argc = 0;
#    int i;
#    int c = *(int *)buf;
#    int n = 4;
#    for (i=0; i<c; i++)
#    {
#        argv[argc++] = buf + n;
#        n += (strlen(buf+n) + 1);
#    }
#
# All commands supported by xcap.exe:
# xcap setmode [net|local]
#      {startif | stopif} <0-31>
#      {startcap | stopcap} <0-31>
#      setfilter <0-31> <filter>
#      {startgrp | stopgrp} <grpindex>
#      creategrp <name>
#      createpkt <grpindex> <name> <item1> ... <itemN>
#      deletegrp <grpindex>
#      deletepkt <grpindex> <pktindex>
#      enablepkt <grpindex> <pktindex> <true|false>
#      sendpkt <0-31> <grpindex> <pktindex> [<inc>]
#      sendpkt <0-31> <hex-packet-string>
#      getpkt <grpindex> <pktindex>
#      recvpkt <0-31>
#      clearpkt [<0-31>]
#      getdata <grpindex> <pktindex> <hdrindex> <offset> <length> [hex|str|int|mac|ipv4|ipv6]
#      setdata <grpindex> <pktindex> <hdrindex> <offset> <length> <data> [hex|str|int|mac|ipv4|ipv6]
#      resetdata <grpindex> <pktindex> <hdrindex> <data>
#      checksum <data>
#      addarp <ipaddress> <mac>
#      delarp <ipaddress> <mac>
#      -host <host>:<port>
#
# e.g. to communicate with xcap.exe, you may input:
#     xcap startif 0
#


from socket import *

TCL_HOST = "127.0.0.1"
TCL_PORT = 48765

s = socket(AF_INET, SOCK_DGRAM)
addr = (TCL_HOST, TCL_PORT)

while True:
    # Please input a command here
    cmd = input("Please input command:")
    if cmd == "quit":
        break

    w = cmd.split()
    bytes = bytearray()
    n = len(w)

    # 4 bytes of length
    for i in range(4):
        bytes.append(int(n % 256))
        n = n / 256

    # command and args
    for e in w:
        bytes.extend(e.encode('latin-1'))
        bytes.append(0)

    # output command and args
    print(bytes)

    # send the command and args to xcap.exe
    s.sendto(bytes, addr)

    # wait for reponse from xcap.exe
    data, address = s.recvfrom(1024)
    print(data, address)

s.close()
