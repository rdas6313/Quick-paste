import sublime
import sublime_plugin


class QuickPasteCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		allcontent = self.view.visible_region()		
		selection = self.view.sel()
		data = self.view.substr(selection[0])
		if not data:
			data = self.view.substr(allcontent)
			selection.add(allcontent)
		#print(data)
