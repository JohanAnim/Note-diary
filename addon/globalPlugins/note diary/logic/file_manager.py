# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import os
import shutil

import globalVars

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