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

def selectAPFeatures():
    result = db.select('APsFeatures')
    return result
