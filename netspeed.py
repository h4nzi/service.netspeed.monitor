import time
import os
import sys
import xbmc
import xbmcgui
import xbmcaddon
import json

# Plugin Info

addon_id = 'service.netspeed.monitor'
selfAddon = xbmcaddon.Addon(addon_id)
__version__ = selfAddon.getAddonInfo('version')
monitor = xbmc.Monitor()

   
if selfAddon.getSetting('rozhrani') == '0':
    interface="eth0"
    print("interface = eth0")
elif selfAddon.getSetting('rozhrani') == '1':
    interface="wlan0"
    print("interface = wlan0")
else:
    print("Neznámé rozhraní a nebo není povoleno")

    
def get_bytes(t, iface=interface):
    with open('/sys/class/net/' + iface + '/statistics/' + t + '_bytes', 'r') as f:
        data = f.read();
    return int(data)

if __name__ == '__main__':
    (tx_prev, rx_prev) = (0, 0)
    monitor = xbmc.Monitor()
    while not monitor.abortRequested():
        # xbmc.log("*********Netspeed Running*****************", 1)
        try:
            tx = get_bytes('tx')
            rx = get_bytes('rx')
        except IOError:
            # print("Nelze číst počet bajtů přijatých nebo přenesených rozhraním {}".format(args.iface))
            break
        if tx_prev > 0:
            tx_speed = (tx - tx_prev) / 2
            tx_b = str(round(tx_speed / 132072, 2))
            # print('TX: ', tx_b, 'Mb/s')
            xbmcgui.Window(10000).setProperty('TX', tx_b)
        if rx_prev > 0:
            rx_speed = (rx - rx_prev) / 2
            rx_b = str(round(rx_speed / 132072, 2))
            # print('RX: ', rx_b, 'Mb/s')
            xbmcgui.Window(10000).setProperty('RX', rx_b)
        if monitor.waitForAbort(2):
            xbmc.log("********Netspeed Abort Called*****************", 2)
            break
        tx_prev = tx
        rx_prev = rx
        
