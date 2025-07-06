# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import os
import shutil
import zipfile
import wx

import globalVars
import addonHandler
addonHandler.initTranslation()

def enlistarCapitulos(diario):
	return os.listdir(os.path.join(globalVars.appArgs.configPath, "diarios", diario))

def crearCarpetaDiario(diario):
	if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios", diario)):
		os.mkdir(os.path.join(globalVars.appArgs.configPath, "diarios", diario))
	else: return False
def crearCapitulo(diario, capitulo):
	if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo)):
		with open(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), "w") as f:
			f.write("")
	else: return False

def guardarCapitulo(diario, capitulo, contenido):
	# Agregar la línea de codificación
	with open(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), "w", encoding='utf-8') as f:
		f.write(contenido)

def cargarCapitulo(diario, capitulo):
	with open(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), "r", encoding='utf-8') as f:
		return f.read()

def eliminarDiario(diario):
	shutil.rmtree(os.path.join(globalVars.appArgs.configPath, "diarios", diario))

def eliminarCapitulo(diario, capitulo):
	os.remove(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo))

def renombrarDiario(diario, nuevoNombre):
	os.rename(os.path.join(globalVars.appArgs.configPath, "diarios", diario), os.path.join(globalVars.appArgs.configPath, "diarios", nuevoNombre))
def renombrarCapitulo(diario, capitulo, nuevoNombre):
	os.rename(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), os.path.join(globalVars.appArgs.configPath, "diarios", diario, nuevoNombre))

def exportarDiarios():
	with wx.FileDialog(None, _("Exportar diarios"), wildcard="Archivo de diarios de Note Diary (*.ndn)|*.ndn", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
		carpetaDiarios = os.path.join(globalVars.appArgs.configPath, "diarios")
		if fileDialog.ShowModal() == wx.ID_OK:
			with zipfile.ZipFile(fileDialog.GetPath(), "w") as zip:
				for diario in os.listdir(carpetaDiarios):
					zip.write(os.path.join(carpetaDiarios, diario), diario)
					for capitulo in os.listdir(os.path.join(carpetaDiarios, diario)):
						zip.write(os.path.join(carpetaDiarios, diario, capitulo), os.path.join(diario, capitulo))

def importarDiarios(main_dialog_instance):
	with wx.FileDialog(None, _("Importar diarios"), wildcard="Archivo de diarios de Note Diary (*.ndn)|*.ndn", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
		if fileDialog.ShowModal() == wx.ID_OK:
			with zipfile.ZipFile(fileDialog.GetPath(), "r") as zip:
				try:
					zip.testzip()
				except:
					wx.MessageBox(_("El archivo está dañado"), _("Error"), wx.OK | wx.ICON_ERROR)
					return
			if zip.namelist() == []:
				wx.MessageBox(_("El archivo está vacío"), _("Error"), wx.OK | wx.ICON_ERROR)
				return
			else:
				for diario in zip.namelist():
					if os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios", diario)):
						dialog = wx.MessageDialog(None, _("¿el archivo con el nombre %s ya existe, te gustaría importarlo aún así?") %diario, _("Archivo existente"), style=wx.YES|wx.NO|wx.ICON_WARNING)
						if dialog.ShowModal() == wx.ID_YES:
							eliminarDiario(diario)
							zip.extract(diario,os.path.join(globalVars.appArgs.configPath, "diarios"))
							continue
						else: continue
					zip.extract(diario,os.path.join(globalVars.appArgs.configPath, "diarios"))
				wx.MessageBox(_("El archivo se importó correctamente"), _("Éxito"), wx.OK | wx.ICON_INFORMATION)
				main_dialog_instance.onReiniciar()
				return

def onReiniciar(main_dialog_instance):
	# limpiar el arbol
	main_dialog_instance.tree.DeleteAllItems()
	# actualizar el árbol
	main_dialog_instance.diarios = os.listdir(os.path.join(globalVars.appArgs.configPath, "diarios"))
	for diario in main_dialog_instance.diarios:
		main_dialog_instance.tree.AppendItem(main_dialog_instance.root, diario)
		for capitulo in enlistarCapitulos(diario):
			main_dialog_instance.tree.AppendItem(main_dialog_instance.tree.GetLastChild(main_dialog_instance.root), capitulo)
	main_dialog_instance.tree.SelectItem(main_dialog_instance.tree.GetFirstChild(main_dialog_instance.root)[0])