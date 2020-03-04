#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import shutil
import glob
import errno, stat
import re
import pkg_resources
import argparse
from argparse import RawTextHelpFormatter

"""
createmodulefromskeleton.py - Create your own submodule form a oneplace Skeleton_skeleton
 Renames and cleanup code structure
 Usage: createmodulefromskeleton.py path/to/module modulename

 @author Verein onePlace
 @copyright (C) 2020  Verein onePlace <admin@1plc.ch>
 @license https://opensource.org/licenses/BSD-3-Clause
 @version 1.0.2
 @since 1.0.0
"""
"""
"""

class Skeleton:
  def __init__(self,name):
    self.name = name.split('-')
  def setVendor(self,vendor_upper,vendor_lower):
    self.vendorU = vendor_upper
    self.vendorL = vendor_lower
  def set(self,module):
    self.module = module
  def getName(self,upper):
    return '-'.join(getupperlower(self.name,upper))
  def getNamespace(self,upper):
    return '\\'.join(getupperlower(self.name,upper))
  def getNamespace2(self,upper):
    return '\\\\'.join(getupperlower(self.name,upper))
  def getRouteName(self,upper):
    return '/'.join(getupperlower(self.name,upper))
  def getTableName(self,upper):
    return '_'.join(getupperlower(self.name,upper))
  def getModelName(self,upper):
    return ''.join(getupperlower(self.name[-1],upper))
  def getFormName(self,upper):
    return ''.join(getupperlower(self.name,upper))
  def getBaseName(self,upper):
    return ''.join(getupperlower(self.name[0],upper))
  def getLabel(self,upper):
    return ' '.join(getupperlower(self.name,upper))
  def getVendor(self,upper):
    if upper:
      #print(self.vendor)
      return self.vendorU[:-1]
    else:
      return self.vendorL
  def get(self):
    return [
    [self.getVendor(True),self.module.getVendor(True)],
    [self.getVendor(False),self.module.getVendor(False)],
    [self.getName(True),self.module.getName(True)],
    [self.getName(False),self.module.getName(False)],
    [self.getTableName(True),self.module.getTableName(True)],
    [self.getTableName(False),self.module.getTableName(False)],
    [self.getNamespace(True),self.module.getNamespace(True)],
    [self.getNamespace(False),self.module.getNamespace(False)],
    [self.getNamespace2(True),self.module.getNamespace2(True)],
    [self.getNamespace2(False),self.module.getNamespace2(False)],
    [self.getRouteName(True),self.module.getRouteName(True)],
    [self.getRouteName(False),self.module.getRouteName(False)],
    [self.getFormName(True),self.module.getFormName(True)],
    [self.getFormName(False),self.module.getFormName(False)],
    [self.getBaseName(True)+"1",self.module.getBaseName(True)],
    [self.getBaseName(False)+"1",self.module.getBaseName(False)],
    [self.getModelName(True),self.module.getModelName(True)],
    [self.getModelName(False),self.module.getModelName(False)],
    [self.getBaseName(True),self.module.getBaseName(True)],
    [self.getBaseName(False),self.module.getBaseName(False)],
    ]
  def getview(self):
    return [
      [self.getVendor(True),self.module.getVendor(True)],
      [self.getVendor(False),self.module.getVendor(False)],
      [self.getModelName(True)+"2",self.module.getModelName(True)],
      [self.getModelName(False)+"2",self.module.getModelName(False)],
      [self.getBaseName(True),self.module.getBaseName(True)],
      [self.getBaseName(False),self.module.getBaseName(False)],
      ]
# Remove Files and Folders (wildcard only for files)
aToDelFiles = []
aToDelFiles.append("/data/*.sh")
aToDelFiles.append("/data/*.ps1")
aToDelFiles.append("/data/*.py")
aToDelFiles.append("/view/layout/*default.phtml")
aToDelFiles.append("/CHANGELOG.md")
aToDelFiles.append("/mkdocs.yml")
aToDelFiles.append("/README.md")

aToDelDirs = []
aToDelDirs.append("/.idea")
aToDelDirs.append("/docs")
aToDelDirs.append("/.git")

# Whitelist from renaming
aWhiteList = []
aWhiteList.append("/language/")


#default Values
sDefaultVendor = "OnePlace"
sSkeletonName = "Skeleton-Skeleton"
sSkeletonVersion = "1.0.0"
sModulePhp = "Module.php"
sModuleConfig = "module.config.php"
sModulePhpNC = "Module.php.no_controller"
sModuleConfigNC = "module.config.php.no_controller"
sComposerJson = "composer.json"
sModuleConfig = "module.config.php"
sInstallSql = "install.sql"
aHooks = []
aIncludes = []

aSkeletonControllerNames = []
aSkeletonControllers = []
aModuleControllerNames = []
aModuleControllers = []
aSkeletonRouteNames = []
aSkeletonRoutes = []
aModuleRouteNames = []
aModuleRoutes = []

"""
  Helper Functions and Class
"""
def v_print(value):
  if DEBUG :
    print(value)

def remove_readonly(func, path, exc_info):
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise

# Convert Module Name for Skeleton to skeleton or vs
def getupperlower(name, upper = True):
  aModule=[]

  if not isinstance(name, list):
    name = [name]
  for item in name:
    if(item[0].islower() and upper):
      aModule.append(item[0].upper() + item[1:])
    elif(item[0].isupper() and not upper):
      aModule.append(item[0].lower()+ item[1:])
    else:
      aModule.append(item)
  return aModule

#regex validator
def regex_version_validate(arg_value, pat=re.compile(r'(?:(\d+)\.)?(?:(\d+)\.)?(?:(\d+)\.\d+)')):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value
def regex_skeleton_module(arg_value, pat=re.compile(r'((([\w]+))-){1}')):
    if not pat.match(arg_value):
        raise argparse.ArgumentTypeError
    return arg_value

oArgParser = argparse.ArgumentParser(formatter_class=RawTextHelpFormatter,
                                     description='Create a new Submodule based on the current PLC_X_Skeleton_Skeleton',
                                     epilog='Run it directly inside /data/ !\n\n'
                                            'Example:\n'
                                            + sys.argv[0] + ': ../../PLC_X_Modul modul-submodule -mvp\n'
                                            + sys.argv[0] + ': ../../PLC_X_Modul modul-submodule --parent contact-history --version 1.0.1 -mvp\n')
oArgParser.add_argument("path", help='path to your new submodule')
oArgParser.add_argument("submodule", help='your submodule: skeleton-skeleton',default=sSkeletonName,type=regex_skeleton_module)
oArgParser.add_argument("--version", help='X.X.X - version of submodule',default=sSkeletonVersion,type=regex_version_validate)
oArgParser.add_argument("--parent", help=sSkeletonName+' - skeleton name',default=sSkeletonName,type=regex_skeleton_module)
oArgParser.add_argument("--upgrade", help='path to project')
oArgParser.add_argument("--vendor", help='set custom vendor')

oArgParser.add_argument("-v", "--verbose", help='increase output verbosity',action="store_true")
oArgParser.add_argument("-m", "--model", help='add model structure',action="store_true")
oArgParser.add_argument("-c", "--controller", help='add controller structure',action="store_true")
oArgParser.add_argument("-p", "--partial", help='add partial structure',action="store_true")
oArgParser.add_argument("-r", "--route", help='add route action structure',action="store_true")
oArgParser.add_argument("-R", "--replace", help='replace destination',action="store_true")
args = oArgParser.parse_args()

sModuleVersion = args.version
sSkeletonName = args.parent
sSkeletonVersion = args.version
sModuleName = args.submodule
sModulePath = os.path.abspath(args.path)
sScriptPath = os.path.realpath(__file__)
sModuleToUpgrade = args.upgrade


DEBUG = True if args.verbose else False

def parseModulePhp(path,names,controllers,hook=False,include=False):
  sCodeHooks = "CoreEntityController::addHook"
  sCodeUse = "use "
  bParseController = False
  sTempController = ""
  bParseFactories = False


  #parse 'factories'
  sFactories = "'factories'"
  sFactoriesEnd = "],"
  sControllerEnd = "},"

  # save all hooks and includes in Module.php to replace these later
  try:
    fp = open(path, "r")
    for line in fp:
      # looking for hooks
      if line.find(sCodeHooks) >= 0 and hook:
        aHooks.append(line)
      # looking for use
      if line.find(sCodeUse) >= 0 and include:
        aIncludes.append(line)

      if line.find(sFactories) >= 0:
        bParseFactories = True
      if bParseFactories and line.find(sFactoriesEnd) >= 0:
        bParseFactories = False
      if not bParseFactories:
        continue

      # parse and save Controllers
      if bParseController:
        sTempController = sTempController + line
        if line.find(sControllerEnd) >= 0:
          bParseController=False
          controllers.append(sTempController)
          sTempController=""

      # detect Start Controller
      sController = re.search(r'(Controller\\).+(class)', line)
      if sController:
        names.append(sController.group(0))
        bParseController = True
        sTempController = line

  except IOError:
    print("Upgrade failed, no oneplace module detected at: " + path + " \n")
    exit(2)

def parseModuleConfig(path,names,route):
  bParseRoutes = False
  sTempRouter = ""
  bParseRoute = False
  sRoute = "'routes'"
  sRoutesEnd = "        ],"
  sRouteEnd = "            ],"
  sRouteStart = "["

  try:
    fp = open(path, "r")
    for line in fp:
      #parse 'factories'

      if line.find(sRoute) >= 0:
        bParseRoutes = True
        continue
      if bParseRoutes and line.find(sRoutesEnd) == 0:
        bParseRoutes = False
      if not bParseRoutes:
        continue
      #print(line)
      # detect Start Route
      if not bParseRoute:
        sRouteName = re.search(r"'(.)+'", line)
        if sRouteName:
          names.append(sRouteName.group(0))
          bParseRoute = True
          sTempRouter = line
      else:
        sTempRouter = sTempRouter + line
      if bParseRoute and line.find(sRouteEnd) == 0:
        bParseRoute = False
        route.append(sTempRouter)

  except IOError as e:
    print("Upgrade failed, no oneplace module detected at: " + path + " \n" + str(e))
    exit(2)


# init class for handling renaming variants
oSkeleton = Skeleton(sSkeletonName)
oModule = Skeleton(sModuleName)
oSkeleton.setVendor(sDefaultVendor + "\\","$vendor$")
if args.vendor:
  print(args.vendor)
  oModule.setVendor(args.vendor + "\\",args.vendor.lower())
else:
  print(sDefaultVendor)
  oModule.setVendor(sDefaultVendor + "\\",sDefaultVendor.lower())

oSkeleton.set(oModule)

print(oSkeleton.get())
print(sDefaultVendor)
exit(0)


'''
 Upgrade a existing plugin
'''
if sModuleToUpgrade:

  parseModulePhp("../src/Module.php.no_controller",aSkeletonControllerNames,aSkeletonControllers)
  parseModulePhp(sModuleToUpgrade + "/src/Module.php",aModuleControllerNames,aModuleControllers,True,True)

  # remove known Controllers from List
  for name in aSkeletonControllerNames:
    if name.find(oSkeleton.getModelName(True)) >=0:
      index=aSkeletonControllerNames.index(name)
      aSkeletonControllerNames.pop(index)
      aSkeletonControllers.pop(index)

  for sSCtl in aSkeletonControllerNames:
    for sMCtl in aModuleControllerNames:
      if sMCtl.find(sSCtl) >= 0:
        index=aModuleControllerNames.index(sMCtl)
        aModuleControllerNames.pop(index)
        aModuleControllers.pop(index)

        index=aSkeletonControllerNames.index(sSCtl)
        aSkeletonControllerNames.pop(index)
        aSkeletonControllers.pop(index)

  # aModuleControllers -> Controllers to add after rebase
  print(str(len(aModuleControllers)) +" new Controllers to add")
  for name in aModuleControllerNames:
    print (name)



  parseModuleConfig("../config/module.config.php.no_route",aSkeletonRouteNames,aSkeletonRoutes)
  parseModuleConfig(sModuleToUpgrade+"/config/module.config.php",aModuleRouteNames,aModuleRoutes)
  # remove known Routes from List
  for name in aSkeletonRouteNames:
    if name.find(oSkeleton.getName(False)) >=0:
      index=aSkeletonRouteNames.index(name)
      aSkeletonRouteNames.pop(index)
      aSkeletonRoutes.pop(index)

  for sSCtl in aSkeletonRouteNames:
    for sMCtl in aModuleRouteNames:
      if sMCtl.find(sSCtl) >= 0:
        index=aModuleRouteNames.index(sMCtl)
        aModuleRouteNames.pop(index)
        aModuleRoutes.pop(index)

        index=aSkeletonRouteNames.index(sSCtl)
        aSkeletonRouteNames.pop(index)
        aSkeletonRoutes.pop(index)


  # aModuleRoutes -> Routes to add after rebase
  print(str(len(aModuleRoutes)) +" new Routes to add\n")

  #detect partials
  if os.path.exists(sModuleToUpgrade+"/view/partial") == True:
    args.partial = True
  else:
    args.partial = False

  #detect partials
  if os.path.exists(sModuleToUpgrade+"/src/Model/") == True:
    args.model = True
  else:
    args.model = False

  #manage Controller.php
  args.controller=False
  args.route=False

  aWhiteList.append("/data/")




if not args.model:
  aToDelDirs.append("/src/Model")

if not args.controller:
  aToDelFiles.append("/src/Controller/"+oSkeleton.getModelName(True)+"Controller.php")

if not args.partial:
  aToDelDirs.append("/view/partial")


# check if path is occupied
if os.path.exists(sys.argv[1]):
  if args.replace:
    shutil.rmtree(sModulePath, ignore_errors=False, onerror=remove_readonly)
  else:
    print("Module already exists... \nmove ,delete or rename your Module at " + sModulePath + '\n')
    exit(1)

#check if context is correct
try:
  f = open("../src/Module.php", "r")
  for line in f:
    if line.find("VERSION") >= 0:
      sSkeletonVersion = re.search(r'(?<=VERSION )*[\d.]+', line).group(0)
      #print("Skeleton Version is " + sSkeletonVersion)
except IOError:
  print("Error wrong context, run it in /data/" + sModulePath + "\n")
  oArgParser.print_help()
  exit(2)


# copy skeleton file tree
print("Creating oneplace module at " + sModulePath + "\n")
try:
  shutil.copytree("../", sModulePath)
except IOError as err:
  print("Cant create module "+ "\n" + format(err))


# Remove folders
iChangeCount=0
for dir in aToDelDirs:
  try:
    if os.path.exists(sModulePath+dir) == True:
      v_print(" - delete " + sModulePath+dir)
      shutil.rmtree(sModulePath+dir, ignore_errors=False, onerror=remove_readonly)
      iChangeCount += 1
  except IOError as err:
    print("Error while deleting file : ", sModulePath+dir + " - " + format(err))
    exit(2)
print("Total: " + str(iChangeCount) + " folders deleted")

# delete files
iChangeCount=0
for fileList in aToDelFiles:
  for filePath in glob.glob(sModulePath+fileList):
    try:
      v_print(" - delete " + filePath)
      iChangeCount += 1
      if os.path.exists(filePath) == True:
        os.remove(filePath)
    except:
      print("Error while deleting file : ", filePath)
      exit(2)
print("Total: " + str(iChangeCount) + " files deleted")

# this while loop is only for folder recursive renaming issue
bFinish = False
while not bFinish:
  bFinish = True
  # rename all folders
  for root, dirs, files in os.walk(sModulePath):
    path = root.split(os.sep)
    for dir in dirs:
      sSource = dir
      for result in oSkeleton.getview():
        if result[0] in dir and result[0] != result[1]:
          # rename all Folders from skeleton to moduleName
          sDest = dir.replace(result[0],result[1])
          v_print(" - rename folder  " + os.path.join(root,sSource) + " to " + os.path.join(root,sDest))
          os.rename(os.path.join(root,sSource), os.path.join(root,sDest))
          iChangeCount += 1
          bFinish = False # dirty solution
          break

print("Total: " + str(iChangeCount) + " folders renamed")
iChangeCount=0

iChangeCount=0
#rename all files
ignore=False
for root, dirs, files in os.walk(sModulePath):
  # rename all Files from Skeleton to ModuleName
  for file in files:
    sSource = file
    # ignore whitelisted files
    for url in aWhiteList:
      path = os.path.join(root,sSource)
      if path.find(url) >= 0:
        v_print(" - ignore " + path)
        ignore = True

    if ignore:
      ignore=False
      continue

    for result in oSkeleton.get():
      if result[0] in file:
        sDest = file.replace(result[0], result[1])
        v_print(" - rename  " + os.path.join(root,sSource) + " to " + os.path.join(root,sDest))
        os.rename(os.path.join(root,sSource), os.path.join(root,sDest))
        iChangeCount += 1
        break

print("Total: " + str(iChangeCount) + " files renamed")


# delete copy files before renaming
if sModuleToUpgrade:
  try:
    shutil.rmtree(sModulePath+"/view/partial", ignore_errors=False, onerror=remove_readonly)
    shutil.copytree(sModuleToUpgrade+"/view/partial", sModulePath+"/view/partial")
  except IOError as err:
    v_print("Cant copy; "+ format(err))

  try:
    shutil.copyfile(sModuleToUpgrade+"/"+sComposerJson,sModulePath+"/"+sComposerJson)
    shutil.copyfile(sModuleToUpgrade+"/README.md",sModulePath+"/README.md")
  except IOError as err:
    print("Cant copy; "+ format(err))

if args.route:
  os.remove(sModulePath+"/config/module.config.php.no_route")
else:
  os.remove(sModulePath+"/config/module.config.php")
  os.rename(sModulePath+"/config/module.config.php.no_route",sModulePath+"/config/module.config.php")
  view = "/view/one-place/" + oModule.getBaseName(False) + "/" + oModule.getModelName(False) + "/" + oModule.getModelName(False)
  shutil.rmtree(sModulePath+view, ignore_errors=False, onerror=remove_readonly)

if args.controller:
  os.remove(sModulePath+"/src/Module.php.no_controller")
else:
  os.remove(sModulePath+"/src/Module.php")
  os.rename(sModulePath+"/src/Module.php.no_controller",sModulePath+"/src/Module.php")


# all renaming inside files happens here:
iChangeCount=0
for root, dirs, files in os.walk(sModulePath):
  # rename all Files from Skeleton to ModuleName
  for file in files:
    sSource = os.path.join(root,file)
    sSourceTemp = os.path.join(root,file + "_temp")

    # ignore whitelisted files
    for url in aWhiteList:
      if sSource.find(url) >= 0:
        ignore = True

    if ignore:
      ignore = False
      continue

    fp = open(sSource,"r")
    fpW = open(sSourceTemp,"w")

    # search an replace inside each file
    # look for versions and set it to 1.0.0
    line_count = 0
    sVersionTag ="@version"
    sSinceTag ="@since"
    sComposerVersion ='"version"'
    sSkeletonIdfs = "skeleton_idfs"
    sSkeletonForm = "skeleton-single"
    sSkeletonSkeletonForm = "skeletonskeleton-single"
    sSkeletonFormLabel = "Skeleton Skeleton"

    sCodeModelStart = "getServiceConfig"
    sCodeControllerStart = "getControllerConfig"
    sCodeRoutesStart = "Routes"
    sCodeInsertHooks = "Plugin Hook"
    sRouteStart = "'routes'"
    sFactoriesStart = "'factories'"
    sCodeUse = "use "
    bCodeDelMode = False
    bGetControllerConfig=False


    try:
      for line in fp:
        line_count=line_count+1

        if sModuleToUpgrade:
          # module.config.php insert routes
          if sSource.find(sModuleConfig) >= 0 and line.find(sRouteStart) >= 0:
            fpW.write(line)
            for route in aModuleRoutes:
              fpW.write(route)
            line=""

          if sSource.find(sModulePhp) >= 0 and line.find("getControllerConfig") >= 0:
            bGetControllerConfig=True
          # Module.php insert controllers
          if bGetControllerConfig:
            if sSource.find(sModulePhp) >= 0 and line.find(sFactoriesStart) >= 0:
              fpW.write(line)
              for ctrl in aModuleControllers:
                fpW.write(ctrl)
              line=""


          # insert Custom Hooks
          if sSource.find(sModulePhp) >= 0 and line.find(sCodeInsertHooks) >= 0:
            fpW.write(line)
            for hook in aHooks:
              fpW.write(hook)
            line=""

          # replace aIncludes with original
          if sSource.find(sModulePhp) >= 0 and line.find(sCodeUse) >= 0:
            if len(aIncludes) > 0 :
              for include in aIncludes:
                fpW.write(include)
              aIncludes=[]
              line=""
            else:
              continue

        # Model Handling
        if not args.model:
          if sSource.find(sModulePhp) >= 0 and line.find(sCodeModelStart) >= 0:
            v_print(" - del " + sCodeModelStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""


        # Controller Handling
        if not args.controller and not sModuleToUpgrade: #deactivated
          if sSource.find(sModulePhp) >= 0 and line.find(sCodeControllerStart) >= 0:
            v_print(" - del " + sCodeControllerStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""
          if sSource.find(sModuleConfig) >= 0 and line.find(sCodeRoutesStart) >= 0:
            v_print(" - del " + sCodeRoutesStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""

        if bCodeDelMode:
          line = ""

        # not a beauty - but works
        if sSource.find(sModulePhp) >= 0 and line.find("VERSION") >= 0:
          v_print(" - set " + "VERSION" + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
          line="    const VERSION = '" + sModuleVersion + "';\n"

        # set all versions tags to current verion
        #elif sSource.find(sModulePhp) >= 0 and line.find(sVersionTag) >= 0:
        #  v_print(" - set " + sVersionTag + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
        #  line = line[:line.find(sVersionTag) + len(sVersionTag)] + " " + sModuleVersion + "\n"
        #  line = line[:line.find(sVersionTag) + len(sVersionTag)] + " " + sModuleVersion + "\n"

        # correct all since tags
        elif line.find(sSinceTag) >= 0:
          sSinceVersion = re.search(r'[\d.]+', line).group(0)
          if pkg_resources.parse_version(sSinceVersion) > pkg_resources.parse_version(sModuleVersion) :
            v_print(" - set " + sSinceTag + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
            line = line[:line.find(sSinceTag) + len(sSinceTag)] + " " + sModuleVersion + "\n"

        #corret composer config file version
        elif sSource.find(sComposerJson) >= 0 and line.find(sComposerVersion) >= 0:
          v_print(" - set " + sComposerVersion + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
          line ="  " + sComposerVersion + ': "' + sModuleVersion + '",\n'

        # install.sql custom keys
        if sSource.find(sInstallSql) >= 0 and line.find(sSkeletonSkeletonForm) >= 0:
          v_print(" - renaming " + sSource + " at Line: " + str(line_count))
          line = line.replace(sSkeletonSkeletonForm, oModule.getFormName(False)+"-single")
        if sSource.find(sInstallSql) >= 0 and line.find(sSkeletonForm) >= 0:
          v_print(" - renaming " + sSource + " at Line: " + str(line_count))
          line = line.replace(sSkeletonForm, oModule.getBaseName(False)+"-single")
        if sSource.find(sInstallSql) >= 0 and line.find(sSkeletonIdfs) >= 0:
          v_print(" - renaming " + sSource + " at Line: " + str(line_count))
          line = line.replace(sSkeletonIdfs, oModule.getBaseName(False)+"_idfs")
        if sSource.find(sInstallSql) >= 0 and line.find(sSkeletonFormLabel) >= 0:
          v_print(" - renaming " + sSource + " at Line: " + str(line_count))
          line = line.replace(sSkeletonFormLabel, oModule.getLabel(True))

        # replace skeleton name
        sOrig=line

        for result in oSkeleton.get():
          #print(result)
          line = line.replace(result[0], result[1])
        if sOrig != line :
          #print(sOrig + " ! " + line)
          v_print(" - renaming " + sSource + " at Line: " + str(line_count))
          iChangeCount += 1
        fpW.write(line)
    except Exception as e:
      print(sModulePath + " Error while renaming file : " + dir + " " + str(e))
      exit(2)


    fp.close()
    os.remove(sSource)
    fpW.close()
    os.rename(sSourceTemp, sSource)


if sModuleToUpgrade:
  # copy skeleton file tree
  print("Copy Controller form Source Module " + sModulePath + "\n")
  try:
    for file in glob.glob(sModuleToUpgrade + "/src/Controller/*.php"):
      #f = open(sModulePath + "/src/Controller/"+ os.path.basename(file))
      if not os.path.exists(sModulePath + "/src/Controller/"+os.path.basename(file)):
        v_print("Copy " + file + " to " + sModulePath + "/src/Controller/"+ os.path.basename(file))
        shutil.copyfile(file,sModulePath + "/src/Controller/"+os.path.basename(file))

  except IOError:
    print("IOError: " + file)


  try:
    view = "/view/one-place/" + oModule.getBaseName(False) + "/" + oModule.getModelName(False) + "/" + oModule.getModelName(False)
    if os.path.exists(sModuleToUpgrade+view):
      v_print("form " + sModuleToUpgrade+view + " to " +  sModulePath + view )
      shutil.copytree(sModuleToUpgrade+view, sModulePath + view )
  except IOError as err:
    v_print("Cant copy views: "+  format(err))

  try:
    shutil.copytree(sModuleToUpgrade+"/.git", sModulePath+"/.git")
  except IOError as err:
    v_print("Cant copy git: "+  format(err))

  try:
    shutil.rmtree(sModulePath+"/data/", ignore_errors=False, onerror=remove_readonly)
    shutil.copytree(sModuleToUpgrade+"/data/", sModulePath+"/data")
  except IOError as err:
    v_print("Cant copy data : "+  format(err))

  try:
    shutil.copytree(sModuleToUpgrade+"/docs/", sModulePath+"/docs")
  except IOError as err:
    v_print("Cant copy docs: "+  format(err))

print("Total: " + str(iChangeCount) + " changes inside files")
iChangeCount=0

print("\n\nModule: <"+ sModuleName +"> successfully created at: " + sModulePath)
