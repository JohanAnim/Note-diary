# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx
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
from accessible import MenuAccessible
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
	with open(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), "w") as f:
		f.write(contenido)

def cargarCapitulo(diario, capitulo):
	with open(os.path.join(globalVars.appArgs.configPath, "diarios", diario, capitulo), "r") as f:
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
		# crear un item en el menú de herramientas y en el diálogo de configuración
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.menuItem = self.toolsMenu.Append(wx.ID_ANY, _("Note diary"), _("Abrir el diario"))
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
		self.btn_menu = wx.Button(self.mainPanel, wx.ID_ANY, label="&Menú", pos=(10, 10))
		self.Bind(wx.EVT_BUTTON, self.onMenu, self.btn_menu)
		self.btn_menu.SetToolTip(wx.ToolTip(_("Menú de opciones")))
		# añadir la accesibilidad al menú
		self.btn_menu.SetAccessible(MenuAccessible(self.btn_menu))

		# Translator: Label for the tree
		self.label = wx.StaticText(self.mainPanel, label="Diarios")
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

		self.label_info = wx.StaticText(self.mainPanel, label="Información")
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
		compartir = wx.Menu()
		correo = compartir.Append(wx.ID_ANY, _("Compartir por correo"))
		compartir.Append(wx.ID_ANY, _("Compartir por facebook"))
		compartir.Append(wx.ID_ANY, _("Compartir por twitter"))
		compartir.Append(wx.ID_ANY, _("Compartir por whatsapp"))
		compartir.Append(wx.ID_ANY, _("Compartir por telegram"))
		# Translators: Label for the menu item to share
		menu.AppendSubMenu(compartir, _("Compartir"))

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
				# añadir el diario al árbol
				self.tree.AppendItem(self.root, dlg.GetValue())
				# reproducir un sonido
				self.reproducirSonido("crear-diario")

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
					self.tree.AppendItem(self.tree.GetSelection(), dlg.GetValue())
					self.reproducirSonido("crear-diario")
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
			self.lbl_editor = wx.StaticText(self.dlg_editor, label=_("Contenido:"))
			self.editor = wx.TextCtrl(self.dlg_editor, style=wx.TE_MULTILINE)
			self.editor.SetValue(cargarCapitulo(self.diario, self.capitulo))
			# evento del cursor del editor para brindar información con la voz mientras se navega con las flechas
			self.editor.Bind(wx.EVT_KEY_DOWN, self.onCursor)
			self.reproducirSonido("editar-cap")

			# Translators: label of the button to copy the chapter to the clipboard
			self.btn_copiar = wx.Button(self.dlg_editor, label="Copiar")
			self.btn_copiar.Bind(wx.EVT_BUTTON, self.onCopiarCap)

			# Translators: label of the button to save the chapter
			self.btn_guardar = wx.Button(self.dlg_editor, label="&Guardar")
			self.btn_guardar.Bind(wx.EVT_BUTTON, self.onGuardarCapitulo)

			# Translators: label of the button to close the dialog to edit a chapter
			self.btn_cerrar = wx.Button(self.dlg_editor, id=wx.ID_CLOSE, label="&Cerrar")
			self.btn_cerrar.Bind(wx.EVT_BUTTON, self.onCerrarEditor)
			self.dlg_editor.SetEscapeId(self.btn_cerrar.GetId())

			# los sizers
			self.sizer_btn = wx.BoxSizer(wx.HORIZONTAL)
			self.sizer_btn.Add(self.btn_copiar, 0, wx.ALL, 5)
			self.sizer_btn.Add(self.btn_guardar, 0, wx.ALL, 5)
			self.sizer_btn.Add(self.btn_cerrar, 0, wx.ALL, 5)
			self.sizer_editor = wx.BoxSizer(wx.VERTICAL)
			self.sizer_editor.Add(self.lbl_editor, 0, wx.ALL, 5)
			self.sizer_editor.Add(self.editor, 1, wx.ALL | wx.EXPAND, 5)
			self.sizer_editor.Add(self.sizer_btn, 0, wx.ALIGN_RIGHT)
			# establecer el sizer
			self.dlg_editor.SetSizer(self.sizer_editor)
			self.dlg_editor.ShowModal()

	# función para que el NVDA vervalice el número de línea en el que se está editando
	def onCursor(self, event):
		# cuando se navegue con algunas de las flechas se dirá el número de línea y la página
		if event.GetKeyCode() == wx.WXK_UP or event.GetKeyCode() == wx.WXK_DOWN or event.GetKeyCode() == wx.WXK_LEFT or event.GetKeyCode() == wx.WXK_RIGHT:
			# obtener el número de línea
			linea = self.editor.GetNumberOfLines()
			# obtener la posición del cursor
			pos = self.editor.GetInsertionPoint()
			# obtener la posición de la línea
			linea_pos = self.editor.XYToPosition(0, linea)
			#número de páginas total?
			paginas=linea//50+1
			# acer que la voz diga en la primera línea de cada página que página 1 de 2, página 2 de 2, etc
			linea_actual = 0
			for i in range(0, linea):
				if i % 50 == 0: linea_actual += 1
				if pos == self.editor.XYToPosition(0, i): break
			# solo desir el mensaje cuadno el cursor está en la primera línea de cada página osea cada 50 líneas o cuando se está en la última línea
			if	pos == self.editor.XYToPosition(0, 0) or pos == self.editor.XYToPosition(0, linea - 1) or pos == self.editor.XYToPosition(0, linea_pos - 1):
				if pos == self.editor.XYToPosition(0, i): ui.message(_("Página ") + str(linea_actual) + _(" de ") + str(paginas))
		event.Skip()

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

	def onCerrarEditor(self, event):
		self.dlg_editor.Destroy()

	def onEliminar(self, event):
		# variables
		self.diario = self.tree.GetItemText(self.tree.GetSelection())
		self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
		self.contar_capitulos = self.tree.GetChildrenCount(self.tree.GetSelection())
		if self.tree.GetItemParent(self.tree.GetSelection()) == self.root:
			# Translators: title of the dialog to delete a diary
			self.dlg_eliminar = wx.MessageDialog(self, _("¿Está seguro de que desea eliminar el diario " + self.diario + "? \nTome en cuenta que esta acción no es rebersible, también eliminará todos los capítulos del diario"), _("Eliminar diario"), wx.YES_NO | wx.ICON_QUESTION)
			if self.dlg_eliminar.ShowModal() == wx.ID_YES:
				# eliminar el diario
				eliminarDiario(self.diario, )
				self.tree.Delete(self.tree.GetSelection())
				# Translators: message when a diary is deleted
				notify = wx.adv.NotificationMessage(title=_("Diario eliminado"), message=_("Se ha eliminado el diario " + self.diario + " con " + str(self.contar_capitulos) + " capítulos"))
				notify.Show(timeout=10)
				if self.tree.GetChildrenCount(self.root) == 0:
					# poner el foco en el botón de menú
					self.btn_menu.SetFocus()
			self.dlg_eliminar.Destroy()
		else:
			self.diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.capitulo = self.tree.GetItemText(self.tree.GetSelection())
			# Translators: title of the dialog to delete a chapter
			self.dlg_eliminar = wx.MessageDialog(self, _("¿Está seguro de que desea eliminar el capítulo " + self.capitulo + "?"), _("Eliminar capítulo"), wx.YES_NO | wx.ICON_QUESTION)
			if self.dlg_eliminar.ShowModal() == wx.ID_YES:
				eliminarCapitulo(self.diario, self.capitulo)
				self.tree.Delete(self.tree.GetSelection())
				notify = wx.adv.NotificationMessage(title=_("Capítulo eliminado"), message=_("El capítulo " + self.capitulo + " del diario " + self.diario + " ha sido eliminado"), parent=None, flags=wx.ICON_INFORMATION)
				notify.Show(timeout=10)

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
		if self.tree.GetItemParent(self.tree.GetSelection()) != self.root:
			self.reproducirSonido("pasar-cap")
			# optener los datos del capítulo como el nombre, el diario la fecha y el número de páginas
			self.name_cap = self.tree.GetItemText(self.tree.GetSelection())
			self.name_diario = self.tree.GetItemText(self.tree.GetItemParent(self.tree.GetSelection()))
			self.dir_diario = os.path.join(os.path.dirname(globalVars.appArgs.configPath), "nvda/diarios", self.name_diario)
			self.dir_capitulo = os.path.join(self.dir_diario, self.name_cap)
			# optener la fecha de creación del capítulo
			self.fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(self.dir_capitulo)))
			self.fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(self.dir_capitulo)))
			#self.num_lineas = len(open(self.dir_capitulo, "r").readlines())
			self.num_paginas = len(open(self.dir_capitulo, "r").readlines())//50+1
			# mostrar los datos en el campo de texto
			info = "Capítulo: " + self.name_cap + "\n" + "Pertenese al diario: " + self.name_diario + "\n" + "Fecha de creación: " + self.fecha + "\n" + "Fecha de modificación: " + self.fecha_mod + "\n" + "Número de páginas: " + str(self.num_paginas)
			self.info.SetValue(info)
		else:
			self.reproducirSonido("pasar-diario")
			# optener los datos del diario como el nombre y el número de capítulos
			self.name_diario = self.tree.GetItemText(self.tree.GetSelection())
			self.dir_diario = os.path.join(os.path.dirname(globalVars.appArgs.configPath), "nvda/diarios", self.name_diario)
			self.fecha = time.strftime("%d/%m/%Y", time.localtime(os.path.getctime(self.dir_diario)))
			self.fecha_mod = time.strftime("%d/%m/%Y", time.localtime(os.path.getmtime(self.dir_diario)))
			self.num_capitulos = len(os.listdir(self.dir_diario))
			# mostrar los datos en el campo de texto de info
			info = "Nombre del diario: " + self.name_diario + "\n" + "Fecha de creación: " + self.fecha + "\n" + "Fecha de modificación: " + self.fecha_mod + "\n" + "Número de capítulos: " + str(self.num_capitulos)
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
		self.dlg_acercaDe.SetVersion("Verción actual: " + self.version)
		self.dlg_acercaDe.SetDescription("Descripción: " + self.descripcion)
		self.dlg_acercaDe.SetWebSite(self.url)
		self.dlg_acercaDe.SetDevelopers([self.autor])
		self.dlg_acercaDe.SetLicence("Este complemento es software libre: usted puede redistribuirlo y/o modificarlo bajo los términos de la Licencia Pública General de GNU publicada por la Free Software Foundation, ya sea la versión 3 de la Licencia, o (a su elección) cualquier versión posterior. Este complemento se distribuye con la esperanza de que sea útil, pero SIN NINGUNA GARANTÍA; sin siquiera la garantía implícita de COMERCIABILIDAD o APTITUD PARA UN PROPÓSITO PARTICULAR. Vea la Licencia Pública General de GNU para más detalles. Debería haber recibido una copia de la Licencia Pública General de GNU junto con este producto. Si no es así, vea <http://www.gnu.org/licenses/>.")
		wx.adv.AboutBox(self.dlg_acercaDe)

	def onDocumentacion(self, event):
		# buscar el archivo fuera del directorio del script prinsipal
		doc = os.path.join(os.path.dirname(__file__), "../", "../", "doc", "es", "readme.html")
		# abrir el archivo en el navegador predeterminado
		os.startfile(doc)

	def onExit(self, event):
		self.Destroy()
		gui.mainFrame.postPopup()

