import requests, io, datetime, time
import Module
import xml.etree.ElementTree


class Weather(Module.Module):
    module_name = 'Weather'
    zone = ''
    now = ''
    data = []
    def __init__(self, zone):
        self.zone = zone
    def get(self):
        url = "http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=%s" % (self.zone)
        res = requests.get(url)
        tree = xml.etree.ElementTree.fromstring(res.content)

        weather = []
        self.now = tree.find('channel').find('item').find('description').find('header').find('tm').text
        for _ in tree.find('channel').find('item').find('description').find('body'):
            weather.append({})
            idx = int(_.attrib['seq'])
            for e in _:
                weather[idx][e.tag] = e.text

        self.data = weather
    def check_temperature(self, text):
        if text == '-999.0':
            return '  -  '
        return '%3d℃' % int(float(text))

    def state(self):
        print('<%s>' % self.module_name)
        print('Key is %s' % self.key)
        print('School Code is %s' % self.school_code)
        print('Apartment Code is %s' % self.apart_code)

print('Library, Weather is Loaded')

if __name__ == '__main__':
    ZONE_ID = '2771038000'
    mod_weather = Weather(ZONE_ID)
    mod_weather.get()
    
    now = datetime.date(year=int(mod_weather[0:4]),month=int(month=mod_weather[4:6]),day=int(day=mod_weather[6:8]))

    print(now)
    
    #for row in weather:
        #print('%s일차 %2s시 %4s(%4s/%4s) | %s | 습도 %2s%%'%(row['day'], row['hour'], check_temperature(row['temp']), check_temperature(row['tmn']), check_temperature(row['tmx']), row['wfKor'], row['reh']))
        # row['day'] 날짜
        # row['hour'] 시간
        # row['temp'] 현재온도
        # row['tmx'] 최고온도
        # row['tmn'] 최저온도
        # row['sky'] 하늘상태 [1 맑음, 3 구름, 4 흐림]
        # row['pty'] 강수상태 [0 없음, 1   비, 2 눈비, 3  눈, 4 소나기]
        # row['pop'] 강수확률
        # row['ws'] 풍속
        # row['wd'] 풍향 (북, 북동, 동, 남동, 남, 남서, 서, 북서)
        # row['reh'] 습도
