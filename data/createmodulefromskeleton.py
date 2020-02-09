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
 @version 1.0.0
 @since 1.0.0
"""



# Remove Files and Folders (wildcard only for files)
aToDelFiles = []
aToDelFiles.append("/data/*.sh")
aToDelFiles.append("/data/*.ps1")
aToDelFiles.append("/data/*.py")
aToDelFiles.append("/view/layout/*default.phtml")
aToDelFiles.append("/CHANGELOG.md")
aToDelFiles.append("/mkdocs.yml")

aToDelDirs = []
aToDelDirs.append("/.git")
aToDelDirs.append("/.idea")
aToDelDirs.append("/docs/book")

# Whitelist from renaming
aWhiteList = []
aWhiteList.append("/language/")

#default Values
sSkeletonName = "Skeleton-Skeleton"
sSkeletonVersion = "1.0.0"
sModulePhp = "Module.php"
sComposerJson = "composer.json"
sModuleConfig = "module.config.php"

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

oArgParser.add_argument("-v", "--verbose", help='increase output verbosity',action="store_true")
oArgParser.add_argument("-m", "--model", help='add model structure',action="store_true")
oArgParser.add_argument("-c", "--controller", help='add controller structure',action="store_true")
oArgParser.add_argument("-p", "--partial", help='add partial structure',action="store_true")
oArgParser.add_argument("-r", "--replace", help='replace destination',action="store_true")
args = oArgParser.parse_args()

sModuleVersion = args.version
sSkeletonName = args.parent
sSkeletonVersion = args.version
sModuleName = args.submodule
sModulePath = os.path.abspath(args.path)
sScriptPath = os.path.realpath(__file__)

DEBUG = True if args.verbose else False
if not args.model:
  aToDelDirs.append("/src/Model")
if not args.controller:
  aToDelDirs.append("/src/Controller")
if not args.partial:
  aToDelDirs.append("/view/partial")

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

class Skeleton:
  def __init__(self,name):
    self.name = name.split('-')
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
  def get(self):
    return [
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
    [self.getModelName(True),self.module.getModelName(True)],
    [self.getModelName(False),self.module.getModelName(False)],
    [self.getBaseName(True),self.module.getBaseName(True)],
    [self.getBaseName(False),self.module.getBaseName(False)]
    ]


"""
  Do the Main Stuff below
"""
# init class for handling renaming variants
oSkeleton = Skeleton(sSkeletonName)
oModule = Skeleton(sModuleName)
oSkeleton.set(oModule)
print(oSkeleton.get())
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
    if line.find("VERSION") > 0:
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
      for result in oSkeleton.get():
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
      if path.find(url) > 0:
        print(" - ignore " + path)
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


# all renaming inside files happens here:
iChangeCount=0
for root, dirs, files in os.walk(sModulePath):
  # rename all Files from Skeleton to ModuleName
  for file in files:
    sSource = os.path.join(root,file)
    sSourceTemp = os.path.join(root,file + "_temp")

    # ignore whitelisted files
    for url in aWhiteList:
      if sSource.find(url) > 0:
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

    sCodeModelStart = "getServiceConfig"
    sCodeControllerStart = "getControllerConfig"
    sCodeRoutesStart = "Routes"
    bCodeDelMode = False

    try:
      for line in fp:
        line_count=line_count+1

        # Model Handling
        if not args.model:
          if sSource.find(sModulePhp) > 0 and line.find(sCodeModelStart) > 0:
            v_print(" - del " + sCodeModelStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""

        # Controller Handling
        if not args.controller:
          if sSource.find(sModulePhp) > 0 and line.find(sCodeControllerStart) > 0:
            v_print(" - del " + sCodeControllerStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""
          if sSource.find(sModuleConfig) > 0 and line.find(sCodeRoutesStart) > 0:
            v_print(" - del " + sCodeRoutesStart + " in " + sSource + " at Line " + str(line_count))
            bCodeDelMode = False if bCodeDelMode else True
            line = ""

        if bCodeDelMode:
          line = ""

        # not a beauty - but works
        if sSource.find(sModulePhp) > 0 and line.find("VERSION") > 0:
          v_print(" - set " + sVersionTag + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
          line="    const VERSION = '" + sModuleVersion + "';\n"

        # set all versions tags to current verion
        elif sSource.find(sModulePhp) > 0 and line.find(sVersionTag) > 0:
          v_print(" - set " + sVersionTag + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
          line = line[:line.find(sVersionTag) + len(sVersionTag)] + " " + sModuleVersion + "\n"

        # correct all since tags
        elif line.find(sSinceTag) > 0:
          sSinceVersion = re.search(r'[\d.]+', line).group(0)
          if pkg_resources.parse_version(sSinceVersion) > pkg_resources.parse_version(sModuleVersion) :
            v_print(" - set " + sSinceTag + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
            line = line[:line.find(sSinceTag) + len(sSinceTag)] + " " + sModuleVersion + "\n"

        #corret composer config file version
        elif sSource.find(sComposerJson) > 0 and line.find(sComposerVersion) > 0:
          v_print(" - set " + sComposerVersion + " to " + sModuleVersion + " in " + sSource + " at Line " + str(line_count))
          line ="  " + sComposerVersion + ': "' + sModuleVersion + '",\n'



        # replace skeleton name
        sOrig=line
        for result in oSkeleton.get():
          line = line.replace(result[0], result[1])
        if sOrig != line :
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

print("Total: " + str(iChangeCount) + " changes inside files")
iChangeCount=0

print("\n\nModule: <"+ sModuleName +"> successfully created at: " + sModulePath)
