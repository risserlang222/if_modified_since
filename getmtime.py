# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 10:11:51 2021

@author: CyberUser
"""
import socket
import ssl
import pprint
from datetime import datetime
import csv
def getModifyStat(strdt, hostname, strurl):
    context = ssl.create_default_context()

    with socket.create_connection((hostname, 443)) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as ssock:
            cert = ssock.getpeercert()
            struli = "GET "  + strurl + " HTTP/1.1\r\nHost: " + hostname + "\r\nIf-Modified-Since: " + strdt + "\r\n\r\n"
            ssock.sendall(struli.encode('utf-8'))
            tmp = str(ssock.recv(1024)).split("\r\n")
#            pprint.pprint(tmp)
            tmp1 = str(tmp[0]).split(" ")
#            print('code= ' + tmp1[1])
            return tmp1[1]


if __name__ == '__main__':
    path = 'url_list.txt'
    try:
        with open(path, encoding='utf-8') as f:
            l = f.readlines()
        with open('output.csv', 'w', newline="", encoding='utf-8') as f2:
            output_csv = csv.writer(f2)

            for key in l:
                data = key.split('\t')
                u = data[0].split('/')
                dt = data[1].strip()
                try:
                    tdatetime = datetime.strptime(dt, '%Y/%m/%d %H:%M:%S')
                except(ValueError):
#                    print("この行にはエラーがあるのでスキップします。" + dt, file=f2)
                    print("この行にはエラーがあるのでスキップします。",file=f2)
                    continue

                dtstr = tdatetime.strftime('%a, %d %b %Y %H:%M:%S GMT')
                hostname = str(u[2])
                strurl = '/' + str(u[3])

#                print(dtstr,hostname,strurl)
                code = getModifyStat(dtstr,hostname,strurl)
                #print(code,strurl,dtstr)

                #with open('output.csv', 'w', newline="") as f2:
                #    output_csv = csv.writer(f2)
                print(str(code), str(strurl), str(dtstr), file=f2)
                    #output_csv.writerow([print(code,strurl,dtstr)])
                    #output_csv.writerow([str(code), str(strurl), str(dtstr)])
                #    pprint.pprint([code,strurl,dtstr], stream=f2)


    #                exit(1)
    except(FileExistsError):
        print("処理対象のファイルがありません。")
    finally:
        pass