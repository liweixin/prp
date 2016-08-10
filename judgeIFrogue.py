# -*- coding: cp936 -*-
#coding = utf-8

import dbOperations

results = dbOperations.selectAPFeatures()
list = []
for result in results:
    list.append({"bssid":result["bssid"],
                        "ssid":result["ssid"],
                        "security":result["security"],
                        "signal":result["signals"],
                        "latitude":result["latitude"],
                        "longtitude":result["longtitude"],
                        "macAdress":result["macAdress"],
                        "timeString":result["timeString"]} )
    
def seeifexist(AP):
    all = len(list)
    flag = 0 #1 for totally same record
    for i in range(0, all):
        if(flag == 0):
            if(list[i]['ssid']==AP['ssid'] and list[i]['bssid']==AP['bssid'] and list[i]['security']==AP['security']):
                flag = 1
        else:
            break
    if(flag == 1): return list[i-1]['trust']
    else: return -10 #no record in

def judgessid(AP):
    all = len(list)
    ssid_trust = 1 #0 for trusted
    for i in range(0, all):
        if(list[i]['ssid']==AP['ssid']):
            ssid_trust = 0
            break
    return ssid_trust

def judgebssid(AP):
    all = len(list)
    bssid_trust = 1 #0 for trusted
    b = AP['bssid'].split(':')
    for i in range(0, all):
        a= list[i]['bssid'].split(':')
        if(a[0] == b[0] and a[1] == b[1] and a[2] == b[2]):
            bssid_trust = 0
            break
    return bssid_trust
        

def judgesignal(AP):
    all = len(list)
    signal_str = []
    for i in range(0, all):
        signal_str.append(list[i]['signal'])
    new_signal_str = sorted(signal_str)
    weakest = new_signal_str[all/4]
    strongest = new_signal_str[all*3/4]
    if(AP['signal']>=weakest and AP['signal']<=strongest):
        signal_trust = 0 #0 for trusted
    else:
        signal_trust = 1
    return signal_trust

def judgesecurity(AP):
    security_trust = 1 #0 for trusted
    a=''
    if(AP['security']!=''):
        a= AP['security'].split('-')[0].split('[')[1]
    if(a=='WPA' or a=='WPA2' or a=='WEP'):
        security_trust =0
    else:
        security_trust =1
    return security_trust

def addAPSafety(ap):
    all = len(ap)
    for i in range(0,all):
        #if(seeifexist(ap[i])!= -10):
        if(False):
            print ap[i]['ssid'],ap[i]['bssid'],"turst:",seeifexist(ap[i])
        else:
            if(judgessid(ap[i])+judgebssid(ap[i])+judgesignal(ap[i])+judgesecurity(ap[i])>=2):
                dbOperations.insertSafety(ap[i]['bssid'],1)
            else:
                dbOperations.insertSafety(ap[i]['bssid'],0)


