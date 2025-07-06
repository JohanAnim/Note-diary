# -*- coding: utf-8 -*-
# Copyright (C) 2022 - 2024 Johan G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import config
import os
import wx.adv
from gui.settingsDialogs import SettingsPanel
import gui
from gui.nvdaControls import CustomCheckListBox
import addonHandler
addonHandler.initTranslation()

class noteDiarySettingsPanel(SettingsPanel):
	# Translators: This is the label for the settings panel.
	title = _("Note Diary")

	def __init__(self, parent):
		self.sounds = {
			"crear": _("Crear un diario o capítulo"),
			"borrar": _("Borrar un diario o capítulo"),
			"editar-cap": _("Editar un capítulo"),
			"guardar-cap": _("Guardar un capítulo"),
			"pasar-cap": _("Pasar por los capítulos"),
			"pasar-diario": _("Pasar por los diarios"),
			"busqueda_exitosa": _("Búsqueda exitosa"),
			"busqueda_fallida": _("Búsqueda fallida"),
		}
		super().__init__(parent)

	def makeSettings(self, settingsSizer):
		# la casilla de verificación para activar y desactivar los sonidos
		self.soundsCheckBox = wx.CheckBox(self, label=_("&Activar sonidos"))
		self.soundsCheckBox.SetValue(config.conf['Note']['sounds'])
		self.soundsCheckBox.Bind(wx.EVT_CHECKBOX, self.onSoundsCheckBox)

		# la etiqueta para la lista de sonidos
		self.soundsLabel = wx.StaticText(self, label=_("Sonidos a reproducir:"))

		# la lista de sonidos con casillas de verificación
		self.soundListBox = CustomCheckListBox(self, choices=list(self.sounds.values()))
		for i, sound_key in enumerate(self.sounds.keys()):
			if config.conf['Note'][sound_key]:
				self.soundListBox.Check(i)

		# el botón para probar el sonido
		self.testSoundButton = wx.Button(self, label=_("&Probar sonido"))
		self.testSoundButton.Bind(wx.EVT_BUTTON, self.onTestSound)

		# Ocultar la etiqueta, la lista y el botón de prueba si la casilla de sonidos está desmarcada
		self.soundsLabel.Show(self.soundsCheckBox.IsChecked())
		self.soundListBox.Show(self.soundsCheckBox.IsChecked())
		self.testSoundButton.Show(self.soundsCheckBox.IsChecked())

		settingsSizer.Add(self.soundsCheckBox, border=10, flag=wx.ALL)
		settingsSizer.Add(self.soundsLabel, border=10, flag=wx.ALL)
		settingsSizer.Add(self.soundListBox, border=10, flag=wx.ALL | wx.EXPAND)
		settingsSizer.Add(self.testSoundButton, border=10, flag=wx.ALL | wx.ALIGN_RIGHT)

	def onSoundsCheckBox(self, event):
		self.soundsLabel.Show(self.soundsCheckBox.IsChecked())
		self.soundListBox.Show(self.soundsCheckBox.IsChecked())
		self.testSoundButton.Show(self.soundsCheckBox.IsChecked())

	def onTestSound(self, event):
		selected_index = self.soundListBox.GetSelection()
		if selected_index != wx.NOT_FOUND:
			sound_key = list(self.sounds.keys())[selected_index]
			sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "sounds", f"{sound_key}.wav")
			if os.path.exists(sound_path):
				try:
					reproducir = wx.adv.Sound(sound_path)
					reproducir.Play(wx.adv.SOUND_ASYNC)
				except Exception as e:
					print(f"Error al reproducir el sonido: {e}")
			else:
				print(f"El archivo de sonido no existe: {sound_path}")

	def onSave(self):
		config.conf['Note']['sounds'] = self.soundsCheckBox.GetValue()
		for i, sound_key in enumerate(self.sounds.keys()):
			config.conf['Note'][sound_key] = self.soundListBox.IsChecked(i)
