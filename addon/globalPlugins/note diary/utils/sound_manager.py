# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import os
import config
import addonHandler
addonHandler.initTranslation()

def reproducirSonido(sonido):
	# Comprobar si los sonidos están activados y si el sonido específico está activado
	if config.conf["Note"]["sounds"] and config.conf["Note"][sonido]:
		sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources", "sounds", f"{sonido}.wav")
		if os.path.exists(sound_path):
			try:
				reproducir = wx.adv.Sound(sound_path)
				reproducir.Play(wx.adv.SOUND_ASYNC)
			except Exception as e:
				print(f"Error al reproducir el sonido: {e}")
		else:
			print(f"El archivo de sonido no existe: {sound_path}")
