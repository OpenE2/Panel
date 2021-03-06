import os
from Plugins.Plugin import PluginDescriptor
from Components.Input import Input
from Screens.ChoiceBox import ChoiceBox
from Components.ActionMap import ActionMap
from Screens.InputBox import InputBox
from Components.ActionMap import ActionMap, NumberActionMap
from Components.FileList import FileList
from Components.Button import Button
from Components.Label import Label
from Components.config import config, configfile, ConfigYesNo, ConfigSubsection, getConfigListEntry, ConfigSelection, ConfigNumber, ConfigText, ConfigInteger
from Components.MenuList import MenuList
from Screens.Screen import Screen
from Screens.MessageBox import MessageBox
from Screens.Console import Console
import gettext
from Screens.PanelTextexit import PanelTextexit

try:
	cat = gettext.translation('Satdreamgr-Panel', '/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/locale', [config.osd.language.getText()])
	_ = cat.gettext
except IOError:
	pass

def main(session,**kwargs):
    try:
     	session.open(HardwareInfo)
    except:
        print "[Hardware] Pluginexecution failed"

def autostart(reason,**kwargs):
    if reason == 0:
        print "[PluginMenu] no autostart"

def menu(menuid, **kwargs):
	if menuid == "none":
		return [(_("Hardware Info"), main, "harware_setup", 45)]
	return []

def Plugins(**kwargs):
	return PluginDescriptor(name = _("Hardware Info"), description = _("Hardware Info"), where = PluginDescriptor.WHERE_MENU, fnc = menu)

hardware_main = """<screen name="HardwareInfo" position="center,center" size="600,405" >
                   <widget name="menu" itemHeight="35" position="20,10" size="580,330" scrollbarMode="showOnDemand" transparent="1" zPosition="9"/>
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/red.png" position="80,360" size="32,32" zPosition="1" alphatest="blend"/>
                   <ePixmap pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Satdreamgr-Panel/images/green.png" position="240,360" size="32,32" zPosition="1" alphatest="blend"/>
                   <widget name="key_red" position="110,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   <widget name="key_green" position="270,360" size="80,32" valign="center" halign="center" zPosition="1" font="Regular;22" transparent="1" />
                   </screen>"""

class HardwareInfo(Screen):

	def __init__(self, session):
		self.skin = hardware_main
		Screen.__init__(self, session)
		self.session = session
		menu = []
		menu.append((_("System Information"),"system"))
		menu.append((_("DVB Modules"),"modules"))
		menu.append((_("Netstat"),"netstat"))
		menu.append((_("Ifconfig"),"ifconfig"))
		menu.append((_("Internet Connectivity Test"),"internet"))
		menu.append((_("V. SecondStage Loader"),"Second"))
		menu.append((_("ipkg list installed"),"listinstalled"))
		menu.append((_("Show All Devices"),"devices"))
		menu.append((_("Show Mounts"),"mounts"))
		menu.append((_("Remove crashlogs"),"crashlogs"))
		menu.append((_("Create debug log"),"debuglog"))
        	self["menu"] = MenuList(menu)
        	self["key_red"] = Label(_("Exit"))
        	self["key_green"] = Label(_("Ok"))
        	self.setup_title = _("Hardware Info")
        	self.onLayoutFinish.append(self.layoutFinished)
        	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "WizardActions", "DirectionActions"],{"ok": self.go, "red": self.close, "green": self.go, "back": self.close,}, -1)
    	def go (self):
    		if self["menu"].l.getCurrentSelection() is not None:
        		choice = self["menu"].l.getCurrentSelection()[1]
			if choice == "system":
                         self.session.open(system_info)
			if choice == "modules":
				self.session.open(PanelTextexit, _("DVB Modules"),["opkg list_installed | grep dvb-modules"])
			if choice == "netstat":
				self.session.open(PanelTextexit, _("Netstat"), ["netstat | grep tcp && netstat | grep unix"])
			if choice == "ifconfig":
				self.session.open(PanelTextexit, _("Ifconfig"),["ifconfig"])
			if choice == "internet":
				self.session.open(PanelTextexit, _("Internet Connectivity Test"),["ping -c 1 www.satdreamgr.com && ping -c 1 www.google.com"])
			if choice == "Second":
				self.session.open(PanelTextexit, _("Your Version SecondStage Loader Installed"),["opkg list | grep second"])
			if choice == "listinstalled":
				self.session.open(PanelTextexit, _("opkg list installed"),["opkg list_installed"])
			if choice == "devices":
				self.session.open(PanelTextexit, _("Info All Devices"),["df -h"])
			if choice == "mounts":
				self.session.open(PanelTextexit, _("Info Mounts Devices"),["mount"])
			if choice == "crashlogs":
				self.session.openWithCallback(self.removeCRASH, MessageBox,_("Do you really wish to run this command?"), MessageBox.TYPE_YESNO)				
			if choice == "debuglog":
				self.session.openWithCallback(self.debugLOG, MessageBox,_("Do you really wish to run this command?"), MessageBox.TYPE_YESNO)

	def debugLOG(self, answer):
		if answer is True:
			os.system("dmesg > /tmp/sdg.debug.log && lsusb >> /tmp/sdg.debug.log && lsmod >> /tmp/sdg.debug.log && cat /proc/bus/nim_sockets >> /tmp/sdg.debug.log")
			configfile.save()
			self.showInfo()
		else:
			self.close()
			
	def removeCRASH(self, answer):
		if answer is True:
			os.system("rm -rf /media/hdd/enigma2_crash*")
			configfile.save()
			self.showInfo()
		else:
			self.close()			

	def showInfo(self):
		msg = _("Execution finished")
		self.session.open(MessageBox, msg, MessageBox.TYPE_INFO, timeout = 5)

	def layoutFinished(self):
		self.setTitle(self.setup_title)

hardware_main_info = """<screen name="HardwareInfobis" position="center,center" size="640,480">
    <ePixmap position="20,30" zPosition="5" size="50,50" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/ram.png" alphatest="blend" />
    <widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/bar.png" position="90,30" size="515,20" transparent="1" zPosition="6">
      <convert type="PanelSpaceInfo">MemTotal</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" zPosition="6" position="90,56" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
      <convert type="PanelSpaceInfo">MemTotal,Full</convert>
    </widget>
    <ePixmap position="20,110" zPosition="1" size="50,50" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/swap.png" alphatest="blend" />
    <widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/bar.png" position="90,110" size="515,20" transparent="1" zPosition="6">
      <convert type="PanelSpaceInfo">SwapTotal</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" zPosition="6" position="90,134" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
      <convert type="PanelSpaceInfo">SwapTotal,Full</convert>
    </widget>
    <ePixmap position="20,190" zPosition="1" size="50,50" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/flash.png" alphatest="blend" />
    <widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/bar.png" position="90,190" size="515,20" transparent="1" zPosition="6">
      <convert type="PanelSpaceInfo">FleshInfo</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" zPosition="6" position="90,213" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
      <convert type="PanelSpaceInfo">Flesh,Full</convert>
    </widget>
    <ePixmap position="20,270" zPosition="1" size="50,50" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/hdd.png" alphatest="blend" />
    <widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/bar.png" position="90,270" size="515,20" transparent="1" zPosition="6">
      <convert type="PanelSpaceInfo">HddInfo</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" zPosition="6" position="90,293" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
      <convert type="PanelSpaceInfo">HddInfo,Full</convert>
    </widget>
    <ePixmap position="20,350" zPosition="1" size="50,50" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/usb.png" alphatest="blend" />
    <widget source="session.Event_Now" render="Progress" pixmap="/usr/lib/enigma2/python/Plugins/Satdreamgr/Hardware/icons/bar.png" position="90,350" size="515,20" transparent="1" zPosition="6">
      <convert type="PanelSpaceInfo">UsbInfo</convert>
    </widget>
    <widget source="session.CurrentService" render="Label" zPosition="6" position="90,378" size="515,26" halign="left" valign="center" font="Regular; 23" transparent="0">
      <convert type="PanelSpaceInfo">UsbInfo,Full</convert>
    </widget>
     <widget backgroundColor="#000015" font="Regular; 23" foregroundColor="green" halign="center" position="20,440" render="Label" size="120,23" source="session.CurrentService" transparent="1" zPosition="1" valign="center">
      <convert type="PanelCpuUsage">Total</convert>
    </widget>
	</screen>"""

class system_info(Screen):

	def __init__(self, session):
		self.skin = hardware_main_info
		Screen.__init__(self, session)
		self.session = session

        	self.setup_title = _("Hardware Info")
        	self.onLayoutFinish.append(self.layoutFinished)
        	self["actions"] = ActionMap(["OkCancelActions", "ColorActions", "WizardActions", "DirectionActions"],{"ok": self.close, "back": self.close,}, -1)

	def layoutFinished(self):
		self.setTitle(self.setup_title)
