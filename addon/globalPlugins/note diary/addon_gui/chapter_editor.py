# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import os
import ui
import addonHandler
addonHandler.initTranslation()

from .accessibility import Accesibilidad
from ..logic import file_manager

class ChapterEditorDialog(wx.Dialog):
	def __init__(self, parent, diario, capitulo):
		super(ChapterEditorDialog, self).__init__(parent, title=_("Editando el capítulo: ") + capitulo, size=(500, 500))
		self.diario = diario
		self.capitulo = capitulo

		# translators: label of the text field to edit a chapter
		self.lbl_editor = wx.StaticText(self, label=_("Conte&nido:"))
		self.editor = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		self.editor.SetValue(file_manager.cargarCapitulo(self.diario, self.capitulo))
		self.editor.SetFocus()
		self.editor.Bind(wx.EVT_TEXT, self.onEditarTexto)
		self.esta_editado = False
		# self.reproducirSonido("editar-cap") # Esto debería ser manejado por el MainDialog

		# translators: label of the button to show the copy options
		self.btn_opciones_copiado = wx.Button(self, label=_("Opciones de copiado"))
		self.btn_opciones_copiado_accesible = Accesibilidad(self.btn_opciones_copiado)
		self.btn_opciones_copiado_accesible.SetRole(wx.ROLE_SYSTEM_PUSHBUTTON)
		self.btn_opciones_copiado_accesible.SetEstado(wx.ACC_STATE_SYSTEM_FOCUSED | wx.ACC_STATE_SYSTEM_FOCUSABLE | wx.ACC_STATE_SYSTEM_COLLAPSED)
		self.btn_opciones_copiado.SetAccessible(self.btn_opciones_copiado_accesible)
		self.btn_opciones_copiado.Bind(wx.EVT_BUTTON, self.onOpcionesCopiado)
		# desabilitar el botón de opciones de copiado sino hay texto en el campo de texto
		if self.editor.GetValue() == "": self.btn_opciones_copiado.Disable()
		else: self.btn_opciones_copiado.Enable()

		# la caja de agrupación
		self.caja_agrupacion = wx.Panel(self)
		self.caja_agrupacion_accesible = Accesibilidad(self.caja_agrupacion)
		self.caja_agrupacion_accesible.SetRole(wx.ROLE_SYSTEM_GROUPING)
		self.caja_agrupacion_accesible.SetNombre(self.btn_opciones_copiado.GetLabel())
		self.caja_agrupacion.SetAccessible(self.caja_agrupacion_accesible)
		self.caja_agrupacion.Hide()

		# Translators: label of the button to copy the current line to the clipboard
		self.btn_copiar = wx.Button(self.caja_agrupacion, label=_("Copiar la línea actual &al portapapeles"))
		self.btn_copiar.Bind(wx.EVT_BUTTON, self.onCopiarLinea)
		# Translators: label of the button to copy the chapter to the clipboard
		self.btn_copiar = wx.Button(self.caja_agrupacion, label=_("Co&piar todo el documento"))
		self.btn_copiar.Bind(wx.EVT_BUTTON, self.onCopiarCap)

		# Translators: label of the button to save the chapter
		self.btn_guardar = wx.Button(self, label=_("&Guardar"))
		self.btn_guardar.Bind(wx.EVT_BUTTON, self.onGuardarCapitulo)

		# Translators: label of the button to close the dialog to edit a chapter
		self.btn_cerrar = wx.Button(self, id=wx.ID_CLOSE, label=_("&Cerrar"))
		self.btn_cerrar.Bind(wx.EVT_BUTTON, self.onCerrarEditor)
		self.SetEscapeId(self.btn_cerrar.GetId())

		# los sizers
		self.sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
		self.sizer_btn.Add(self.btn_opciones_copiado, 0, wx.ALL, 5)
		self.sizer_btn.Add(self.caja_agrupacion, 0, wx.ALL, 5)
		self.sizer_btn.Add(self.btn_guardar, 0, wx.ALL, 5)
		self.sizer_btn.Add(self.btn_cerrar, 0, wx.ALL, 5)
		self.sizer_editor = wx.BoxSizer(wx.VERTICAL)
		self.sizer_editor.Add(self.lbl_editor, 0, wx.ALL, 5)
		self.sizer_editor.Add(self.editor, 1, wx.ALL | wx.EXPAND, 5)
		self.sizer_editor.Add(self.sizer_btn, 0, wx.ALIGN_RIGHT)
		# establecer el sizer
		self.SetSizer(self.sizer_editor)

	def onOpcionesCopiado(self, event):
		# mostrar o ocultar la caja de agrupación dependiendo si está expandido o no
		if self.caja_agrupacion.IsShown():
			self.caja_agrupacion.Hide()
			# cambiar el estado del botón
			self.btn_opciones_copiado_accesible.SetEstado(wx.ACC_STATE_SYSTEM_COLLAPSED)
		else:
			self.caja_agrupacion.Show()
			# cambiar el estado del botón
			self.btn_opciones_copiado_accesible.SetEstado(wx.ACC_STATE_SYSTEM_EXPANDED)


	def onCopiarLinea(self, event):
		# optener la línea en que el usuario a posicionado el cursor
		pos_cursor = self.editor.GetInsertionPoint()
		num_lineas = self.editor.GetNumberOfLines()
		for num_linea in range(num_lineas):
			inicio_linea = self.editor.XYToPosition(0, num_linea)
			fin_linea = self.editor.XYToPosition(self.editor.GetLineLength(num_linea), num_linea)
			if inicio_linea <= pos_cursor <= fin_linea:
				linea = self.editor.GetRange(inicio_linea, fin_linea)
				# copiar la línea al portapapeles
				wx.TheClipboard.Open()
				wx.TheClipboard.SetData(wx.TextDataObject(linea))
				wx.TheClipboard.Close()
				ui.reportTextCopiedToClipboard(linea)
				return

	def onCopiarCap(self, event):
		# copiar el contenido del capítulo al portapapeles
		wx.TheClipboard.Open()
		wx.TheClipboard.SetData(wx.TextDataObject(self.editor.GetValue()))
		wx.TheClipboard.Close()
		ui.reportTextCopiedToClipboard(self.editor.GetValue())

	def onGuardarCapitulo(self, event):
		# guardar el contenido del campo multilinea en un archivo de texto
		file_manager.guardarCapitulo(self.diario, self.capitulo, self.editor.GetValue())
		self.Parent.onFoco() # Actualizar la información en el MainDialog
		self.EndModal(wx.ID_OK)


	def onEditarTexto(self, event):
		self.esta_editado = True
		# desabilitar el botón de opciones de copiado sino hay texto en el campo de texto
		if self.editor.GetValue() == "": self.btn_opciones_copiado.Disable()
		else: self.btn_opciones_copiado.Enable()

	def onCerrarEditor(self, event):
		if self.esta_editado:
			# Translators: title of the dialog to close the dialog to edit a chapter
			dlg_cerrar = wx.MessageBox(_("El capítulo a sido editado, ¿desea guardar los cambios?"), _("Guardar"), wx.YES_NO | wx.CANCEL | wx.ICON_ASTERISK)
			if dlg_cerrar == wx.YES:
				self.onGuardarCapitulo(event)
			elif dlg_cerrar == wx.NO:
				self.EndModal(wx.ID_CANCEL)
			elif dlg_cerrar == wx.CANCEL:
				pass
		else:
			self.EndModal(wx.ID_CANCEL)
