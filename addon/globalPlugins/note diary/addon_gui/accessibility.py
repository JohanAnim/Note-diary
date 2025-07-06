# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan A G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.

import wx

class Accesibilidad(wx.Accessible):
	def __init__(self, win):
		wx.Accessible.__init__(self, win=win)
		# optener el objeto actual que contiene la accesibilidad
		self.objeto = win
		self.nombre = self.objeto.GetLabel()
		self.descripcion = ""
		self.role = wx.ROLE_NONE
		self.estado = wx.ACC_STATE_SYSTEM_DEFAULT

	def GetRole(self, childId):
		return (wx.ACC_OK, self.role)

	def GetState(self, childId):
		return (wx.ACC_OK, self.estado)

	def GetName(self, childId):
		return (wx.ACC_OK, self.nombre)

	def GetDescription(self, childId):
		return (wx.ACC_OK, self.descripcion)

	def SetNombre(self, nombre):
		self.nombre = nombre

	def SetDescripcion(self, descripcion):
		self.descripcion = descripcion

	def SetRole(self, role):
		self.role = role

	def SetEstado(self, estado):
		self.estado = estado

	# metodos para optener el nombre actual del objeto, la descripcion, el role y el estado
	def GetNombre(self):
		return self.nombre
	
	def GetDescripcion(self):
		return self.descripcion

	def GetEstado(self):
		return self.estado
