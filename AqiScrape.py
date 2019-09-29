# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 15:19:47 2019

@author: wqd180009
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pytz

class Country: # only valid for country with 1 timezone
  def __init__(self, name, timezone):
    self.name = name
    self.timezone = timezone
    
class City:
  def __init__(self, name, url, timezone):
    self.name = name
    self.url = url
    self.timezone = timezone
    
  def __str__(self):
     return "(" + self.name + "," + self.url  + "," + self.timezone + ")"
 
class AirQuality:
  def __init__(self, city, time, aqi, temp, pressure, humidity, wind):
    self.city = city
    self.time = time
    self.aqi = aqi
    self.temp = temp
    self.pressure = pressure
    self.humidity = humidity
    self.wind = wind
    
  def __str__(self):
     return '{{"City":"{}", "Time":"{}", "Aqi":{}, "Temp":{}, "Pressure":{}, "Humidity":{}, "Wind":{}}}\n'.format(self.city, self.time, self.aqi, self.temp, self.pressure, self.humidity, self.wind)
    

def getCitiesLink(country : Country):
    page = requests.get("http://aqicn.org/city/all")
    print ("Scrapping from http://aqicn.org/city/all for {}".format(country.name))

    soup = BeautifulSoup(page.content, 'html.parser')
    import re
    count = 0
    cities = []   
    for elem in soup.find_all(href=re.compile(country.name.lower()), text=True):
        cities.append(City(elem.text, elem.get('href'),country.timezone))
        count = count + 1    
    print("{} {} cities loaded: ".format(count, country.name))
    return cities    

def getAirQuality(city: City):
    def buildTime(timeTxt, timezone):   # String from website: Updated on Sunday 14:00
        time = timeTxt[len(timeTxt)-5:len(timeTxt)]
        tz = pytz.timezone(pytz.country_timezones(timezone)[0])
        d = datetime.now(tz)
        return "{} {}".format(d.strftime("%Y-%m-%d"), time)

    def getAqi(soup): 
        cur_aqiTag = soup.find(id='cur_aqi')
        if (cur_aqiTag != None):
            return cur_aqiTag.text
        pm25Tag = soup.find(id='cur_pm25')
        if (pm25Tag!=None):
            return pm25Tag.text
        
        pm10Tag = soup.find(id='cur_pm10')
        if (pm10Tag!=None):
            return pm10Tag.text 
        
        return None

    def getText(element):
        try:
            return element.text
        except:
            return None
        
    page = requests.get(city.url)
    print ("Scrapping air quality index for {}".format(city.name))
    soup = BeautifulSoup(page.content, 'html.parser')
    
    try:
        timeTxt = getText(soup.find(id='aqiwgtutime'))
        aqi = getAqi(soup)
        temp = getText(soup.find(id='cur_t'))
        pressure = getText(soup.find(id='cur_p'))
        humidity = getText(soup.find(id='cur_h'))
        wind = getText(soup.find(id='cur_w'))
        time = buildTime(timeTxt, city.timezone)
        return AirQuality(city.name, time, aqi, temp, pressure, humidity, wind)
    except Exception as e:
        print ("Fail to getAirQuality for {}".format(city),e)


def write(fileName, aqi):
    f = open(fileName, "a")
    f.write(aqi.__str__())
    
    f.close()

countries = [Country("Malaysia","my")]
"""
countries = [Country("Malaysia","my")], 
             Country("Indonesia","in"),
             Country("Singapore","sg"),
             Country("Thailand","th")]
"""
countryCities = []
for country in countries: 
    countryCities.extend(getCitiesLink(country))
print("Total cities loaded : {}".format(len(countryCities)))


for city in countryCities:
    fileName = "AirQuality_{}.data".format(datetime.now().strftime("%Y%m%d_%H"))
    write(fileName,getAirQuality(city))

print("Done")    

