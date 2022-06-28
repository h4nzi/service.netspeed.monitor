#!/usr/bin/python3

#odzkoušeno, funguje - dořešit konverzi na číslo
#https://www.daniweb.com/programming/threads/504783/convert-rx-tx-to-kbps
#https://www.daniweb.com/programming/threads/504783/convert-rx-tx-to-kbps + https://stackoverflow.com/questions/26573681/python-getting-upload-download-speeds


import time
import os
import sys
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon



def get_bytes(t, iface='eth0'):
    with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)

if __name__ == '__main__':
    (tx_prev, rx_prev) = (0, 0)
    
    while(True):
        try:
            tx = get_bytes('tx')
            rx = get_bytes('rx')
        except IOError:
            print("Cannot read the number of bytes received or transmitted through interface {}".format(args.iface))
            break
        if tx_prev > 0:
            tx_speed = (tx - tx_prev) / 2
            tx_b = round(tx_speed / 132072, 2)
            print('TX: ', tx_b, 'Mb/s')
            tx_a = str(tx_b)
            xbmcgui.Window(10000).setProperty('TX', tx_a)
        if rx_prev > 0:
            rx_speed = (rx - rx_prev) / 2
            rx_b = round(rx_speed / 132072, 2)
            print('RX: ', rx_b, 'Mb/s')
            rx_a = str(rx_b)
            xbmcgui.Window(10000).setProperty('RX', rx_a) #https://stackoverflow.com/questions/44622280/save-settings-value-accessible-globally-in-kodi
        time.sleep(2)
        tx_prev = tx
        rx_prev = rx
        