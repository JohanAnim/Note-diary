# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import os
import wx.adv
import languageHandler
import addonHandler
addonHandler.initTranslation()

def showAboutDialog():
	# optener el contenido de el archivo manifest
	addon_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
	manifest_path = os.path.join(addon_dir, "manifest.ini")
	version = ""
	autor = ""
	url = ""
	descripcion = ""
	nombre = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

	with open(manifest_path, "r") as manifest:
		for linea in manifest:
			if linea.startswith("version"):
				version = linea.split("=")[1].strip()
			elif linea.startswith("author"):
				autor = linea.split("=")[1].strip()
			elif linea.startswith("url"):
				url = linea.split("=")[1].strip()
			elif linea.startswith("description"):
				descripcion = linea.split("=")[1].strip()
	# mostrar el cuadro de diálogo
	dlg_acercaDe = wx.adv.AboutDialogInfo()
	dlg_acercaDe.SetName(nombre)
	dlg_acercaDe.SetVersion(_("Verción actual: ") + version)
	dlg_acercaDe.SetDescription(_("Descripción: ") + descripcion)
	dlg_acercaDe.SetWebSite(url)
	dlg_acercaDe.SetDevelopers([autor])
	wx.adv.AboutBox(dlg_acercaDe)

def openDocumentation():
	addon_dir = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."))
	lang = languageHandler.getLanguage()
	if "_" in lang:
		lang = lang.split("_")[0]
	doc_path = os.path.join(addon_dir, "doc", lang, "readme.html")
	if not os.path.exists(doc_path):
		doc_path = os.path.join(addon_dir, "doc", "en", "readme.html")
	try:
		os.startfile(doc_path)
	except OSError:
		wx.MessageBox(_("No se pudo abrir la documentación."), _("Error"), wx.OK | wx.ICON_ERROR)
