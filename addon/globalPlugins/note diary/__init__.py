# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import gui
import globalPluginHandler
import globalVars
import ui
import config
import os
import sys
import addonHandler
addonHandler.initTranslation()

from scriptHandler import script
from .addon_config.settings import noteDiarySettingsPanel
from .addon_gui.main_dialog import MainDialog

if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios")):
	os.mkdir(os.path.join(globalVars.appArgs.configPath, "diarios"))

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		# Call of the constructor of the parent class.
		super(GlobalPlugin, self).__init__()
		confspec = {
			"sounds": "boolean(default=True)",
			"crear": "boolean(default=True)",
			"borrar": "boolean(default=True)",
			"editar-cap": "boolean(default=True)",
			"guardar-cap": "boolean(default=True)",
			"pasar-cap": "boolean(default=True)",
			"pasar-diario": "boolean(default=True)",
			"busqueda_exitosa": "boolean(default=True)",
			"busqueda_fallida": "boolean(default=True)"
		}
		config.conf.spec['Note'] = confspec

		self._MainWindows = None

		if globalVars.appArgs.secure:
			return
		
		if hasattr(globalVars, "noteDiary"):
			self._MainWindows = globalVars.noteDiary
		else:
			self.runSleep()

	def runSleep(self):
		# item en el menú de herramientas y en el diálogo de configuración
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.menuItem = self.toolsMenu.Append(wx.ID_ANY, _("Note diary"), _("Abrir la ventana de Note diary"))
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.dlgPrincipal, self.menuItem)
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(noteDiarySettingsPanel)

	def terminate(self):
		try:
			self.toolsMenu.RemoveItem(self.menuItem)
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(noteDiarySettingsPanel)
		except Exception:
			pass
		try:
			self._MainWindows.Destroy()
		except Exception:
			pass

	def dlgPrincipal(self, event):
		if not self._MainWindows:
			self._MainWindows = MainDialog(gui.mainFrame)
		if not self._MainWindows.IsShown():
			gui.mainFrame.prePopup()
			self._MainWindows.Show()
			# si ya hay una instancia de la ventana principal, mostrar un mensaje
		else:
			ui.message(_("Ya hay una instancia de Note\tdiary abierta"))
	# Translators: Description for the input gesture panel
	@script(gesture=None, description= _("Abrir la lista de diarios"),
		# Translators: Category name in panel entry gestures
		category= _("Note diary"))
	def script_NoteDiary(self, gesture):
		wx.CallAfter(self.dlgPrincipal, None)