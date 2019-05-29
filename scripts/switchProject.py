window = cmds.window(title="Switch Project")

calendarPath = os.path.join("R:/", "Insta Calendar", "2019")

cmds.rowLayout(numberOfColumns=5)

yearMenu = cmds.optionMenu(label="Year ")
cmds.menuItem("2019")

monthMenu = cmds.optionMenu(label="Month ", changeCommand=updateMonth)
projectsMenu = cmds.optionMenu(label="Projects ", changeCommand=updateProjects)
filesMenu = cmds.optionMenu(label="Files ")

actionBtn = cmds.button(label="Switch Project", c=buttonAction)

updateMenus()
cmds.showWindow(window)

def updateMenus():
	
	for monthItem in os.listdir(calendarPath):
		cmds.menuItem(monthItem, parent=monthMenu)
	monthMenuItemNum = cmds.optionMenu(monthMenu, q=True, ni=True)
	cmds.optionMenu(monthMenu, e=True, sl = monthMenuItemNum-2) #Change sl to fit folders!!

	updateMonth(cmds.optionMenu(monthMenu, q=True, v=True))
		
				
def updateMonth(item):
	if cmds.optionMenu(projectsMenu, q=True, ni=True) > 0:
		for items in cmds.optionMenu(projectsMenu, q=True, ill=True):
			cmds.deleteUI(items)
	
	for projectItem in os.listdir(os.path.join(calendarPath, item)):
		cmds.menuItem(projectItem, parent=projectsMenu)
		
	updateProjects(cmds.optionMenu(projectsMenu, q=True, v=True))
	
	
def updateProjects(item):
	if cmds.optionMenu(filesMenu, q=True, ni=True) > 0:
		for items in cmds.optionMenu(filesMenu, q=True, ill=True):
			cmds.deleteUI(items)
	
	fullPath = os.path.join(calendarPath, cmds.optionMenu(monthMenu, q=True, v=True), item, "maya", "scenes")
	
	if os.path.isdir(fullPath):
		for files in os.listdir(fullPath):
			fileName, extension = os.path.splitext(files)
			
			if extension == '.ma':
				cmds.menuItem(files, parent=filesMenu)
		cmds.button(actionBtn, e=True, label="Switch Project")
	
	else:
		cmds.menuItem('No files found.', parent=filesMenu)
		cmds.button(actionBtn, e=True, label="Create New")
	

def buttonAction(label, *args):
	monthSel = cmds.optionMenu(monthMenu, q=True, v=True)
	projectSel = cmds.optionMenu(projectsMenu, q=True, v=True)
	fileSel = cmds.optionMenu(filesMenu, q=True, v=True)
	
	if fileSel == 'No files found.':
		path = os.path.join(calendarPath, monthSel, projectSel)
		print 'Creating a new project in ' + path
	else:
		path = os.path.join(calendarPath, monthSel, projectSel, fileSel)
		print 'Switching to project ' + path
		