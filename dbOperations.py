# -*- coding: cp936 -*-
#coding = utf-8

import web
import datetime
import config

db = web.database(dbn=config.dbn, db=config.db, user=config.dbuser, pw=config.dbpw)
'''
def insertUser(username,password):
    db.insert('Users',username=username,password=password)

def insertAuthorizedAPs(bssid, ssid, channel, vendor, location):
    db.insert('AuthorizedAPs',bssid=bssid,ssid=ssid,channel=channel,vendor=vendor,location=location)

def deleteAuthorizeAPs(bssid):
    db.delete('AuthorizedAPs',where = 'bssid = $bssid', vars = locals())

def insertAPFeatures(bssid, ssid, channel, vendor, location, security, signal, noise, route):
    db.insert('APsFeatures', bssid=bssid, ssid=ssid, channel=channel, vendor=vendor, location=location, security=security, signal=signal, noise=noise, route=route)

def insertAPCredits(bssid, location_history, useraccess_history, security_history, route_history, credit):
    db.insert('APsCredit', bssid=bssid, location_history=location_history, useraccess_history=useraccess_history, security_history=security_history, route_history=route_history, credit=credit)
'''

def insertAPAcessRecord(bssid, macAdress, startTime, endTime, latitude, longtitude):
    db.insert('APAcessRecord',
              bssid=bssid,
              macAdress=macAdress,
              startTime=startTime,
              endTime=endTime,
              latitude=latitude,
              longtitude=longtitude )
    
#一个bssid只能有一个content，后面应该改为一个bssid&&macAdress对应一个content
def insertTraceRouteRecord(bssid, macAdress, content):
    results = db.select('TraceRouteRecord', where = 'bssid = $bssid and macAdress=$macAdress', vars = locals())
    traceRouteRecord = []
    cnt = 0
    for result in results:
        cnt = cnt + 1
    print cnt
    if(cnt==0):
        db.insert('TraceRouteRecord',
              bssid=bssid,
              macAdress=macAdress,
              content=content)
    else:
        db.update('TraceRouteRecord',
              where = "bssid=$bssid and macAdress=$macAdress",
              content=content,
              vars = locals() )

def insertAPFeatures(bssid, ssid, security, signal, latitude, longtitude, macAdress, timeString):
    db.insert('APsFeatures',
              bssid=bssid,
              ssid=ssid,
              security=security,
              signals=signal,
              latitude=latitude,
              longtitude=longtitude,
              macAdress=macAdress,
              timeString=timeString )

def updateAPFeatures(dic):
    db.update('APsFeatures',   
              where="bssid=$dic['BSSID']",  #The "$" shouldn't be removed.
              ssid=dic['SSID'],
              security=dic['SECURITY'],
              signals=dic['SIGNALS'],
              latitude=dic['LATITUDE'],
              longtitude=dic['LONGTITUDE'],
              macAdress=dic['MACADRESS'],
              timeString=dic['TIMESTRING'], 
	      vars = locals() )  
    #must add "vars = locals()"
    #to get the value of dic['BSSID'] from the outside scope
			  
def selectAPFeatures():
    result = db.select('APsFeatures')
    return result

def selectAPAcessRecord():
    result = db.select('APAcessRecord')
    return result

def selectTraceRouteRecord():
    result = db.select('TraceRouteRecord')
    return result

def deleteAPFeature(bssid):
    db.delete('APsFeatures',where = 'bssid = $bssid', vars = locals())

def deleteAPAcessRecord(startTime):
    db.delete('APAcessRecord',where = 'startTime = $startTime', vars = locals())

def querySafety(bssid):
    result = db.select('exceltomysql', what = 'safe', where = 'bssid = $bssid', vars = locals())
    return result	

def insertSafety(bssid, safe):
    db.insert('exceltomysql', bssid = bssid, safe = safe)
