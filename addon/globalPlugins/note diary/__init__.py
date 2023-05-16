# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
import wx.adv
import shutil
import gui
import globalPluginHandler
import globalVars
import ui
import api
import time
import zipfile
import sys, os,config
sys.path.append(os.path.dirname(__file__))
from scriptHandler import script
from .settings import noteDiarySettingsPanel
from acccesibilidad import Accesibilidad
import addonHandler
addonHandler.initTranslation()

if not os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios")):
	os.mkdir(os.path.join(globalVars.appArgs.configPath, "diarios"))

# variables globales
capitulos = []

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

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self):
		# Call of the constructor of the parent class.
		super(GlobalPlugin, self).__init__()
		confspec = {"sounds": "boolean(default=True)"}
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
			self._MainWindows = Dialogo(gui.mainFrame)
		if not self._MainWindows.IsShown():
			gui.mainFrame.prePopup()
			self._MainWindows.Show()
			# si ya hay una instancia de la ventana principal, mostrar un mensaje
		else:
			ui.message(_("Ya hay una instancia de Note	diary abierta"))
	# Translators: Description for the input gesture panel
	@script(gesture=None, description= _("Abrir la lista de diarios"),
		# Translators: Category name in panel entry gestures
		category= _("Note diary"))
	def script_NoteDiary(self, gesture):
		wx.CallAfter(self.dlgPrincipal, None)

class Dialogo(wx.Dialog):
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

	def reproducirSonido(self, sonido):
		# variables
		vul = True
		sonidos = {
			"crear": "crear.wav",
			"borrar": "borrar.wav",
			"editar-cap": "editar-cap.wav",
			"guardar-cap": "guardar-cap.wav",
			"pasar-cap": "pasar-cap.wav",
			"pasar-diario": "pasar-diario.wav",
			"busqueda-exitosa": "busqueda_exitosa.wav",
			"busqueda-fallida": "busqueda_fallida.wav",
		}
		if config.conf["Note"]["sounds"]:
			if vul:
				# si vul es verdadero, se reproduce el sonido
				# si no, no se reproduce nada
				reproducir = wx.adv.Sound(os.path.join(os.path.dirname(__file__), "sounds", sonidos[sonido]))
				reproducir.Play(wx.adv.SOUND_ASYNC)

	def __init__(self, parent):
		WIDTH = 500
		HEIGHT = 350
		pos = self._calculatePosition(WIDTH, HEIGHT)

		super(Dialogo, self).__init__(parent, -1, title=_("Note diary"), pos = pos, size = (WIDTH, HEIGHT))

		# Create the main panel
		self.mainPanel = wx.Panel(self)

		# Translators: Label for the button menu
		self.btn_menu = wx.Button(self.mainPanel, wx.ID_ANY, label=_("&Más opciones"), pos=(10, 10))
		# los eventos del menú
		self.btn_menu.Bind(wx.EVT_BUTTON, self.onMenu)
		self.btn_menu.Bind(wx.EVT_CHAR_HOOK, self.onCharHook)
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
		self.text_ctrl.Bind(wx.EVT_TEXT, self.onText)
		label_filtro = wx.StaticText(self.panel_buscar, label=_("Filtrar por:"))
		self.filter_choice = wx.Choice(self.panel_buscar, choices=["Diarios", "Capítulos"])
		self.filter_choice.SetSelection(0)

		# Translator: Label for the tree
		self.label = wx.StaticText(self.mainPanel, label=_("&Diarios"))
		self.tree = wx.TreeCtrl(self.mainPanel, -1, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)
		self.root = self.tree.AddRoot("diarios")

		self.diarios = os.listdir(os.path.join(globalVars.appArgs.configPath, "diarios"))
		for diario in self.diarios:
			self.tree.AppendItem(self.root, diario)
			for capitulo in enlistarCapitulos(diario):
				self.tree.AppendItem(self.tree.GetLastChild(self.root), capitulo)

		self.tree.SetFocus()
		self.tree.Bind(wx.EVT_KEY_DOWN, self.onKeyDown)
		self.tree.Bind(wx.EVT_CONTEXT_MENU, self.onMenuContextual)
		self.tree.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onVerCapitulo)
		self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.onFoco)

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
		menu.Bind(wx.EVT_MENU_OPEN, self.onMenuOpen)
		# cuando el menú se cierra
		menu.Bind(wx.EVT_MENU_CLOSE, self.onMenuClose)
		# Translators: Label for the menu item to create a diary
		nuevo_diario = menu.Append(wx.ID_ANY, _("Nuevo diario"))
		self.Bind(wx.EVT_MENU, self.onNuevoDiario, nuevo_diario)
		# Translators: Label for the menu item to create a new chapter
		nuevo_capitulo = menu.Append(wx.ID_ANY, _("Nuevo capítulo"))
		self.Bind(wx.EVT_MENU, self.onNuevoCapitulo, nuevo_capitulo)
		# Translators: Label for the menu item to import a ndn file
		importar = menu.Append(wx.ID_ANY, _("Importar diarios"))
		self.Bind(wx.EVT_MENU, self.onImportar, importar)
		# Translators: Label for the menu item to export all diaries to a file with the extension ndn
		exportar = menu.Append(wx.ID_ANY, _("Exportar diarios"))
		self.Bind(wx.EVT_MENU, self.onExportar, exportar)
		# el submenú de ayuda
		ayuda = wx.Menu()
		# Translators: Label for the menu item to show the about dialog
		acerca_de = ayuda.Append(wx.ID_ABOUT, _("Acerca de..."))
		self.Bind(wx.EVT_MENU, self.onAcercaDe, acerca_de)
		# Translators: Label for the menu item to show the documentation
		documentacion = ayuda.Append(wx.ID_HELP, _("Documentación"))
		self.Bind(wx.EVT_MENU, self.onDocumentacion, documentacion)
		# Translators: Label for the menu item to show the help
		menu.AppendSubMenu(ayuda, _("Ayuda"))

		self.PopupMenu(menu, self.btn_menu.GetPosition())
		menu.Destroy()

	def onMenuOpen(self, event):
		# cambiar el estado del menú de contraído a expandido
		self.menu_accesible.SetEstado(wx.ACC_STATE_SYSTEM_EXPANDED)

	def onMenuClose(self, event):
		# cambiar el estado del menú de expandido a contraído
		self.menu_accesible.SetEstado(wx.ACC_STATE_SYSTEM_COLLAPSED)

	def onCharHook(self, event):
		if event.GetKeyCode() == wx.WXK_DOWN:
			self.onMenu(event)
		else:
			event.Skip()

	def onText(self, event):
		# Manejador del evento de texto
		text = self.text_ctrl.GetValue().upper()
		filter_type = self.filter_choice.GetString(self.filter_choice.GetSelection())

		# Crear un diccionario para almacenar los diarios y capítulos que coinciden con la búsqueda
		coincidencias = {}

		# Filtrar los diarios y capítulos según el texto de búsqueda y el tipo de filtro
		for diario in self.diarios:
			if filter_type == "Capítulos":
				coincidencias_capitulos = [capitulo for capitulo in enlistarCapitulos(diario) if text in capitulo.upper()]
				if coincidencias_capitulos:
					coincidencias[diario] = coincidencias_capitulos

			elif text in diario.upper():
				coincidencias[diario] = enlistarCapitulos(diario)

		# Actualizar el árbol con los resultados de la búsqueda
		self.tree.Freeze()
		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot("diarios")
		for diario, capitulos in coincidencias.items():
			diario_node = self.tree.AppendItem(self.root, diario)
			for capitulo in capitulos:
				self.tree.AppendItem(diario_node, capitulo)
				self.text_ctrl.SetFocus()

		# Reproducir un sonido según el resultado de la búsqueda
		if coincidencias:
			self.reproducirSonido("busqueda-exitosa")
			# sacar la cantidad de diarios y capítulos que coinciden con la búsqueda
			num_resultados = len(coincidencias)
			if num_resultados == 1: wx.CallLater(100, lambda: ui.message(_("Se encontró {} resultado").format(num_resultados)))
			else: wx.CallLater(100, lambda: ui.message(_("Se encontraron {} resultados").format(num_resultados)))
		else:
			self.reproducirSonido("busqueda-fallida")
			wx.CallLater(100, lambda: ui.message(_("No se encontraron resultados")))

		# Expandir todos los diarios que contienen coincidencias en el filtro de los caps
		if filter_type == "Capítulos":
			self.tree.ExpandAll()

		self.tree.Thaw()

	def onMenuContextual(self, event):
		# crear un menú
		menu = wx.Menu()
		if self.tree.GetItemParent(self.tree.GetSelection()) != self.root:
			# Translators: Label for the menu item to edit a chapter
			editar = menu.Append(wx.ID_ANY, _("Editar...\tIntro"))
			self.Bind(wx.EVT_MENU, self.onVerCapitulo, editar)
		# Translators: Label for the menu item to delete a diary
		eliminar_ = menu.Append(wx.ID_ANY, _("Eliminar...\tSuprimir"))
		self.Bind(wx.EVT_MENU, self.onEliminar, eliminar_)
		# Translators: Label for the menu item to rename a diary
		renombrar = menu.Append(wx.ID_ANY, _("Renombrar...\tF2"))
		self.Bind(wx.EVT_MENU, self.onRenombrar, renombrar)
		# el menú para compartir
		# compartir = wx.Menu()
		# correo = compartir.Append(wx.ID_ANY, _("Compartir por correo"))
		# compartir.Append(wx.ID_ANY, _("Compartir por facebook"))
		# compartir.Append(wx.ID_ANY, _("Compartir por twitter"))
		# compartir.Append(wx.ID_ANY, _("Compartir por whatsapp"))
		# compartir.Append(wx.ID_ANY, _("Compartir por telegram"))
		# Translators: Label for the menu item to share
		# menu.AppendSubMenu(compartir, _("Compartir"))

		self.PopupMenu(menu, event.GetPosition())
		menu.Destroy()

	def onNuevoDiario(self, event):
		# Translators: title of the dialog to create a new diary
		with wx.TextEntryDialog(self, _("Introduce el nombre del diario"), _("Nuevo diario")) as dlg:
			if dlg.ShowModal() == wx.ID_OK:
				# crear una nueva carpeta con el nombre del diario
				check=crearCarpetaDiario(dlg.GetValue())
				if check==False:
					# translators: Message to show when the diary already exists
					wx.MessageBox(_("al parecer este diario ya  existe.\nrevise que el nombre no coinsida con otro diario."), "Error", wx.OK | wx.ICON_ERROR)
					return
				# cuando termine de crearse el diario enfocarlo
				self.tree.SelectItem(self.tree.AppendItem(self.root, dlg.GetValue()))
				self.reproducirSonido("crear")

	def onNuevoCapitulo(self, event):
		if self.tree.GetChildrenCount(self.root) == 0: wx.MessageBox(_("No hay ningún diario.\nPor favor cree uno nuevo."), _("Error"), wx.OK | wx.ICON_ERROR)
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			# translators: title of the dialog to create a new chapter
			with wx.TextEntryDialog(self, _("Introduce el nombre del capítulo"), _("Nuevo capítulo")) as dlg:
				if dlg.ShowModal() == wx.ID_OK:
					# crear un nuevo archivo con el nombre del capítulo
					check=crearCapitulo(self.tree.GetItemText(self.tree.GetSelection()), dlg.GetValue())
					if check==False:
						# translators: error message when a chapter already exists
						wx.MessageBox(_("al parecer este capítulo ya  existe.\nrevise que el nombre no coinsida con otro capítulo."), _("Error"), wx.OK | wx.ICON_ERROR)
						return
					# cuando termine de crearse el capítulo enfocarlo
					self.tree.SelectItem(self.tree.AppendItem(self.tree.GetSelection(), dlg.GetValue()))
		# translators: error message when a chapter is created without a diary
		else: wx.MessageBox(_("Debe seleccionar un diario para crear un nuevo capítulo"), _("Error"), wx.OK | wx.ICON_ERROR)

	def onExportar(self, event):
		# elegir una ruta para exportar todos los diarios con la extención ndn
		with wx.FileDialog(self, _("Exportar diarios"), wildcard="Archivo de diarios de Note Diary (*.ndn)|*.ndn", style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT) as fileDialog:
			# optener la carpeta de diarios que está ubicada en el globalVars
			carpetaDiarios = os.path.join(globalVars.appArgs.configPath, "diarios")
			# optener el nombre del fileDialog
			name = fileDialog.GetFilename()
			if fileDialog.ShowModal() == wx.ID_OK:
				with zipfile.ZipFile(fileDialog.GetPath(), "w") as zip:
					# añadir todos los diarios a la carpeta
					for diario in os.listdir(carpetaDiarios):
						# añadir el diario a la carpeta
						zip.write(os.path.join(carpetaDiarios, diario), diario)
						# añadir todos los capítulos a la carpeta
						for capitulo in os.listdir(os.path.join(carpetaDiarios, diario)):
							zip.write(os.path.join(carpetaDiarios, diario, capitulo), os.path.join(diario, capitulo))

	def onImportar(self, event):
		# elegir un archivo para importar todos los diarios con la extención ndn
		with wx.FileDialog(self, _("Importar diarios"), wildcard="Archivo de diarios de Note Diary (*.ndn)|*.ndn", style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as fileDialog:
			if fileDialog.ShowModal() == wx.ID_OK:
				# leer el archivo seleccionado y extraerlo en la carpeta de diarios
				with zipfile.ZipFile(fileDialog.GetPath(), "r") as zip:
					# verificar que el archivo no esté dañado
					try:
						zip.testzip()
					except:
						# translators: error message when the file is damaged
						wx.MessageBox(_("El archivo está dañado"), _("Error"), wx.OK | wx.ICON_ERROR)
						return
					# comprobar si el archivo está vacío
					if zip.namelist() == []:
						# translators: error message when the file is empty
						wx.MessageBox(_("El archivo está vacío"), _("Error"), wx.OK | wx.ICON_ERROR)
						return
					else:
						# comprobar si el archivo contiene diarios con el mismo nombre que los que ya existen
						for diario in zip.namelist():
							if os.path.exists(os.path.join(globalVars.appArgs.configPath, "diarios", diario)):
								dialog = wx.MessageDialog(None, _("¿el archivo con el nombre %s ya existe, te gustaría importarlo aún así?") %diario, _("Archivo existente"), style=wx.YES|wx.NO|wx.ICON_WARNING)
								if dialog.ShowModal() == wx.ID_YES:
									eliminarDiario(diario)
									zip.extract(diario,os.path.join(globalVars.appArgs.configPath, "diarios"))
									continue
								else: continue
							zip.extract(diario,os.path.join(globalVars.appArgs.configPath, "diarios"))
						# destruir la ventana y bolber a abrirla para reflejar los cambios
						# translators: message when the file is imported successfully
						wx.MessageBox(_("El archivo se importó correctamente"), _("Éxito"), wx.OK | wx.ICON_INFORMATION)
						self.onReiniciar()
						return
	def onReiniciar(self):
		# limpiar el arbol
		self.tree.DeleteAllItems()
		# actualizar el árbol
		self.diarios = os.listdir(os.path.join(globalVars.appArgs.configPath, "diarios"))
		for diario in self.diarios:
			self.tree.AppendItem(self.root, diario)
			for capitulo in enlistarCapitulos(diario):
				self.tree.AppendItem(self.tree.GetLastChild(self.root), capitulo)
		self.tree.SelectItem(self.tree.GetFirstChild(self.root)[0])

	def onVerCapitulo(self, event):
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			# si se pulsa enter en un diario, se expande o contrae
			if self.tree.IsExpanded(self.tree.GetSelection()): self.tree.Collapse(self.tree.GetSelection())
			else: self.tree.Expand(self.tree.GetSelection())
		else:   
			# obtener el nombre del diario y del cap
			self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
			# translators: title of the dialog to edit a chapter
			self.dlg_editor = wx.Dialog(self, title=_("Editando el capítulo: ") + self.capitulo, size=(500, 500))
			# translators: label of the text field to edit a chapter
			self.lbl_editor = wx.StaticText(self.dlg_editor, label=_("Conte&nido:"))
			self.editor = wx.TextCtrl(self.dlg_editor, style=wx.TE_MULTILINE)
			self.editor.SetValue(cargarCapitulo(self.diario, self.capitulo))
			self.editor.SetFocus()
			self.editor.Bind(wx.EVT_TEXT, self.onEditarTexto)
			self.esta_editado = False
			self.reproducirSonido("editar-cap")

			# translators: label of the button to show the copy options
			self.btn_opciones_copiado = wx.Button(self.dlg_editor, label=_("Opciones de copiado"))
			self.btn_opciones_copiado_accesible = Accesibilidad(self.btn_opciones_copiado)
			self.btn_opciones_copiado_accesible.SetRole(wx.ROLE_SYSTEM_PUSHBUTTON)
			self.btn_opciones_copiado_accesible.SetEstado(wx.ACC_STATE_SYSTEM_FOCUSED | wx.ACC_STATE_SYSTEM_FOCUSABLE | wx.ACC_STATE_SYSTEM_COLLAPSED)
			self.btn_opciones_copiado.SetAccessible(self.btn_opciones_copiado_accesible)
			self.btn_opciones_copiado.Bind(wx.EVT_BUTTON, self.onOpcionesCopiado)
			# desabilitar el botón de opciones de copiado sino hay texto en el campo de texto
			if self.editor.GetValue() == "": self.btn_opciones_copiado.Disable()
			else: self.btn_opciones_copiado.Enable()

			# la caja de agrupación
			self.caja_agrupacion = wx.Panel(self.dlg_editor)
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
			self.btn_guardar = wx.Button(self.dlg_editor, label=_("&Guardar"))
			self.btn_guardar.Bind(wx.EVT_BUTTON, self.onGuardarCapitulo)

			# Translators: label of the button to close the dialog to edit a chapter
			self.btn_cerrar = wx.Button(self.dlg_editor, id=wx.ID_CLOSE, label=_("&Cerrar"))
			self.btn_cerrar.Bind(wx.EVT_BUTTON, self.onCerrarEditor)
			self.dlg_editor.SetEscapeId(self.btn_cerrar.GetId())

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
			self.dlg_editor.SetSizer(self.sizer_editor)
			self.dlg_editor.ShowModal()

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
		# obtener el nombre del diario
		self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
		# guardar el contenido del campo multilinea en un archivo de texto
		guardarCapitulo(self.diario, self.capitulo, self.editor.GetValue())
		self.Refresh()
		self.Update()
		self.onFoco()
		self.reproducirSonido("guardar-cap")
		self.dlg_editor.Destroy()


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
				self.dlg_editor.Destroy()
			elif dlg_cerrar == wx.CANCEL:
				pass
		else:
			self.dlg_editor.Destroy()

	def onEliminar(self, event):
		# variables
		self.diario = self.tree.GetItemText(self.tree.GetSelection())
		self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
		self.contar_capitulos = self.tree.GetChildrenCount(self.tree.GetSelection())
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			# Translators: title of the dialog to delete a diary
			self.dlg_eliminar = wx.MessageDialog(self, _("¿Está seguro de que desea eliminar el diario " + self.diario + "? \nTome en cuenta que esta acción no es rebersible, y que también eliminará todos los capítulos del diario"), _("Eliminar diario"), wx.YES_NO | wx.ICON_ASTERISK)
			if self.dlg_eliminar.ShowModal() == wx.ID_YES:
				# eliminar el diario
				eliminarDiario(self.diario, )
				self.tree.Delete(self.tree.GetSelection())
				# reproducir el sonido
				self.reproducirSonido("borrar")
				if self.tree.GetChildrenCount(self.root) == 0:
					# poner el foco en el botón de menú
					self.btn_menu.SetFocus()
			self.dlg_eliminar.Destroy()
		else:
			self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
			# Translators: title of the dialog to delete a chapter
			self.dlg_eliminar = wx.MessageDialog(self, _("¿Está seguro de que desea eliminar el capítulo " + self.capitulo + "?"), _("Eliminar capítulo"), wx.YES_NO | wx.ICON_ASTERISK)
			if self.dlg_eliminar.ShowModal() == wx.ID_YES:
				eliminarCapitulo(self.diario, self.capitulo)
				self.tree.Delete(self.tree.GetSelection())

			self.dlg_eliminar.Destroy()

	def onRenombrar(self, event):
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			self.diario = self.tree.GetItemText(self.tree.GetSelection())
			# crear un cuadro de diálogo para ingresar el nuevo nombre del diario
			self.dlg_renombrar = wx.TextEntryDialog(self, "Ingrese el nuevo nombre del diario", "Renombrar diario", self.diario)
			self.btn_ok = self.dlg_renombrar.FindWindowById(wx.ID_OK)
			self.btn_ok.SetLabel(_("&Renombrar"))
			if self.dlg_renombrar.ShowModal() == wx.ID_OK:
				# renombrar el diario
				renombrarDiario(self.diario, self.dlg_renombrar.GetValue())
				self.tree.SetItemText(self.tree.GetSelection(), self.dlg_renombrar.GetValue())
			self.dlg_renombrar.Destroy()
		else:
			self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
			# crear un cuadro de diálogo para ingresar el nuevo nombre del capítulo
			self.dlg_renombrar = wx.TextEntryDialog(self, "Ingrese el nuevo nombre del capítulo", "Renombrar capítulo", self.capitulo)
			self.btn_ok = self.dlg_renombrar.FindWindowById(wx.ID_OK)
			self.btn_ok.SetLabel(_("&Renombrar"))
			if self.dlg_renombrar.ShowModal() == wx.ID_OK:
				# renombrar el capítulo
				renombrarCapitulo(self.diario, self.capitulo, self.dlg_renombrar.GetValue())
				# renombrar el capítulo en el árbol
				self.tree.SetItemText(self.tree.GetSelection(), self.dlg_renombrar.GetValue())
			self.dlg_renombrar.Destroy()

	def onKeyDown(self, event):
		# creamos todos los atajos de teclado
		if event.GetKeyCode() == 78 and event.ControlDown(): self.onNuevoDiario(event)
		elif event.GetKeyCode() == 80 and event.ControlDown(): self.onNuevoCapitulo(event)
		elif wx.GetKeyState(wx.WXK_F2): self.onRenombrar(event)
		# tecla f1 para abrir la documentación
		elif wx.GetKeyState(wx.WXK_F1): self.onDocumentacion(event)
		# tecla f5 para actualizar el árbol
		elif wx.GetKeyState(wx.WXK_F5): self.onActualizar(event)
		# detectar la tecla suprimir para eliminar
		elif event.GetKeyCode() == wx.WXK_DELETE: self.onEliminar(event)
		else: event.Skip()

	# crear función para actualizar la ventana principal
	def onActualizar(self, event):
		# actualizar la ventana padre
		self.Refresh()
		self.Update()
		self.tree.SelectItem(self.tree.GetFirstChild(self.root)[0])
		self.tree.SetFocus()
		ui.message(_("Se	ha actualizado la ventana"))
		time.sleep(1)

	def onFoco(self, event=None):
		if not self.tree or self.tree.IsBeingDeleted() or not self.tree.GetSelection():
			return

		selected_item = self.tree.GetSelection()
		parent_item = self.tree.GetItemParent(selected_item)

		if parent_item == self.root:
			self.reproducirSonido("pasar-diario")

			# obtener los datos del diario
			name_diario = self.tree.GetItemText(selected_item)
			dir_diario = os.path.join(os.path.dirname(globalVars.appArgs.configPath), "nvda/diarios", name_diario)
			fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(dir_diario)))
			fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(dir_diario)))
			num_capitulos = len(os.listdir(dir_diario))

			# mostrar los datos en el campo de texto de info
			info = _("Nombre del diario: {0}\nFecha de creación: {1}\nFecha de modificación: {2}\nNúmero de capítulos: {3}").format(name_diario, fecha, fecha_mod, num_capitulos)
			self.info.SetValue(info)

		else:
			self.reproducirSonido("pasar-cap")

			# obtener los datos del capítulo
			name_cap = self.tree.GetItemText(selected_item)
			name_diario = self.tree.GetItemText(parent_item)
			dir_diario = os.path.join(os.path.dirname(globalVars.appArgs.configPath), "nvda/diarios", name_diario)
			dir_capitulo = os.path.join(dir_diario, name_cap)
			fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(dir_capitulo)))
			fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(dir_capitulo)))
			num_lineas = sum(1 for line in open(dir_capitulo, "r", encoding="utf-8"))
			num_paginas = (num_lineas // 50) + 1

			# mostrar los datos en el campo de texto de info
			info = _("Capítulo: {0}\nPertenece al diario: {1}\nFecha de creación: {2}\nFecha de modificación: {3}\nNúmero de páginas: {4}").format(name_cap, name_diario, fecha, fecha_mod, num_paginas)
			self.info.SetValue(info)	

	def onAcercaDe(self, event):
		# optener el contenido de el archivo manifest
		with open(os.path.join(os.path.dirname(__file__), "../", "../", "manifest.ini"), "r") as manifest:
			for linea in manifest:
				if linea.startswith("version"):
					self.version = linea.split("=")[1].strip()
				elif linea.startswith("author"):
					self.autor = linea.split("=")[1].strip()
				elif linea.startswith("url"):
					self.url = linea.split("=")[1].strip()
				elif linea.startswith("description"):
					self.descripcion = linea.split("=")[1].strip()
				elif linea.startswith("name"):
					self.nombre = os.path.basename(os.path.dirname(__file__))
		# mostrar el cuadro de diálogo
		self.dlg_acercaDe = wx.adv.AboutDialogInfo()
		self.dlg_acercaDe.SetName(self.nombre)
		self.dlg_acercaDe.SetVersion(_("Verción actual: ") + self.version)
		self.dlg_acercaDe.SetDescription(_("Descripción: ") + self.descripcion)
		self.dlg_acercaDe.SetWebSite(self.url)
		self.dlg_acercaDe.SetDevelopers([self.autor])
		wx.adv.AboutBox(self.dlg_acercaDe)

	def onDocumentacion(self, event):
		addon_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
		#nvda language.
		idioma=globalVars.appArgs.language.lower()
		if '_' in idioma:
			idioma=idioma.split('_')
			idioma=idioma[0]
		#intentar abrir  el archivo en el navegador predeterminado con la ruta del idioma.
		try: os.startfile(os.path.join(addon_dir, "doc", idioma, "readme.html"))
		except: os.startfile(os.path.join(addon_dir, "doc", 'en', "readme.html"))

	def onExit(self, event):
		self.Destroy()
		gui.mainFrame.postPopup()

