# -*- coding: utf-8 -*-
# Copyright (C) 2022 - 2024 Johan G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import config
import os
from gui.settingsDialogs import SettingsPanel

import addonHandler
addonHandler.initTranslation()
# interface for the settings panel
class noteDiarySettingsPanel(SettingsPanel):
	# Translators: This is the label for the settings panel.
	title = _("Note Diary")
	def makeSettings(self, settingsSizer):
		# la casilla de verificación para activar y desactivar los sonidos
		self.soundsCheckBox = wx.CheckBox(self, label=_("Activar sonidos "))
		self.soundsCheckBox.SetValue(config.conf['Note']['sounds'])

		settingsSizer.Add(self.soundsCheckBox, border=10, flag=wx.ALL)

	def onSave(self):
		config.conf['Note']['sounds']=self.soundsCheckBox.GetValue()
