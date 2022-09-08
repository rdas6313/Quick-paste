import sublime
from .logger import Logger


class SublimeApiHelper:

	def __init__(self,plugin):
		self.plugin = plugin

	def getContent(self):
		allcontent = sublime.Region(0,self.plugin.view.size())
		selection = self.plugin.view.sel()
		data = self.plugin.view.substr(selection[0])
		if not data:
			data = self.plugin.view.substr(allcontent)
			selection.add(allcontent)

		return data

	def getFileName(self):
		window = self.plugin.view.window()
		data = window.extract_variables()
		return data.get("file_name","Sample file name")

	def showMessage(self,msg):
		sublime.message_dialog(msg)

	def showErrorMessage(self,msg):
		sublime.error_message(msg)

	def copy(self,data): #copy to clipboard
		sublime.set_clipboard(data)

	def runInBackground(self,callable_method,delay=0):
		sublime.set_timeout_async(callable_method,delay)

	def inputText(self,title,place_holder,on_done,on_cancel=None,on_change=None):
		window = self.plugin.view.window()
		window.show_input_panel(title,place_holder,on_done,on_change,on_cancel)

	def inputPassword(self,title,on_done,on_cancel=None,on_change=None):
		window = self.plugin.view.window()
		panel = window.show_input_panel(title,"",on_done,on_change,on_cancel)
		panel.settings().set("password", True) #only works for Sublime text 3 and 4

	def selectFromList(self,items,on_select,place_holder,initial_index=0):
		window = self.plugin.view.window()
		window.show_quick_panel(items,on_select,0,initial_index,None,place_holder)

	def createNewFile(self,file_name="",syntax="",content=""):
		if type(file_name).__name__ != 'str' or type(syntax).__name__ != 'str' or type(content).__name__ != 'str':
			return False
		window = self.plugin.view.window()
		edit = self.plugin.edit
		view = window.new_file(syntax=syntax)
		view.set_name(file_name)
		view.insert(edit,0,content)
		return True

	def execute(self,cmd,args):
		self.plugin.view.run_command(cmd,args)

		
