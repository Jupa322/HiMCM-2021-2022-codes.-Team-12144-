import json
import urllib.request
import ssl
import pandas as pd
ssl._create_default_https_context = ssl._create_unverified_context

griddata = []
posdata = []
elevdata = []

def elevation(lat, lng):
    apikey = "AIzaSyChte0nrvyPeKRRTvfW1ORoAk48pBw7QSU"
    url = "https://maps.googleapis.com/maps/api/elevation/json"
    request = urllib.request.urlopen(url+"?locations="+str(lat)+","+str(lng)+"&key="+apikey)
    try:
        results = json.load(request).get('results')
        if 0 < len(results):
            elevation = results[0].get('elevation')
            # ELEVATION
            return elevation
        else:
            print('HTTP GET Request failed.')
    except ValueError:
        print('JSON decode failed: '+str(request))

def getdata(latmin,latmax,lngmin,lngmax,stepinterval):
    stepinterval = stepinterval/111319.9
    rows = int((latmax - latmin)//stepinterval)
    columns = int((lngmax - lngmin)//stepinterval)
    for i in range(0,rows):
        for j in range(0,columns):
            elevdata.append(elevation(latmin + i * stepinterval, lngmin + j * stepinterval))
            griddata.append([i,j])
            posdata.append([latmin+i * stepinterval,lngmin+j * stepinterval])

    return exporttoexcel(griddata,posdata,elevdata)

def exporttoexcel(griddata,posdata,elevdata):
    dict = {'gridindex': griddata, 'position': posdata, 'elevation': elevdata}
    result = pd.DataFrame(dict)
    result.to_csv('waterelevfinal10.csv')

getdata(36.062222,36.095833,-114.466667,-114.433611,200)

