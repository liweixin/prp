#coding=utf-8
import time
import traceback
import sys
import web
import hashlib
import os
import json
import config
import dbOperations

#initDatabase()支持中文

#Configurations for session
#Non debug mode
#Sessions doesn't work in debug mode because it interfere with reloading
#See session_with_reloader for more details
web.config.debug = False
web.config.session_parameters['cookie_name'] = 'user_session_id'
web.config.session_parameters['cookie_domain'] = None
#24 * 60 * 60, # 24 hours   in seconds
web.config.session_parameters['timeout'] = 86400,
web.config.session_parameters['ignore_expiry'] = True
web.config.session_parameters['ignore_change_ip'] = True
#Randomly generate strings with fixed length as secret key
web.config.session_parameters['secret_key'] = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
web.config.session_parameters['expired_message'] = 'Warning: Session Expired'

# Define urls and the corresponding handlers 
urls = (
    '/apFeatures', 'SendApFeatures',
    '/wifiInfos', 'GetWifiInfos',
    '/wifiLatLng', 'GetWifiLatLng',
    '/mapDisplay', 'ShowMap',
    '/apFeaturesList', 'ApFeaturesList',
    '/home', 'Home',
    '/', 'Blank',
)

app = web.application(urls,globals())
t_globals = {
    'datestr': web.datestr,
    'cookie' : web.cookies,
}

render = web.template.render(config.templatesPath)
db = web.database(dbn=config.dbn, db=config.db, user=config.dbuser, pw=config.dbpw)
store = web.session.DBStore(db, 'Sessions')
session = web.session.Session(app, store,initializer={'logged_in': False, 'username': ""})

def getTimeString():
    timeStamp = int(time.time())
    timeArray = time.localtime(timeStamp)
    timeString = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return timeString

def getAllAPsFeatures():
    results = dbOperations.selectAPFeatures()
    apsfeatures = []
    for result in results:
        apsfeatures.append({"bssid":result["bssid"],
                            "ssid":result["ssid"],
                            "security":result["security"],
                            "signal":result["signals"],
                            "latitude":result["latitude"],
                            "longtitude":result["longtitude"],
                            "macAdress":result["macAdress"],
                            "timeString":result["timeString"]} )
    return json.dumps(apsfeatures)

class Home:
    def GET(self):
        return render.home()

class Blank:
    def GET(self):
        raise web.seeother('/home')

class ApFeaturesList:
    def GET(self):
        return render.apFeaturesList(getAllAPsFeatures())

class ShowMap:
    def GET(self):
        results = db.select('APsFeatures', what="longtitude, latitude", order="longtitude DESC")
        location = []
        for result in results:
            location.append({"longtitude":result["longtitude"], "latitude":result["latitude"]})
        return render.mapDisplay(json.dumps(location))
                            
class GetWifiLatLng:
    def GET(self):
        results = db.select('APsFeatures', what="longtitude, latitude", order="longtitude DESC")
        total = 0
        location=[]
        for result in results:
            if(total==0):
                data={}
                data["longtitude"]=result["longtitude"]
                data["latitude"]=result["latitude"]
                location.append(data)
                total=total+1
            else:
                if(result!=preResult):
                    data={}
                    data["longtitude"]=result["longtitude"]
                    data["latitude"]=result["latitude"]
                    location.append(data)
                    total=total+1
            preResult = result
        data={}
        data["count"]=total
        data["location"]=location
        return json.dumps(data)
        
class GetWifiInfos:
    def GET(self):
        st = web.ctx.query
        lat = 0
        lng = 0
        if((st.find("?Latitude=")==0)&(st.find("&Longtitude=")>=0)):
            pos = st.find("&Longtitude=")
            lat = float(st[10:pos])
            lng = float(st[pos+12:])
        latlngDict = {'latitude':lat, 'longtitude':lng}
        results = db.select('APsFeatures', what="signals, security, ssid, bssid, timeString",
                            where="(latitude=$latlngDict['latitude'])and(longtitude=$latlngDict['longtitude'])",
                            vars=locals())
        list=[]
        for result in results:
            data={}
            data["bssid"]=result["bssid"]
            data["ssid"]=result["ssid"]
            data["security"]=result["security"]
            data["signals"]=result["signals"]
            data["timeString"]=result["timeString"]
            list.append(data)
        data={}
        data["count"]=len(results)
        data["wifiInfos"]=list
        return json.dumps(data)

class Fail:
    def GET(self, operation):
        return render.fail(operation)

class Success:
    def GET(self, operation):
        return render.success(operation)
        
class SendApFeatures:
    features_form = web.form.Form(
        web.form.Textbox('BSSID',web.form.notnull,size=17),
        web.form.Textbox('SSID',web.form.notnull,size=30),
        web.form.Textbox('Security',web.form.notnull,size=50),
        web.form.Textbox('Signal',web.form.notnull,size=3),
        web.form.Textbox('Longtitude',web.form.notnull,size=12),
        web.form.Textbox('Latitude',web.form.notnull,size=12),
        web.form.Textbox('MacAdress',web.form.notnull,size=17),
        web.form.Button('Submit'),
    )    
    def GET(self):
        #if session.logged_in == True:
        #    return 
        form = self.features_form()
        return render.apFeatures(form)
    
    def POST(self):
        i = web.input()
        macAdress = web.net.websafe(i.MacAdress)
        bssid = web.net.websafe(i.BSSID)
        ssid = web.net.websafe(i.SSID)
        security = web.net.websafe(i.Security)
        signal = web.net.websafe(i.Signal)
        latitude = web.net.websafe(i.Latitude)
        longtitude = web.net.websafe(i.Longtitude)
        timeString = getTimeString()
        featuresDict = {'BSSID':bssid, 'SSID':ssid, 'SECURITY':security, 'SIGNALS':signal,
                        'LONGTITUDE':longtitude, 'LATITUDE':latitude, 'TIMESTRING':timeString, 'MACADRESS':macAdress}    
        if not verifyFeatures(featuresDict):
            result = {
                "code":1,
                "info":"Update Success."
                }
            return result
            #raise web.seeother('/fail/sendAPFeatures')
        else:
            '''
            db.insert('APsFeatures',
                      bssid=bssid,
                      ssid=ssid,
                      security=security,
                      signals=signal,
                      latitude=latitude,
                      longtitude=longtitude,
                      macAdress=macAdress,
                      timeString=timeString )
                      '''
            dbOperations.insertAPFeatures(bssid, ssid, security, signal, latitude, longtitude, macAdress, timeString)
            result = {
                "code":1,
                "info":"Upload success."
                }
            print 'Success'
            return result
            raise web.seeother('/success/sendAPFeatures')

def verifyFeatures(featuresDict):
    t=db.select('APsFeatures', where="bssid=$featuresDict['BSSID']",vars=locals())
    for temp in t:
        dbOperations.updateAPFeatures(featuresDict)
        print 'Update Success.'
        return False      
    return True


def notfound():
    return web.notfound("Sorry, the page your were looking for was not found.")
    
app.notfound = notfound

# running our server
if __name__ == '__main__':
    app.run()

