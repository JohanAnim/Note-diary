# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import os
import wx
import ui

from logic import file_manager

def search_diaries_and_chapters(main_dialog_instance, text, filter_type):
	# Crear un diccionario para almacenar los diarios y capítulos que coinciden con la búsqueda
	coincidencias = {}

	# Filtrar los diarios y capítulos según el texto de búsqueda y el tipo de filtro
	for diario in main_dialog_instance.diarios:
		if filter_type == "Capítulos":
			coincidencias_capitulos = [capitulo for capitulo in file_manager.enlistarCapitulos(diario) if text in capitulo.upper()]
			if coincidencias_capitulos:
				coincidencias[diario] = coincidencias_capitulos

		elif text in diario.upper():
			coincidencias[diario] = file_manager.enlistarCapitulos(diario)

	# Actualizar el árbol con los resultados de la búsqueda
	main_dialog_instance.tree.Freeze()
	main_dialog_instance.tree.DeleteAllItems()
	main_dialog_instance.root = main_dialog_instance.tree.AddRoot("diarios")
	for diario, capitulos in coincidencias.items():
		diario_node = main_dialog_instance.tree.AppendItem(main_dialog_instance.root, diario)
		for capitulo in capitulos:
			main_dialog_instance.tree.AppendItem(diario_node, capitulo)
			main_dialog_instance.text_ctrl.SetFocus()

	# Reproducir un sonido según el resultado de la búsqueda
	if coincidencias:
		main_dialog_instance.reproducirSonido("busqueda-exitosa")
		# sacar la cantidad de diarios y capítulos que coinciden con la búsqueda
		num_resultados = len(coincidencias)
		if num_resultados == 1: wx.CallLater(100, lambda: ui.message(_("Se encontró {} resultado").format(num_resultados)))
		else: wx.CallLater(100, lambda: ui.message(_("Se encontraron {} resultados").format(num_resultados)))
	else:
		main_dialog_instance.reproducirSonido("busqueda-fallida")
		wx.CallLater(100, lambda: ui.message(_("No se encontraron resultados")))

	# Expandir todos los diarios que contienen coincidencias en el filtro de los caps
	if filter_type == "Capítulos":
		main_dialog_instance.tree.ExpandAll()

	main_dialog_instance.tree.Thaw()