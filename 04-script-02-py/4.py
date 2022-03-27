#!/usr/bin/env python3

import socket
from string import whitespace

hosts = ["drive.google.com", "mail.google.com", "google.com"]
fileList = []

with open('host_test.log') as file:
    for f in file:
        fileList.append(f)

with open('host_test.log', 'w+') as file:
    for i in hosts:
        result = socket.gethostbyname(i)
        added = 0
        for y in fileList:
            inList = y.find(" {}".format(i))
            if (inList != -1):
                ipstr=y.replace('\n', '').split("  ")[1].translate({None: whitespace})
                if (ipstr == result):
                    print(" {}  {}\n".format(i, result))
                    file.write(" {}  {}\n".format(i, result))
                    added = 1
                    break
                else:
                    print("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    file.write("[ERROR] {} IP mismatch: {}  {}\n".format(i, ipstr, result))
                    added = 1
                    break
        if (added == 0):
            print(" {}  {}\n".format(i, result))
            file.write(" {}  {}\n".format(i, result))