import sublime
import sublime_plugin
from .logger import Logger


class SublimeApi(sublime_plugin.TextCommand):
	
	log = Logger()

	def init(self):
		pass

	def getContent(self):
		allcontent = sublime.Region(0,self.view.size())
		selection = self.view.sel()
		data = self.view.substr(selection[0])
		if not data:
			data = self.view.substr(allcontent)
			selection.add(allcontent)

		return data

	def getFileName(self):
		window = self.view.window()
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
		window = self.view.window()
		window.show_input_panel(title,place_holder,on_done,on_change,on_cancel)

	def selectFromList(self,items,on_select,place_holder,initial_index=0):
		window = self.view.window()
		window.show_quick_panel(items,on_select,0,initial_index,None,place_holder)

		
