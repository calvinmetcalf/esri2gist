import arcpy
from tempfile import mkdtemp
from os import remove, rmdir
from urllib2 import Request, urlopen

def doStuff(inFile,dbUrl,tbx):
    arcpy.ImportToolbox(tbx)
    base = mkdtemp()
    outFile = base+'//output.json'
    arcpy.esri2open(inFile,outFile)
    postToCouch(dbUrl,outFile)
    cleanUp(base,outFile)

def cleanUp(p,f):
    remove(f)
    rmdir(p)

def postToCouch(url,outFile):
    newUrl = url + '//_bulk_docs'
    baseFile = open(outFile,'r')
    data = baseFile.read()
    baseFile.close()
    req = Request(newUrl)
    req.add_header('Content-Type', 'application/json')
    res = urlopen(req,data)
    arcpy.AddMessage(str(res.code))

doStuff(arcpy.GetParameterAsText(0),arcpy.GetParameterAsText(1),arcpy.GetParameterAsText(2))
