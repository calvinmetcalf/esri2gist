import arcpy
from tempfile import mkdtemp
from os import remove, rmdir
from urllib2 import Request, urlopen

design = """
{
   "_id":"_design/geojson",
   "spatial": {
       "geometry": "function(doc){\n       if(doc.geometry){ emit(doc.geometry,doc)};\n            }"
   },
   "rewrites": [
       {
           "to": "/_spatial/_list/geojson/geometry",
           "from": "/all",
           "query": {
               "bbox": "-180,-90,180,90"
           }
       }
   ],
   "lists": {
       "geojson": "function(head, req) {\n    var row, out, sep = '\\n';\n    if (req.headers.Accept.indexOf('application/json')!=-1) {\n        start({\"headers\":{\"Content-Type\" : \"application/json\"}});\n    }    else {\n        start({\"headers\":{\"Content-Type\" : \"text/plain\"}});\n    }\n    if ('callback' in req.query) {\n        send(req.query['callback'] + \"(\");\n    }    send('{\"type\": \"FeatureCollection\", \"features\":[');\n    while (row = getRow()) {\n        out = {type: \"Feature\", geometry: row.value.geometry};\n\t\t\t\tdelete row.value.geometry;\n               out.properties= row.value\n        send(sep + JSON.stringify(out));        sep = ',\\n';\n    }\n    send(\"]}\");\n    if ('callback' in req.query) {\n        send(\")\");}};\n"
   }
}"""

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
    req2 = Request(url)
    req2.add_header('Content-Type', 'application/json')
    arcpy.AddMessage(str(urlopen(req2,design).code))

doStuff(arcpy.GetParameterAsText(0),arcpy.GetParameterAsText(1),arcpy.GetParameterAsText(2))
