# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import os
import time
import globalVars
import ui
import addonHandler
addonHandler.initTranslation()

import markdown

from ..logic import file_manager
from ..logic import search_logic
from ..utils.sound_manager import reproducirSonido
from ..utils import app_info


def onMenuOpen(main_dialog_instance, event):
	# cambiar el estado del menú de contraído a expandido
	main_dialog_instance.menu_accesible.SetEstado(wx.ACC_STATE_SYSTEM_EXPANDED)

def onMenuClose(main_dialog_instance, event):
	# cambiar el estado del menú de expandido a contraído
	main_dialog_instance.menu_accesible.SetEstado(wx.ACC_STATE_SYSTEM_COLLAPSED)

def onCharHook(main_dialog_instance, event):
	if event.GetKeyCode() == wx.WXK_DOWN:
		main_dialog_instance.onMenu(event)
	else:
		event.Skip()

def onText(main_dialog_instance, event):
	text = main_dialog_instance.text_ctrl.GetValue().upper()
	filter_type = main_dialog_instance.filter_choice.GetString(main_dialog_instance.filter_choice.GetSelection())
	search_logic.search_diaries_and_chapters(main_dialog_instance, text, filter_type)

def onMenuContextual(main_dialog_instance, event):
	# crear un menú
	menu = wx.Menu()
	if main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()) != main_dialog_instance.root:
		# Translators: Label for the menu item to edit a chapter
		editar = menu.Append(wx.ID_ANY, _("Editar...\tIntro"))
		main_dialog_instance.Bind(wx.EVT_MENU, main_dialog_instance.onVerCapitulo, editar)
		# Translators: Label for the menu item to open a chapter in a web view
		vista_web = menu.Append(wx.ID_ANY, _("Abrir vista web en este capítulo"))
		main_dialog_instance.Bind(wx.EVT_MENU, lambda evt: onAbrirVistaWeb(main_dialog_instance, evt), vista_web)
	# Translators: Label for the menu item to delete a diary
	eliminar_ = menu.Append(wx.ID_ANY, _("Eliminar...\tSuprimir"))
	main_dialog_instance.Bind(wx.EVT_MENU, lambda evt: onEliminar(main_dialog_instance, evt), eliminar_)
	# Translators: Label for the menu item to rename a diary
	renombrar = menu.Append(wx.ID_ANY, _("Renombrar...\tF2"))
	main_dialog_instance.Bind(wx.EVT_MENU, lambda evt: onRenombrar(main_dialog_instance, evt), renombrar)
	# el menú para compartir
	# compartir = wx.Menu()
	# correo = compartir.Append(wx.ID_ANY, _("Compartir por correo"))
	# compartir.Append(wx.ID_ANY, _("Compartir por facebook"))
	# compartir.Append(wx.ID_ANY, _("Compartir por twitter"))
	# compartir.Append(wx.ID_ANY, _("Compartir por whatsapp"))
	# compartir.Append(wx.ID_ANY, _("Compartir por telegram"))
	# Translators: Label for the menu item to share
	# menu.AppendSubMenu(compartir, _("Compartir"))

	main_dialog_instance.PopupMenu(menu, event.GetPosition())
	menu.Destroy()

def onAbrirVistaWeb(main_dialog_instance, event):
	diario = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()))
	capitulo = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
	contenido = file_manager.cargarCapitulo(diario, capitulo)
	# convertir el contenido a html
	contenido_html = markdown.markdown(contenido, extensions=['tables'])
	ui.browseableMessage(contenido_html, _("Vista web del capítulo: ") + capitulo, True)

def onNuevoDiario(main_dialog_instance, event):
	# Translators: title of the dialog to create a new diary
	with wx.TextEntryDialog(main_dialog_instance, _("Introduce el nombre del diario"), _("Nuevo diario")) as dlg:
		if dlg.ShowModal() == wx.ID_OK:
			# crear una nueva carpeta con el nombre del diario
			check=file_manager.crearCarpetaDiario(dlg.GetValue())
			if check==False:
				# translators: Message to show when the diary already exists
				wx.MessageBox(_("al parecer este diario ya  existe.\nrevise que el nombre no coinsida con otro diario."), "Error", wx.OK | wx.ICON_ERROR)
				return
			# cuando termine de crearse el diario enfocarlo
			main_dialog_instance.tree.SelectItem(main_dialog_instance.tree.AppendItem(main_dialog_instance.root, dlg.GetValue()))
			reproducirSonido("crear")


def onNuevoCapitulo(main_dialog_instance, event):
	if main_dialog_instance.tree.GetChildrenCount(main_dialog_instance.root) == 0: wx.MessageBox(_("No hay ningún diario.\nPor favor cree uno nuevo."), _("Error"), wx.OK | wx.ICON_ERROR)
	if main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()) == main_dialog_instance.root:
		# translators: title of the dialog to create a new chapter
		with wx.TextEntryDialog(main_dialog_instance, _("Introduce el nombre del capítulo"), _("Nuevo capítulo")) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				# crear un nuevo archivo con el nombre del capítulo
				check=file_manager.crearCapitulo(main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection()), dlg.GetValue())
				if check==False:
					# translators: error message when a chapter already exists
					wx.MessageBox(_("al parecer este capítulo ya  existe.\nrevise que el nombre no coinsida con otro capítulo."), _("Error"), wx.OK | wx.ICON_ERROR)
					return
				# cuando termine de crearse el capítulo enfocarlo
				main_dialog_instance.tree.SelectItem(main_dialog_instance.tree.AppendItem(main_dialog_instance.tree.GetSelection(), dlg.GetValue()))
	# translators: error message when a chapter is created without a diary
	else: wx.MessageBox(_("Debe seleccionar un diario para crear un nuevo capítulo"), _("Error"), wx.OK | wx.ICON_ERROR)

def onEliminar(main_dialog_instance, event):
	# variables
	diario = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
	capitulo = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
	contar_capitulos = main_dialog_instance.tree.GetChildrenCount(main_dialog_instance.tree.GetSelection())
	if main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()) == main_dialog_instance.root:
		# Translators: title of the dialog to delete a diary
		dlg_eliminar = wx.MessageDialog(main_dialog_instance, _("¿Está seguro de que desea eliminar el diario ") + diario + _("? \nTome en cuenta que esta acción no es rebersible, y que también eliminará todos los capítulos del diario"), _("Eliminar diario"), wx.YES_NO | wx.ICON_ASTERISK)
		if dlg_eliminar.ShowModal() == wx.ID_YES:
			# eliminar el diario
			file_manager.eliminarDiario(diario, )
			main_dialog_instance.tree.Delete(main_dialog_instance.tree.GetSelection())
			# reproducir el sonido
			reproducirSonido("borrar")
			if main_dialog_instance.tree.GetChildrenCount(main_dialog_instance.root) == 0:
				# poner el foco en el botón de menú
				main_dialog_instance.btn_menu.SetFocus()
	else:
		diario = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()))
		capitulo = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
		# Translators: title of the dialog to delete a chapter
		dlg_eliminar = wx.MessageDialog(main_dialog_instance, _("¿Está seguro de que desea eliminar el capítulo ") + capitulo + "?", _("Eliminar capítulo"), wx.YES_NO | wx.ICON_ASTERISK)
		if dlg_eliminar.ShowModal() == wx.ID_YES:
			file_manager.eliminarCapitulo(diario, capitulo)
			main_dialog_instance.tree.Delete(main_dialog_instance.tree.GetSelection())
	dlg_eliminar.Destroy()

def onRenombrar(main_dialog_instance, event):
	if main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()) == main_dialog_instance.root:
		diario = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
		# Translators: title of the dialog to rename a diary
		dlg_renombrar = wx.TextEntryDialog(main_dialog_instance, _("Ingrese el nuevo nombre del diario"), _("Renombrar diario"), diario)
		btn_ok = dlg_renombrar.FindWindowById(wx.ID_OK)
		# Translators: label of the button to rename a diary
		btn_ok.SetLabel(_("&Renombrar"))
		if dlg_renombrar.ShowModal() == wx.ID_OK:
			# renombrar el diario
			file_manager.renombrarDiario(diario, dlg_renombrar.GetValue())
			main_dialog_instance.tree.SetItemText(main_dialog_instance.tree.GetSelection(), dlg_renombrar.GetValue())
		dlg_renombrar.Destroy()
	else:
		diario = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetItemParent(main_dialog_instance.tree.GetSelection()))
		capitulo = main_dialog_instance.tree.GetItemText(main_dialog_instance.tree.GetSelection())
		# Translators: title of the dialog to rename a chapter
		dlg_renombrar = wx.TextEntryDialog(main_dialog_instance, _("Ingrese el nuevo nombre del capítulo"), _("Renombrar capítulo"), capitulo)
		btn_ok = dlg_renombrar.FindWindowById(wx.ID_OK)
		# Translators: label of the button to rename a chapter
		btn_ok.SetLabel(_("&Renombrar"))
		if dlg_renombrar.ShowModal() == wx.ID_OK:
			# renombrar el capítulo
			file_manager.renombrarCapitulo(diario, capitulo, dlg_renombrar.GetValue())
			# renombrar el capítulo en el árbol
			main_dialog_instance.tree.SetItemText(main_dialog_instance.tree.GetSelection(), dlg_renombrar.GetValue())
		dlg_renombrar.Destroy()

def onKeyDown(main_dialog_instance, event):
	# creamos todos los atajos de teclado
	if event.GetKeyCode() == 78 and event.ControlDown(): onNuevoDiario(main_dialog_instance, event)
	elif event.GetKeyCode() == 80 and event.ControlDown(): onNuevoCapitulo(main_dialog_instance, event)
	elif wx.GetKeyState(wx.WXK_F2): onRenombrar(main_dialog_instance, event)
	# tecla f1 para abrir la documentación
	elif wx.GetKeyState(wx.WXK_F1): app_info.openDocumentation()
	# tecla f5 para actualizar el árbol
	elif wx.GetKeyState(wx.WXK_F5): onActualizar(main_dialog_instance, event)
	# detectar la tecla suprimir para eliminar
	elif event.GetKeyCode() == wx.WXK_DELETE: onEliminar(main_dialog_instance, event)
	else: event.Skip()

# crear función para actualizar la ventana principal
def onActualizar(main_dialog_instance, event):
	# actualizar la ventana padre
	main_dialog_instance.Refresh()
	main_dialog_instance.Update()
	main_dialog_instance.tree.SelectItem(main_dialog_instance.tree.GetFirstChild(main_dialog_instance.root)[0])
	main_dialog_instance.tree.SetFocus()
	ui.message(_("Se\tha actualizado la ventana"))
	time.sleep(1)

def onFoco(main_dialog_instance, event=None):
	if not main_dialog_instance.tree or main_dialog_instance.tree.IsBeingDeleted() or not main_dialog_instance.tree.GetSelection():
		return

	selected_item = main_dialog_instance.tree.GetSelection()
	parent_item = main_dialog_instance.tree.GetItemParent(selected_item)

	if parent_item == main_dialog_instance.root:
		reproducirSonido("pasar-diario")

		# obtener los datos del diario
		name_diario = main_dialog_instance.tree.GetItemText(selected_item)
		dir_diario = os.path.join(globalVars.appArgs.configPath, "diarios", name_diario)
		fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(dir_diario)))
		fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(dir_diario)))
		num_capitulos = len(os.listdir(dir_diario))

		# mostrar los datos en el campo de texto de info
		info = _("Nombre del diario: {0}\nFecha de creación: {1}\nFecha de modificación: {2}\nNúmero de capítulos: {3}").format(name_diario, fecha, fecha_mod, num_capitulos)
		main_dialog_instance.info.SetValue(info)

	else:
		reproducirSonido("pasar-cap")

		# obtener los datos del capítulo
		name_cap = main_dialog_instance.tree.GetItemText(selected_item)
		name_diario = main_dialog_instance.tree.GetItemText(parent_item)
		dir_diario = os.path.join(globalVars.appArgs.configPath, "diarios", name_diario)
		dir_capitulo = os.path.join(dir_diario, name_cap)
		fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(dir_capitulo)))
		fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(dir_capitulo)))
		num_lineas = sum(1 for line in open(dir_capitulo, "r", encoding="utf-8"))
		num_paginas = (num_lineas // 50) + 1

		# mostrar los datos en el campo de texto de info
		info = _("Capítulo: {0}\nPertenece al diario: {1}\nFecha de creación: {2}\nFecha de modificación: {3}\nNúmero de páginas: {4}").format(name_cap, name_diario, fecha, fecha_mod, num_paginas)
		main_dialog_instance.info.SetValue(info)
