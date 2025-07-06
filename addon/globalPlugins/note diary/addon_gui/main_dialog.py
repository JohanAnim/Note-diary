# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import wx.adv
import os
import time
import globalVars
import ui
import config
import languageHandler

from .accessibility import Accesibilidad
from ..logic import file_manager
from .chapter_editor import ChapterEditorDialog
from ..logic import search_logic
from ..logic import dialog_logic
from ..utils.sound_manager import reproducirSonido
from ..utils import app_info
import addonHandler
addonHandler.initTranslation()

class MainDialog(wx.Dialog):
# Function taken from the add-on emoticons to center the window
	def _calculatePosition(self, width, height):
		w = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_X)
		h = wx.SystemSettings.GetMetric(wx.SYS_SCREEN_Y)
		# Centre of the screen
		x = w / 2
		y = h / 2
		# Minus application offset
		x -= (width / 2)
		y -= (height / 2)
		return (x, y)

	def __init__(self, parent):
		WIDTH = 500
		HEIGHT = 350
		pos = self._calculatePosition(WIDTH, HEIGHT)

		super(MainDialog, self).__init__(parent, -1, title=_("Note diary"), pos = pos, size = (WIDTH, HEIGHT))

		# Create the main panel
		self.mainPanel = wx.Panel(self)

		# Translators: Label for the button menu
		self.btn_menu = wx.Button(self.mainPanel, wx.ID_ANY, label=_("&Más opciones"), pos=(10, 10))
		# los eventos del menú
		self.btn_menu.Bind(wx.EVT_BUTTON, self.onMenu)
		self.btn_menu.Bind(wx.EVT_CHAR_HOOK, lambda event: dialog_logic.onCharHook(self, event))
		self.menu_accesible = Accesibilidad(self.btn_menu)
		self.menu_accesible.SetRole(wx.ROLE_SYSTEM_BUTTONMENU)
		self.menu_accesible.SetEstado(wx.ACC_STATE_SYSTEM_COLLAPSED)
		self.menu_accesible.SetNombre(_("Más opciones"))
		self.menu_accesible.SetDescripcion(_("Abre el menú de opciones"))
		# aplicar la accesibilidad
		self.btn_menu.SetAccessible(self.menu_accesible)

		# un panel para la búsqueda
		self.panel_buscar = wx.Panel(self.mainPanel, pos=(10, 50), size=(480, 30))
		# ponerle accesibilidad para que sea una caja de agrupación
		self.agrupacion_buscar = Accesibilidad(self.panel_buscar)
		self.agrupacion_buscar.SetRole(wx.ROLE_SYSTEM_GROUPING)
		self.agrupacion_buscar.SetNombre(_("Búsqueda"))
		self.panel_buscar.SetAccessible(self.agrupacion_buscar)

		# Crear el campo de texto y el Choice
		label_buscar = wx.StaticText(self.panel_buscar, label=_("Buscar:"))
		self.text_ctrl = wx.TextCtrl(self.panel_buscar)
		self.text_ctrl.Bind(wx.EVT_TEXT, lambda event: dialog_logic.onText(self, event))
		label_filtro = wx.StaticText(self.panel_buscar, label=_("Filtrar por:"))
		self.filter_choice = wx.Choice(self.panel_buscar, choices=[_("Diarios"), _("Capítulos")])
		self.filter_choice.SetSelection(0)

		# Translator: Label for the tree
		self.label = wx.StaticText(self.mainPanel, label=_("&Diarios"))
		self.tree = wx.TreeCtrl(self.mainPanel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
		self.root = self.tree.AddRoot("diarios")

		self.diarios = os.listdir(os.path.join(globalVars.appArgs.configPath, "diarios"))
		for diario in self.diarios:
			self.tree.AppendItem(self.root, diario)
			for capitulo in file_manager.enlistarCapitulos(diario):
				self.tree.AppendItem(self.tree.GetLastChild(self.root), capitulo)

		self.tree.SetFocus()
		self.tree.Bind(wx.EVT_KEY_DOWN, lambda event: dialog_logic.onKeyDown(self, event))
		self.tree.Bind(wx.EVT_CONTEXT_MENU, lambda event: dialog_logic.onMenuContextual(self, event))
		self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onVerCapitulo)
		self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, lambda event: dialog_logic.onFoco(self, event))

		self.label_info = wx.StaticText(self.mainPanel, label=_("&Información"))
		self.info = wx.TextCtrl(self.mainPanel, wx.ID_ANY, style=wx.TE_MULTILINE | wx.TE_READONLY)
		self.info.SetValue(_("Seleccione un diario o un capítulo para ver su información"))
		self.info.SetInsertionPoint(0)
		# estableser el ancho y el alto del control
		self.info.SetSize((WIDTH - 20, 100))

		# Translators: Label for the button to close the window
		self.btnCerrar = wx.Button(self.mainPanel, id=wx.ID_CLOSE, label=_("&Cerrar"))
		self.btnCerrar.Bind(wx.EVT_BUTTON, self.onExit)
		self.SetEscapeId(self.btnCerrar.GetId())

	def onMenu(self, event):
		# create a menu
		menu = wx.Menu()
		# evento para cuadno el menú se abre
		menu.Bind(wx.EVT_MENU_OPEN, lambda event: dialog_logic.onMenuOpen(self, event))
		# cuando el menú se cierra
		menu.Bind(wx.EVT_MENU_CLOSE, lambda event: dialog_logic.onMenuClose(self, event))
		# Translators: Label for the menu item to create a diary
		nuevo_diario = menu.Append(wx.ID_ANY, _("Nuevo diario"))
		self.Bind(wx.EVT_MENU, lambda event: dialog_logic.onNuevoDiario(self, event), nuevo_diario)
		# Translators: Label for the menu item to create a new chapter
		nuevo_capitulo = menu.Append(wx.ID_ANY, _("Nuevo capítulo"))
		self.Bind(wx.EVT_MENU, lambda event: dialog_logic.onNuevoCapitulo(self, event), nuevo_capitulo)
		# Translators: Label for the menu item to import a ndn file
		importar = menu.Append(wx.ID_ANY, _("Importar diarios"))
		self.Bind(wx.EVT_MENU, lambda event: file_manager.importarDiarios(self), importar)
		# Translators: Label for the menu item to export all diaries to a file with the extension ndn
		exportar = menu.Append(wx.ID_ANY, _("Exportar diarios"))
		self.Bind(wx.EVT_MENU, lambda event: file_manager.exportarDiarios(), exportar)
		# el submenú de ayuda
		ayuda = wx.Menu()
		# Translators: Label for the menu item to show the about dialog
		acerca_de = ayuda.Append(wx.ID_ABOUT, _("Acerca de..."))
		self.Bind(wx.EVT_MENU, lambda event: app_info.showAboutDialog(), acerca_de)
		# Translators: Label for the menu item to show the documentation
		documentacion = ayuda.Append(wx.ID_HELP, _("Documentación"))
		self.Bind(wx.EVT_MENU, lambda event: app_info.openDocumentation(), documentacion)
		# Translators: Label for the menu item to show the help
		menu.AppendSubMenu(ayuda, _("Ayuda"))

		self.PopupMenu(menu, self.btn_menu.GetPosition())
		menu.Destroy()


	def onVerCapitulo(self, event):
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			# si se pulsa enter en un diario, se expande o contrae
			if self.tree.IsExpanded(self.tree.GetSelection()): self.tree.Collapse(self.tree.GetSelection())
			else: self.tree.Expand(self.tree.GetSelection())
		else:   
			# obtener el nombre del diario y del cap
			self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
			reproducirSonido("editar-cap")
			with ChapterEditorDialog(self, self.diario, self.capitulo) as dlg:
				dlg.ShowModal()

	def onExit(self, event):
		self.Destroy()
		#gui.mainFrame.postPopup()
