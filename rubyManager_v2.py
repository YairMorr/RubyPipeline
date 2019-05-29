import json
import ast
import os
import maya.mel as mel
import maya.cmds as cmds

class fileManager(object):
	def __init__(self, root):
		self.root = root
		self.currentPath = ""
		self.yearList = []
		self.monthList = []
		self.projectList = []
		self.filesList = []
		self.menus = []
		self.prefs = []
		self.prefsFilename = os.path.join(os.environ["TMP"], "rubyScriptPrefs.txt")
		
	def getPrefs(self):
		if os.path.isfile(self.prefsFilename):
			prefs = open(self.prefsFilename, "r")
			prefsContent = ast.literal_eval(prefs.read())
			prefs.close()
			return prefsContent
		else:
			print "No prefs file found."
			return [0, 0, 0, 0]
	
	def updatePrefs(self, newPrefs):
		if newPrefs:
			print "Updating Ruby prefs"
			json.dump(newPrefs, open(self.prefsFilename, 'w'))


	def updateOptionMenu(self, i, selectedMenu, iterPath, prefs):
		prefsMatch = False
		sl=0
		
		if os.path.exists(iterPath):
			if cmds.optionMenu(selectedMenu, q=True, sl=True) > 0: #Delete items if already populated
				for item in cmds.optionMenu(selectedMenu, q=True, ill=True):
					cmds.deleteUI(item)

			for item in os.listdir(iterPath):

				if i == 3:
					filename, extension = os.path.splitext(item)
					if extension == '.ma':
						cmds.menuItem(item, parent=selectedMenu)
				else:
					cmds.menuItem(item, parent=selectedMenu)

				if item == prefs:
					sl=cmds.optionMenu(selectedMenu, q=True, ni=True)
					cmds.optionMenu(selectedMenu, e=True, sl=sl)

			if cmds.optionMenu(selectedMenu, q=True, sl=True) == 0: #If list is empty, add No items found item
				cmds.menuItem('No items found.', parent=selectedMenu)
		else:
			cmds.menuItem('No Maya project found.', parent=selectedMenu)


	def updateMenus(self, *args):
		self.prefs = self.getPrefs()
		iterPath = self.root
		newPrefs = []
		changeFlag = 10
		
		for i, selectedMenu in enumerate(self.menus):

			if i == 3: #if inside project folder, add Maya's folder structure to path
				if os.path.exists(os.path.join(iterPath, "maya", "scenes")):
					iterPath = os.path.join(iterPath, "maya", "scenes")

			if args:
				if args[0] == cmds.optionMenu(selectedMenu, q=True, v=True):
					changeFlag = i
					print 'line81, changeFlag: ', changeFlag
				elif i > changeFlag:
					self.updateOptionMenu(i, selectedMenu, iterPath, self.prefs[i])
			else:
				self.updateOptionMenu(i, selectedMenu, iterPath, self.prefs[i])

			iterPath = os.path.join(iterPath, cmds.optionMenu(selectedMenu, q=True, v=True)) #go into next selected folder
			newPrefs.append(cmds.optionMenu(selectedMenu, q=True, v=True))

		self.currentPath = iterPath
		self.updatePrefs(newPrefs)
	
	def createProject(self, *args):
		newRoot = os.path.dirname(os.path.dirname(self.currentPath))
		message = "Creating a new project in:\n\n" + newRoot + "\n\nEnter name:"

		projectName = cmds.promptDialog(title="New project", message=message, button=['OK', 'Cancel'], defaultButton='OK', text=cmds.optionMenu(self.menus[2], q=True, v=True), cancelButton='Cancel', dismissString='Cancel')
		
		if projectName == 'OK':
			if cmds.promptDialog(q=True, text=True) == "":
				print "Empty project name. Aborting."
			else:
				switchProjectDialog = cmds.confirmDialog(title='New Maya file', message='Create and open a new Maya file?', button=['Yes', "No new file for now"], defaultButton='OK', cancelButton="No new file for now", dismissString="No new file for now")
				
				newFolders = ["maya", "marvelous", "export", "comp"]
				newProjectPath = os.path.join(newRoot, cmds.promptDialog(q=True, text=True))

				for folder in newFolders:
					projectSubfolders = os.path.join(newProjectPath, folder)
					if not os.path.exists(projectSubfolders):
						os.makedirs(projectSubfolders)
						print "Creating new folder: " , projectSubfolders
							
				if switchProjectDialog == "Yes":
					print 'Creating new Maya file'
					
					workspacePath = os.path.join(newProjectPath, "maya")
					folderPath = os.path.join(workspacePath, "scenes")
					fileName = cmds.promptDialog(q=True, text=True) + "_v01.ma"

					mel.eval('setProject \"' + workspacePath.replace('\\', r'\\') + '\"')

					print "Switching to workspace: ", workspacePath

					for file_rule in cmds.workspace(query=True, fileRuleList=True):
						if file_rule == "images" or file_rule == "sourceImages" or file_rule == "fileCache" or file_rule == "scene":
							file_rule_dir = cmds.workspace(fileRuleEntry=file_rule)
							maya_file_rule_dir = os.path.join( workspacePath, file_rule_dir)

							if not os.path.exists( maya_file_rule_dir ):
								os.makedirs( maya_file_rule_dir )

					cmds.file(new=True, force=True)
					cmds.file(folderPath, rename=os.path.join(folderPath, fileName))
					cmds.file(f=True, type="mayaAscii", save=True)

	def switchProject(self, *args):
		fullPath = os.path.join(self.currentPath, cmds.optionMenu(self.menus[3], q=True, v=True))
		print "Switching to project: ", fullPath
		workspacePath = os.path.dirname(os.path.dirname(self.currentPath))
		print 'workspacePath:', workspacePath
		cmds.workspace(workspacePath, openWorkspace=True)
		cmds.file(new=True, force=True)
		cmds.file(fullPath, o=True)

	def reloadMenus(self):
		iterPath = self.root
		self.prefs = self.getPrefs()
		matchFlag = False
		matchIndex = 0

		for i, selectedMenu in enumerate(self.menus):

			if i > 0: #updating path
				iterPath = os.path.join(iterPath, cmds.optionMenu(self.menus[i - 1], q=True, v=True))
			if i == 3:
				iterPath = os.path.join(iterPath, "maya", "scenes")

			for item in cmds.optionMenu(selectedMenu, q=True, ill=True):
				cmds.deleteUI(item)

			if os.path.exists(iterPath):
				for item in os.listdir(iterPath):
					cmds.menuItem(item, parent=selectedMenu)

					if self.prefs[i] == item:
						matchFlag = True
						matchIndex = cmds.optionMenu(selectedMenu, q=True, ni=True)
			else:
				cmds.menuItem("No items found.", parent=selectedMenu)

			if matchFlag == True:
				cmds.optionMenu(selectedMenu, e=True, sl=matchIndex)
			
		print "Folder menus reloaded."

	def show(self):
		#self.window = cmds.window('Project Explorer', widthHeight = (784, 50))

		#cmds.rowLayout(numberOfColumns=7)
		cmds.iconTextButton( style="iconAndTextHorizontal", image1='R:/Assets\_maya\pipeline\icons\\folder.png', label="Create New Project", c=self.createProject)
		cmds.iconTextButton( style="iconOnly", image1='R:/Assets\_maya\pipeline\icons\\reload.png', label="Save", c=self.reloadMenus)

		self.menus.append(cmds.optionMenu(label="Year", cc=self.updateMenus))
		self.menus.append(cmds.optionMenu(label="Month", cc=self.updateMenus))
		self.menus.append(cmds.optionMenu(label="Project", cc=self.updateMenus))
		self.menus.append(cmds.optionMenu(label="File", cc=self.updateMenus))
		
		#cmds.iconTextButton(style="iconAndTextHorizontal", image1='R:/Assets\_maya\pipeline\icons\\switch.png', label="Load Project")
		switchBtn = cmds.iconTextButton(style="iconAndTextHorizontal", image1='R:/Assets\_maya\pipeline\icons\\switch.png', label="Switch Project", c=self.switchProject)
		
		# cmds.showWindow(self.window)

		self.updateMenus()

	def testyTest(self):
		print "test"