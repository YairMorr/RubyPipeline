import maya.cmds as cmds
import os
import maya.mel as mel
import rubyManager_v2 as manager

reload(manager)

def sayHello():
	print("Hello")

def xRaySwitcher():
	selected = cmds.ls(sl=True,long=True)

	for eachSel in selected:
		if cmds.displaySurface(eachSel, q=True, xRay=True)[0] == True:
			cmds.displaySurface(eachSel, xRay=False)
		else:
			cmds.displaySurface(eachSel, xRay=True)

def loadEnvironment():
	if cmds.namespace(exists="Environment"):
		print "Environment already loaded."
	else:
		cmds.file("R:\Assets\Light_Rigs\Ruby_environment.ma", r=True, namespace = "Environment")

def createImagePlane():
	if cmds.objExists("Environment:Cam"):
		plate = cmds.imagePlane(fileName="../direction/plate.jpg", camera="Environment:Cam")
		cmds.setAttr(plate[1] + ".depth", 1000)
		cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 1)
		width = float(cmds.getAttr(plate[1] + ".coverageX"))
		height = float(cmds.getAttr(plate[1] + ".coverageY"))
		ratio = width/height
		cmds.setAttr("defaultResolution.width", width)
		cmds.setAttr("defaultResolution.height", height)
		cmds.setAttr("defaultResolution.deviceAspectRatio", ratio)
		cmds.setAttr(plate[1] + ".sizeY", cmds.getAttr(plate[1] + ".sizeX") / ratio)
		print "Image plane created successfully. Render resolution updated accordingly."
	else:
		print "Load environment file with a camera before creating image plane"

def deleteMenuItems(menuName):
	for items in cmds.optionMenu(menuName, q=True, ill=True):
		cmds.deleteUI(items)
			
def populateMenuItems(menuName, path):
	if os.path.isdir(path):
		if cmds.optionMenu(menuName, q=True, label=True) == "Files":
			for item in os.listdir(path):
				filename, extension = os.path.splitext(item)
				if extension == '.ma':
					cmds.menuItem(item, parent=menuName)
		else:
			for item in os.listdir(path):
				cmds.menuItem(item, parent=menuName)
	else:
		cmds.menuItem("No files found.", parent=menuName)	
	
def loadRubyBtn(versionsMenu):
	
	selectedItem = cmds.optionMenu(versionsMenu, q=True, v=True)
	versionFolder = selectedItem[10:13] + '0'
	fullPath = os.path.join("R:/Character", versionFolder, selectedItem)
			
	for ref in cmds.file( q=True, r=True):
		if ref.find("Ruby_char") > 0:
			result = cmds.confirmDialog(title="Ruby already exists", message='There is already a reference to Ruby in the scene. This operation will replace the existing Ruby. Proceed?', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
			if result == 'OK':
				print 'replacing reference'
				rubyRN = os.path.splitext(os.path.basename(ref))[0] + "RN"
				cmds.file(fullPath, loadReference=rubyRN)
		else:			
			result = cmds.confirmDialog(title="Reference Ruby", message='Reference Ruby ' + selectedItem[10:14] + '?', button=['OK', 'Cancel'], defaultButton='OK', cancelButton='Cancel', dismissString='Cancel')
			if result == 'OK':
				cmds.file(fullPath, r=True, namespace="Ruby")
			else:
				print 'Referencing cancelled by user.'
	
def populateMenuItemsRuby(menuName, path):
	if os.path.isdir(path):
		for folder in os.listdir(path):
			if os.path.basename(folder)[0] == "v":
				for currentFile in os.listdir(os.path.join(path, folder)):
					filename, extension = os.path.splitext(currentFile)
					if extension == '.ma' and "_char" in filename and filename[-1].isdigit():
						cmds.menuItem(currentFile, parent=menuName)
		cmds.optionMenu(menuName, e=True, sl= cmds.optionMenu(menuName, q=True, ni=True))
	else:
		cmds.menuItem("No files found.", parent=menuName)

def setRenderAttrs():
	cmds.setAttr("defaultRenderGlobals.imageFilePrefix", "<RenderLayer>/<RenderLayer>_<RenderPass>", type="string")
	cmds.setAttr("defaultArnoldRenderOptions.AASamples", 7)
	cmds.setAttr("defaultArnoldRenderOptions.GIDiffuseSamples", 5)
	cmds.setAttr("defaultArnoldRenderOptions.GISpecularSamples", 5)
	cmds.setAttr("defaultArnoldRenderOptions.GITransmissionSamples", 4)
	cmds.setAttr("defaultArnoldRenderOptions.GISssSamples", 5)
	cmds.setAttr("defaultArnoldRenderOptions.GIVolumeSamples", 0)

	rubyPlane = cmds.ls('imagePlaneShape1')[0] # selects image plane
	cmds.setAttr(rubyPlane + '.alphaGain', 0) # sets image plane's Alpha Gain attribute to 0
	cmds.setAttr(rubyPlane + '.displayMode', 0) # sets image plane's Display Mode to None
	
	if cmds.objExists("imagePlaneShape1"):
		cmds.setAttr("defaultResolution.lockDeviceAspectRatio", 1)
		width = float(cmds.getAttr("imagePlaneShape1.coverageX"))
		height = float(cmds.getAttr("imagePlaneShape1.coverageY"))
		ratio = width/height
		cmds.setAttr("defaultResolution.width", width)
		cmds.setAttr("defaultResolution.height", height)
		cmds.setAttr("defaultResolution.deviceAspectRatio", ratio)

class loadHDRI(object):
	def __init__(self):
		pass
	
	def show(self):
		self.loadHDRI()

	def loadHDRI(self):
		thumbsPath = "R:\Assets\Textures\HDRis\\thumbs"
		thumbBtn = {}
    
		if cmds.window('HDRI Gallery', exists = True):
			cmds.deleteUI('HDRI Gallery')

		# create our window
		self.window = cmds.window('HDRI Gallery', widthHeight = (1000, 500), title = 'HDRI Gallery')

		cmds.setParent(menu=True)

		# create a main layout
		scrollLayout = cmds.scrollLayout(horizontalScrollBarThickness=16, verticalScrollBarThickness=16)
		cmds.gridLayout( numberOfColumns=4, cellWidthHeight=(256, 192))

		for thumbnail in os.listdir(thumbsPath):
			fullPath = os.path.join(thumbsPath, thumbnail)
			hdrfileName = os.path.splitext(thumbnail)[0] + '.hdr'
			self.button = cmds.iconTextButton(style='iconAndTextVertical', image1=fullPath, label=hdrfileName, c=lambda x=thumbnail:self.TakeAction(x))

		cmds.showWindow(self.window)

	def TakeAction(self, *args):
		hdrFileName = os.path.splitext(str(args[0]))[0]
		hdrPass = os.path.join("R:\Assets\Textures\HDRis", hdrFileName + '.hdr')
        
		if not cmds.objExists('File_hdri'):
			cmds.createNode('file', n='File_hdri')
			cmds.connectAttr("File_hdri.outColor", "Environment:aiSkyDomeLightShape.color")
			print 'image node file created.'
			
		print 'HDRI switched to: ', hdrPass
		cmds.setAttr("File_hdri.fileTextureName", hdrPass, type="string")

class incrementSave():
	def __init__(self):
		pass
	
	def checkLatestVersion(self, currentPath):
		dirName = os.path.dirname(currentPath)
		latestVersion = 1
		
		for filename in os.listdir(dirName):
			currentfile, extension = os.path.splitext(filename)
			if extension == ".ma":
				currentVersion = int(currentfile.split("v")[1])
				if latestVersion < currentVersion:
					latestVersion = currentVersion
		
		return latestVersion

	def run(self):
		currentPath = cmds.file(q=1, sn=1)
		
		latestVersion = self.checkLatestVersion(currentPath) + 1
		latestVersion = "%02d" % (latestVersion,)
		
		currentFilename, currentExt = os.path.splitext(currentPath)
		currentFilename = os.path.basename(currentFilename)
		currentVersion = currentFilename.split("v")
		
		newVersion = currentVersion[0] + "v" + latestVersion + '.ma'
		
		currentFrame = cmds.currentTime(q=True)
		cmds.currentTime(0)
		print "Switched to frame 0 for saving purposes"
		cmds.file(rename = newVersion)
		cmds.file(save=True)
		cmds.currentTime(currentFrame)
		print "Switched back to frame ", currentFrame

		print "Increment and saved new version: " + newVersion

def saveRubyFile():
	currentFrame = cmds.currentTime(q=True)
	print "Switched to frame 0 for saving purposes"
	cmds.file(save=True)
	cmds.currentTime(currentFrame)
	print "Switched back to frame ", currentFrame
	print "Scene saved: ", cmds.file(q=True, sn=1)

def create_shadowPlane():
	if cmds.objExists("shadow_plane"):
		print "Shadow plane already exists in the scene."
	else:
		shadowPlane = cmds.polyPlane(n="shadow_plane", sx=10, sy=10)
		cmds.scale( 300, 300, 300, shadowPlane)
		cmds.select(shadowPlane)
		cmds.sets(name='matte_SG', renderable=True, empty=True)
		cmds.shadingNode('aiShadowMatte', name="shadowMatte_MAT", asShader=True)
		cmds.surfaceShaderList('shadowMatte_MAT', add="matte_SG")
		cmds.sets(shadowPlane, e=True, forceElement="matte_SG")
		print "Shadow plane created."

def tearOffCam():
	winWidth = 640
	winHeight = 480
	rubyCam = 'Environment:Cam'
	rubyPlane = 'imagePlaneShape1'
	
	if rubyPlane:
		winWidth = cmds.getAttr(rubyPlane + '.coverageX')
		winHeight = cmds.getAttr(rubyPlane + '.coverageY')
		winRatio = (winWidth*1.0)/winHeight
		
		if winHeight > 1300:
			print 'height condition winRatio: ', winRatio
			winHeight = 1300
			winWidth = winHeight*winRatio
			
		elif winWidth > 2000:
			print 'width condition winRatio: ', winRatio
			winWidth = 2000
			winHeight = winWidth/winRatio
	
	rubyWindow = cmds.window(title="Ruby Cam", widthHeight=[winWidth,winHeight])
	cmds.paneLayout()
	
	rubyPanel = cmds.modelPanel(camera=rubyCam)
	rubyModelEditor = cmds.modelPanel(rubyPanel, q=True, modelEditor=True)
	cmds.modelEditor(rubyModelEditor, edit=True, displayAppearance='smoothShaded', displayTextures=True, nurbsCurves=False, joints=False, wireframeOnShaded=False, locators=False)
	cmds.showWindow(rubyWindow)

def launchTools():
	toolsVer = "1.7"
	
	#if cmds.window(q=True, title=True):
	#	print "Hey!"
	#	cmds.deleteUI("rubyTools")
		
	rubyTools = cmds.window(title = "rubyTools")
	
	loadHDR = loadHDRI()
	incrmntSave = incrementSave()
	#loadHDR.show()
	#### <----- Project management controls ------>
	cmds.rowColumnLayout(numberOfRows=1, columnSpacing=[5, 5], rowOffset=[1, "both", 2], columnOffset=[1, "both", 2])

	rubyManager = manager.fileManager("R:/Insta Calendar/")
	rubyManager.show()

	#### <----- Project management controls ------>

	#### <----- Saving commands ------>
	cmds.separator( style='single', width=10 )
	cmds.iconTextButton( style="iconAndTextHorizontal", image1='R:/Assets\_maya\pipeline\icons\\save.png', label="Save", c=saveRubyFile)
	cmds.iconTextButton( style="iconAndTextHorizontal", image1='R:/Assets\_maya\pipeline\icons\\add-file.png', label="Increment & Save", c=incrmntSave.run)
	#### <----- Saving commands ------>	
	
	cmds.separator( style='single', width=10 )
	#### <----- Ruby Loader   -------------------->
	versionsMenu = cmds.optionMenu(label="Load Ruby")
	loadRuby = cmds.iconTextButton(style="iconOnly", image1='R:/Assets\_maya\pipeline\icons\\smile.png', label="Reference Ruby", c=lambda *args:loadRubyBtn(versionsMenu))
	populateMenuItemsRuby(versionsMenu, "R:/Character")
	#### <----- Ruby Loader   -------------------->
	cmds.separator( style='single', width=10 )
	#### <----- Tools buttons -------------------->
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\park.png', label='New Environment', c=loadEnvironment )
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\image.png', label='Create imagePlane', c=createImagePlane )
	cmds.iconTextButton( style='iconOnly', image1='R:/Assets\_maya\pipeline\icons\stop.png', label='Create shadowPlane', c=create_shadowPlane)
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\diffuser.png', label='Assign HDRI to Dome', c=loadHDR.show )
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\wireframe.png', label='Toggle xRay', c=xRaySwitcher )
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\camview.png', label='Tear off Cam', c=tearOffCam )
	#### <----- Tools buttons -------------------->
	cmds.separator( style='single', width=10 )
	#### <----- Render buttons -------------------->
	cmds.iconTextButton( style='iconAndTextHorizontal', image1='R:/Assets\_maya\pipeline\icons\settings.png', label='Set Render Settings', c=setRenderAttrs )
	#### <----- Render buttons -------------------->
	cmds.dockControl( area='top', content=rubyTools, label="Ruby Tools v" + toolsVer )

	def __init__(self):
		pass
	

#### thumbnail resize
def resizeAllImages(width, height):
	import maya.OpenMaya as om
	#thumbnail size: 256x192
	thumbsPath = "R:\Assets\Textures\HDRis\\thumbs"
	for thumbnail in os.listdir(thumbsPath):
		sourceImage = os.path.join(thumbsPath, thumbnail)
		image = om.MImage()
		image.readFromFile(sourceImage)
		
		image.resize(width,height)
		image.writeToFile(sourceImage, 'jpg')


def resizeImage(image, width = 256, height = 192):
	import maya.OpenMaya as om
	thumbsPath = "R:\Assets\Textures\HDRis\\thumbs"
	sourceImage = os.path.join(thumbsPath, image)
	image = om.MImage()
	image.readFromFile(sourceImage)
	
	image.resize(width,height)
	image.writeToFile(sourceImage, 'jpg')