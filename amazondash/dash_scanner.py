#!/usr/bin/python3


from scapy.all import *

import time
import requests
import json
import random
import sys




class DashScanner():
    def __init__(self,filename=None,password="",ip="http://localhost:8123",mac=""):
        self.last_check_time = time.time()
        self.urlGR=ip+'/api/services/notify/bot_to_grcanosa'
        self.urlSA=ip+'/api/services/notify/bot_to_sara'
        self.headers={'x-ha-access': password, 'content-type': 'application/json'}
        self.data={'title': '<LOVEBOT>', 'message': ' Starting...'}
        self.sentences = [":)"]
        self.load_from_file(filename)
        self.mac = mac;
        req_ok = False
        startup_attemps = 1;
        while req_ok == False:
            time.sleep(1)
            try:
                self.data["message"] = "Starting ... "+str(startup_attemps); 
                requests.post(self.urlGR,headers=self.headers,json=self.data)
                req_ok = True;
            except requests.exceptions.RequestException as e:
                startup_attemps+= 1
                

    def load_from_file(self,filename):
        with open(filename) as f:
            for l in f:
                l = l.strip();
                self.sentences.append(l)

    def msg_admin(self, msg):
        self.data["message"] = msg
        requests.post(self.urlGR,headers=self.headers,json=self.data)
        
    def notify_hass(self):
        self.data["message"] = random.choice(self.sentences)
        requests.post(self.urlGR,headers=self.headers,json=self.data)
        requests.post(self.urlSA,headers=self.headers,json=self.data)


    def arp_scan(self,pkt):
        if pkt.haslayer(ARP):
            #print("Has layer ARP")
            if pkt[ARP].op == 1: #who-has (request)
                #print("WHO HAS "+pkt[ARP].hwsrc+"my mac "+self.mac+" equal "+str(pkt[ARP].hwsrc == self.mac))
                if pkt[ARP].hwsrc == self.mac:
                    #print("Probe from DASH")
                    tnow = time.time()
                    #print("Dash probe received, last time was "+str(tnow-self.last_check_time)+" seconds ago")
                    #print(pkt[ARP])
                    if tnow-self.last_check_time > 15:
                        self.notify_hass();
                        self.last_check_time = tnow;
                    else:
                        print("Too short time, repeated ARP")



if __name__ == "__main__":
  #print(sys.argv)
  dS = DashScanner(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  time.sleep(60)
  dS.msg_admin("Starting after 60s")
  sniff(prn=dS.arp_scan,filter="arp",store=0,count=0)
