# -*- coding: utf-8 -*-
# Copyright (C) 2023 Johan G <gutierrezjohanantonio@gmail.com>
# This file is covered by the GNU General Public License.
import wx

# modulo para mejorar la accesibilidad de algunos elementos
# el menú
class MenuAccessible(wx.Accessible):
	def __init__(self, window):
		wx.Accessible.__init__(self)
		self.window = window

	def GetRole(self, childId):
		return (wx.ACC_OK, wx.ROLE_SYSTEM_BUTTONMENU)
	def GetState(self, childId):
		return (wx.ACC_OK, wx.ACC_STATE_SYSTEM_FOCUSABLE | wx.ACC_STATE_SYSTEM_FOCUSED)
