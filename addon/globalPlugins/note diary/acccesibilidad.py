
import wx

class Accesibilidad(wx.Accessible):
	def __init__(self, nombre, descripcion, role, estado):
		wx.Accessible.__init__(self)
		# optener el elemento actual que contiene la accesibilidad
		self.objeto = self.GetWindow()
		self.nombre = nombre
		self.descripcion = descripcion
		self.role = role
		self.estado = estado

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
		# anunciar al lector de pantalla cuando el estado cambia
		wx.NotifyEvent(wx.ACC_EVENT_OBJECT_STATECHANGE, wx.ACC_STATE_SYSTEM_COLLAPSED if self.estado == wx.ACC_STATE_SYSTEM_COLLAPSED else wx.ACC_STATE_SYSTEM_EXPANDED)

	# metodos para optener el nombre actual del objeto, la descripcion, el role y el estado
	def GetNombre(self):
		return self.nombre
	
	def GetDescripcion(self):
		return self.descripcion

	def GetEstado(self):
		return self.estado
