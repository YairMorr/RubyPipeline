@Echo Off
Set "userSetup=%userprofile%\documents\maya\2018\scripts"
Set "mayaEnv=%userprofile%\documents\maya\2018\"
(
  @echo import rubyscripts as ruby
  @echo import maya.utils
  @echo print "userSetup.py is working"
  @echo maya.utils.executeDeferred("ruby.launchTools()")
  
) > "%userSetup%\userSetup.py"

>nul find "RUBY = R:\Character" "%mayaEnv%\Maya.env" && (
  echo "RUBY = R:\Character" was found.
) || (
  echo RUBY = R:\Character >> "%mayaEnv%\Maya.env"
)

>nul find "ASSETS = R:\Assets" "%mayaEnv%\Maya.env" && (
  echo "ASSETS = R:\Assets" was found.
) || (
  echo ASSETS = R:\Assets >> "%mayaEnv%\Maya.env"
)


>nul find "R:\Assets\_maya\pipeline; R:\Assets\_maya\pipeline\scripts" "%mayaEnv%\Maya.env" && (
  echo "PYTHONPATH" was found.
) || (
  echo R:\Assets\_maya\pipeline; R:\Assets\_maya\pipeline\scripts >> "%mayaEnv%\Maya.env"
)

>nul find "MAYA_SHELF_PATH = R:\Assets\_maya\pipeline" "%mayaEnv%\Maya.env" && (
  echo "MAYA_SHELF_PATH" was found.
) || (
  echo MAYA_SHELF_PATH = R:\Assets\_maya\pipeline >> "%mayaEnv%\Maya.env"
)

