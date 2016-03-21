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
#testssh

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
    '/login', 'Login',
    '/apFeatures', 'SendApFeatures',
    '/wifiInfos', 'GetWifiInfos',
    '/wifiLatLng', 'GetWifiLatLng',
    '/mapDisplay', 'ShowMap',
    '/apFeaturesList', 'ApFeaturesList',
    '/home', 'Home',
    '/', 'Blank',
    '/wifiInfos/del/(.+)', 'DelWifiInfo',
    '/fail/(\w+)','Fail',
    '/success/(\w+)','Success',
    '/logout', 'Logout',
    '/apacessrecord', 'APAcessRecord',
)

app = web.application(urls,globals())
t_globals = {
    'datestr': web.datestr,
    'cookie' : web.cookies,
}

db = web.database(dbn=config.dbn, db=config.db, user=config.dbuser, pw=config.dbpw)
store = web.session.DBStore(db, 'Sessions')
session = web.session.Session(app, store,initializer={'logged_in': False, 'username': ""})
render = web.template.render(config.templatesPath, base='base', globals={'context': session})


class APAcessRecord:
    features_form = web.form.Form(
        web.form.Textbox('bssid',web.form.notnull,size=17),
        web.form.Textbox('startTime',web.form.notnull,size=30),
        web.form.Textbox('endTime',web.form.notnull,size=50),
        web.form.Textbox('longtitude',web.form.notnull,size=12),
        web.form.Textbox('latitude',web.form.notnull,size=12),
        web.form.Textbox('macAdress',web.form.notnull,size=17),
        web.form.Button('Submit'),
    )    
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/login')
        form = self.features_form()
        return render.apAcessRecord(form)
    
    def POST(self):
        i = web.input()
        macAdress = web.net.websafe(i.macAdress)
        bssid = web.net.websafe(i.bssid)
        startTime = web.net.websafe(i.startTime)
        endTime = web.net.websafe(i.endTime)
        latitude = web.net.websafe(i.latitude)
        longtitude = web.net.websafe(i.longtitude)
        dbOperations.insertAPAcessRecord(bssid, macAdress, startTime, endTime, latitude, longtitude)
        result = {
            "code":1,
            "info":"Upload success."
        }
        print 'Success'
        return result
        raise web.seeother('/success/sendAPFeatures')

class DelWifiInfo:
    def GET(self, bssid):
        if session.logged_in == False:
            raise web.seeother('/login')
        dbOperations.deleteAPFeature(bssid)
        return "Delete Success."

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
        return web.seeother('/')

class Blank:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/login')
        else:
            raise web.seeother('/mapDisplay')

class ApFeaturesList:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/login')
        return render.apFeaturesList(getAllAPsFeatures())

class ShowMap:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/login')
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
        i = web.input()
        lat = web.net.websafe(i.Latitude)
        lng = web.net.websafe(i.Longtitude)
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
        if session.logged_in == False:
            raise web.seeother('/login')
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
            dbOperations.insertAPFeatures(bssid, ssid, security, signal, latitude, longtitude, macAdress, timeString)
            result = {
                "code":1,
                "info":"Upload success."
                }
            print 'Success'
            return result
            raise web.seeother('/success/sendAPFeatures')

class Login:
    #create login form
    login_form = web.form.Form(
        web.form.Textbox('Username',web.form.notnull,size=30),
        web.form.Password('Password',web.form.notnull,size=30),
        web.form.Button('Login'),
    )
    def GET(self):
        #if session.logged_in == True:
        #    raise web.seeother('/mapDisplay')
        form = self.login_form()
        return render.login(form)
    def POST(self):
        i = web.input()
        username, password = web.net.websafe(i.Username), hashlib.md5(web.net.websafe(i.Password)).hexdigest()
        if not verifyLogin(username,password):
            raise web.seeother('/fail/login')
        else:
            web.setcookie('username', username)
            session.logged_in=True
            raise web.seeother('/success/login')

# Redirect to this page when user's operation failed
class Fail:
    def GET(self, operation):
        return render.fail(operation)

# Redirect to this page when user's operation succeeded
class Success:
    def GET(self, operation):
        return render.success(operation)

def verifyFeatures(featuresDict):
    t=db.select('APsFeatures', where="bssid=$featuresDict['BSSID']",vars=locals())
    for temp in t:
        dbOperations.updateAPFeatures(featuresDict)
        print 'Update Success.'
        return False      
    return True

class Logout:
    def GET(self):
        if session.logged_in == False:
            raise web.seeother('/login')
        session.logged_in=False
        session.kill()
        web.setcookie('username','',expires=-1)
        raise web.seeother('/success/logout')

def verifyLogin(username,password):
    return (username=="fishing" and password==hashlib.md5("fishing").hexdigest());

def notfound():
    return web.notfound("Sorry, the page your were looking for was not found.")
    
app.notfound = notfound

# running our server
if __name__ == '__main__':
    app.run()

