'''
2013-09-05
Eric R. Evarts
MeasureUtils.py is a set of utilities used in the measurement program all clumped together for ease of use
'''

if __name__ == '__main__':
    print(''' This set of utilities will allow ease of use for common helper functions in the various other files of the program.
    ''')

def lineNo():
    import inspect
    return 'Line '+str(inspect.currentframe().f_back.f_lineno)

def parseKeyValue(line):
    # a funciton that will take a line and split it along the equals sign and make a tuple
    splitLine = line.split('=')
    if len(splitLine) != 2:
        return None,None #if the length is not 2, this line may be blank, or not have a key value or have extra junk that should be done differently
    return (splitLine[0].strip(), splitLine[1].strip())

def fullSleep(n):
    from time import time,sleep
    #print 'start fullSleep'
    start = time()
    newTime = time()
    while ((newTime - start) < (n-1e-6)):
        #print('Still in fullSleep',time(),'start =',start,'n=',n,'time - start',time()-start)
        sleep(n - (newTime - start))
        newTime = time()
    #print('End of FullSleep',time()-start,'n=',n)
    return 0

def getDirDict(foldername):
    # return a dict of form filename:fullPathToFilename
    import os
    import os.path
    fileDict = {}
    if os.path.isdir(foldername):
        fileList = os.listdir(foldername)
        for filename in fileList:
            fullfile = os.path.join(foldername,filename)
            if os.path.isfile(fullfile):
                fileDict[filename] = fullfile
    return fileDict

def getSIvalue(edit_box,unit_combo):
    import GetAndSet.Units
    val = float(str(edit_box.text()))
    currUnit = str(unit_combo.currentText())
    if currUnit == '':
        # not a good time to do this math
        raise ValueError
    for key,unitSet in GetAndSet.Units.units.items():
        # check each unit set for the current combo unit
        rejectUnit = False
        for unit in list(unitSet.keys()):
            if unit_combo.findText(unit) == -1:
                # unit not found
                rejectUnit = True
                break
        if rejectUnit:
            continue
        if currUnit in unitSet:
            #print 'found unit string'
            unitDict = GetAndSet.Units.units[key]
            break
    #print 'Val = ',val,'Unit conv = ',unitDict[currUnit]
    return val*unitDict[currUnit]

def getUnitDict(knownUnitStr):
    import GetAndSet.Units
    possibleSets = {}
    for key,unitSet in GetAndSet.Units.units.items():
        # walk through all known sets of units
        # for each, check if known unit is in the set
        if knownUnitStr in unitSet:
            possibleSets[key] = unitSet
    if len(possibleSets)==1:
        return list(possibleSets.values())[0]
    elif len(possibleSets)<1:
        return None
    else:
        # ask the user what to use when more than 1 option available.
        # follow method of Preset to have a list with single select
        # this will only run from within a GUI, requires a running PyQT app
        import Preset.preset_dialog_main
        preset_dialog = Preset.preset_dialog_main.PresetDialog(list(possibleSets.keys()))
        preset_dialog.ui.label.setText('Select the desired unit set to use for {}'.format(knownUnitStr))
        preset_dialog.exec_()
        choice = preset_dialog.getChoice()
        return possibleSets[choice[0]]

def addSortedItems(comboBox,itemsToAdd, key = str.lower):
    comboBox.addItems(sorted(itemsToAdd,key=key))

def resetLastValue(comboBox,lastValueText, defaultInd = 0,blockSignals = False):
    # try to find last value, if yes, set it, else don't do anything
    if blockSignals:
        comboBox.blockSignals(True)
    if comboBox.findText(lastValueText)>-1:
        # if value not found, returns -1, use default below
        comboBox.setCurrentIndex(comboBox.findText(lastValueText))
    elif comboBox.count() > defaultInd:
        comboBox.setCurrentIndex(defaultInd)
    if blockSignals:
        comboBox.blockSignals(False)

def set_units(comboBox,unitDict,defaultUnit):
    # try to set the comboBox appropriately to keep the current unit if possible, else use defaultUnit
    currUnit = str(comboBox.currentText())
    #print defaultUnit,currUnit,comboBox.currentIndex()
    import operator #this changes the dict ot a sorted list of tuples, so we can have them ordered. 
    try:
        sortedUnitDict = sorted(iter(unitDict.items()), key = operator.itemgetter(1))
        units = [tup[0] for tup in sortedUnitDict]
    except TypeError:
        # I have a unit set that doesn't sort nicely, just go alphabetical
        units = sorted(unitDict.keys(), key = str.lower)
    # clear and repopulate
    comboBox.clear()
    comboBox.addItems(units)
    if comboBox.findText(currUnit)>-1:
        # if unit not found, returns -1, use default below
        comboBox.setCurrentIndex(comboBox.findText(currUnit))
    else:
        comboBox.setCurrentIndex(comboBox.findText(defaultUnit))
        

def strToBool(truthString):
    # allow a variety of options for true or false
    if truthString.lower() in ['true','t','y','yes']:
        return True
    elif truthString.lower() in ['false','f','n','no']:
        return False
    else:
        raise ValueError

def getClasstoModuleNameDict(basePackage):
    # return the dictionary with keys of classname value of full module name
    import pkgutil
    import inspect
    import os.path
    pkgpath = os.path.dirname(basePackage.__file__)
    # get a list of the module names in the package
    modlist = [name for _,name,_ in pkgutil.iter_modules([pkgpath])]
    # load each one
    import importlib
    for name in modlist:
        importlib.import_module(basePackage.__name__+'.'+name) 
    # then continue with the inspection
    classDict = {}
    for modname,mod in inspect.getmembers(basePackage, inspect.ismodule):
        # get the class list
        names = [name for name,obj in inspect.getmembers(mod,inspect.isclass)]
        # add to the dict
        currDict = {name:mod.__name__ for name in names}
        classDict.update(currDict)
    return classDict

def getModuleNameforClass(basePackage,className):
    # get the module name from a package and classname
    classDict = getClasstoModuleNameDict(basePackage)
    return classDict[className]

def getPackageDict(basePackage):
    # generate a dictionary of all the modules in this package, values are a list of the classes in the Module
    # inspect only works for live objects, use pkgutil.iter_modules for thorough walkthrough
    import pkgutil
    import inspect
    import os.path
    pkgpath = os.path.dirname(basePackage.__file__)
    # get a list of the module names in the package
    modlist = [name for _,name,_ in pkgutil.iter_modules([pkgpath])]
    # load each one
    import importlib
    for name in modlist:
        importlib.import_module(basePackage.__name__+'.'+name) 
    # then continue with the inspection
    packageDict = {}
    for modname, mod in inspect.getmembers(basePackage, inspect.ismodule):
        # get the class list
        names = [name for name,obj in inspect.getmembers(mod,inspect.isclass)]
        # add to the dict
        packageDict[modname] = names
    return packageDict

def paramToString(rootParameter, ignoreList = []):
    outputList = []
    from Instruments import LabInstruments
    from GetAndSet import getAndSetBase
    # I need to start at rootParameter and print param/value pairs to string
    # however, I need to deal with parameters with children
    # probably convert children to dicts? include type, name, value? list of dicts?
    for param in rootParameter.children():
        paramName = param.name()
        if paramName in ignoreList:
            continue
        currentString = '%s = '%paramName
        # now identify the value, which could be stored in children
        val = param.value()
        if param.hasChildren():
            # This param has children, generate a list of dicts from the children
            # consider just using the saveState() function to generate a string and later
            # use restoreState on that string?
            childList = []
            for child in param.children():
                childDict = child.opts
                childList.append(childDict)
            currentString += str(childList)
        elif type(val)==int:
            currentString += '%d'%val
        elif type(val) == float:
            currentString += '%e'%val
        elif isinstance(val,LabInstruments.LabInstrument) or isinstance(val,getAndSetBase.getAndSet):
            # this is probably for an instrument reference?
            currentString += '%s'%val.getName()
        else:
            currentString += str(val)
        outputList.append(currentString)
    return '\n'.join(outputList)+'\n'

def qtRunning():
    '''
    find out if Qt is running
    '''
    # Test if QtCore.QCoreApplication.instance() is not None
    qAppRunning = False
    try:
        from PyQt4 import QtCore,QtGui
        if QtCore.QCoreApplication.instance()!=None:
            qAppRunning = True
    except ImportError:
        print("Notice: Error import QtCore")
        qAppRunning = False
    return qAppRunning
