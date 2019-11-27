import os, json, io
import slack
import ssl
import certifi
import MealInfo, ClassInfo, EventInfo, Weather
import datetime, time

data = io.open('config.json', mode='r', encoding='utf-8').read()
conf = json.loads(data)
state = 'normal'
meal_list = None
class_list = None

mod_mealinfo = MealInfo.MealInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_classinfo = ClassInfo.ClassInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_eventinfo = EventInfo.EventInfo(
    conf['Open-NEIS-API']['KEY'],
    conf['Open-NEIS-API']['SD_SCHUL_CODE'],
    conf['Open-NEIS-API']['ATPT_OFCDC_SC_CODE']
)
mod_weather = Weather.Weather(
    conf['KMA-Weather-Api']['ZoneID']
)

alergi = [
':egg:'
,':glass_of_milk: '
,':fallen_leaf:'
,':peanuts:'
,':chestnut:'
,':ear_of_rice:'
,':fish:'
,':crab:'
,':shrimp:'
,':pig2:'
,':peach:'
,':tomato:'
,':pill:'
,':brain:'
,':rooster:'
,':ox:'
,':squid:'
,':shell:'
]

script = {
    "show_meallist" : "밥 맛있게 묵으리~",
    "quest_mealtime" : "아침? 점심? 저녁? 뭘 말하는고?",
    "show_classlist" : "공부 열심히 하려무나",
    "show_schedule" : "시간관리 잘 하고~"
}

def adapt_alergi_emoji(text):
    for _ in range(len(alergi)):
        text = text.replace('%d.' % (len(alergi) - _), '%s' % alergi[-1-_])
    return text

@slack.RTMClient.run_on(event="message")
def someone_msg(**payload):
    data = payload["data"]
    web_client = payload["web_client"]

    
    if 'subtype' in data:
        pass
    else:
        s = ''
        #res = web_client.users_info(user = data['user'])
        #name = res['user']['profile']['display_name_normalized']
        user_id = data["user"]
        #print(data)
        msg = ''
        
        if data['text'].find('병규형') != -1:
            if data['text'].find('급식') != -1:
                now = datetime.datetime.now()

                dow = -1
                dday = 0
                daytime = 0

                msg += '<@%s> %s:president::president::president:\n' % (data['user'], script["show_meallist"])

                if data['text'].find('내일') != -1:
                    dday += 1
                if data['text'].find('모레') != -1:
                    dday += 2
                if data['text'].find('글피') != -1:
                    dday += 3
                if data['text'].find('어제') != -1:
                    dday -= 1
                if data['text'].find('엊그제') != -1:
                    dday -= 2
                if data['text'].find('다다다다음주') != -1:
                    dday += 7 * 4
                elif data['text'].find('다다다음주') != -1:
                    dday += 7 * 3
                elif data['text'].find('다다음주') != -1:
                    dday += 7 * 2
                elif data['text'].find('다음주') != -1:
                    dday += 7
                if data['text'].find('저저번주') != -1:
                    dday -= 7 * 2
                elif data['text'].find('저번주') != -1:
                    dday -= 7
                    
                if data['text'].find('월요일') != -1:
                    dow = 0
                elif data['text'].find('화요일') != -1:
                    dow = 1
                elif data['text'].find('수요일') != -1:
                    dow = 2
                elif data['text'].find('목요일') != -1:
                    dow = 3
                elif data['text'].find('금요일') != -1:
                    dow = 4
                elif data['text'].find('토요일') != -1:
                    dow = 5
                elif data['text'].find('일요일') != -1:
                    dow = 6

                if data['text'].find('아침') != -1:
                    daytime = 1
                elif data['text'].find('점심') != -1:
                    daytime = 2
                elif data['text'].find('저녁') != -1:
                    daytime = 3
                
                if dday == 0 and dow == 0:
                    mod_mealinfo.set_date(now.year, now.month)
                    
                    if now < datetime.datetime(year=now.year,month=now.month,day=now.day,hour=7,minute=30):
                        meal_list = mod_mealinfo.get(now.day)
                        
                        msg += '*오늘 아침*\n'
                        for row in meal_list[0]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                        
                        
                    elif now < datetime.datetime(year=now.year,month=now.month,day=now.day,hour=12,minute=40):
                        meal_list = mod_mealinfo.get(now.day)
                        
                        msg += '*오늘 점심*\n'
                        for row in meal_list[1]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                        
                        
                    elif now < datetime.datetime(year=now.year,month=now.month,day=now.day,hour=18,minute=30):
                        meal_list = mod_mealinfo.get(now.day)
                        
                        msg += '*오늘 저녁*\n'
                        for row in meal_list[2]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                        
                        
                    else:
                        meal_list = mod_mealinfo.get(now.day+1)
                        
                        msg += '*내일 아침*\n'
                        for row in meal_list[0]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                        
                elif dow != -1:
                    dday += dow - datetime.datetime.today().weekday()
                    now += datetime.timedelta(days=dday)
                    if now.weekday() == 6:
                        daytime = 1
                    if daytime == 0:
                        msg = script["quest_mealtime"]
                    else:
                        
                        mod_mealinfo.set_date(now.year, now.month)
                        meal_list = mod_mealinfo.get(now.day)
                        daytime_name = ['아침', '점심', '저녁']
                        
                        msg += '*%2d월 %2d일 %2s*\n' % (now.month, now.day, daytime_name[daytime - 1])
                        for row in meal_list[daytime - 1]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                    
                elif dday != 0:
                    now += datetime.timedelta(days=dday)
                    print(now.weekday())
                    if now.weekday() == 6:
                        daytime = 1
                    if daytime == 0:
                        msg = script["quest_mealtime"]
                    else:                        
                        mod_mealinfo.set_date(now.year, now.month)
                        meal_list = mod_mealinfo.get(now.day)
                        daytime_name = ['아침', '점심', '저녁']
                        
                        msg += '*%2d월 %2d일 %2s*\n' % (now.month, now.day, daytime_name[daytime - 1])
                        for row in meal_list[daytime - 1]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                            msg += '• %s\n' % adapt_alergi_emoji(row)
                    
                else:
                    mod_mealinfo.set_date(now.year, now.month)
                    
                    meal_list = mod_mealinfo.get(now.day)
                    
                    daytime_name = ['아침', '점심', '저녁']
                    msg += '*오늘 %s*\n' % (daytime_name[daytime - 1])
                    for row in meal_list[daytime - 1]['DDISH_NM'].replace('<br/>', '\n').split('\n'):
                        msg += '• %s\n' % adapt_alergi_emoji(row)
                    
                    
                    
            elif data['text'].find('시간표') != -1:
                now = datetime.datetime.now()
                
                dow = -1
                dday = 0
                
                msg += '<@%s> %s:president::president::president:\n' % (data['user'], script["show_classlist"])
                
                if data['text'].find('내일') != -1:
                    dday += 1
                if data['text'].find('모레') != -1:
                    dday += 2
                if data['text'].find('글피') != -1:
                    dday += 3
                if data['text'].find('어제') != -1:
                    dday -= 1
                if data['text'].find('엊그제') != -1:
                    dday -= 2
                if data['text'].find('다다다다음주') != -1:
                    dday += 7 * 4
                elif data['text'].find('다다다음주') != -1:
                    dday += 7 * 3
                elif data['text'].find('다다음주') != -1:
                    dday += 7 * 2
                elif data['text'].find('다음주') != -1:
                    dday += 7
                if data['text'].find('저저번주') != -1:
                    dday -= 7 * 2
                elif data['text'].find('저번주') != -1:
                    dday -= 7
                    
                if data['text'].find('월요일') != -1:
                    dow = 0
                elif data['text'].find('화요일') != -1:
                    dow = 1
                elif data['text'].find('수요일') != -1:
                    dow = 2
                elif data['text'].find('목요일') != -1:
                    dow = 3
                elif data['text'].find('금요일') != -1:
                    dow = 4
                elif data['text'].find('토요일') != -1:
                    dow = 5
                elif data['text'].find('일요일') != -1:
                    dow = 6

                grd = 0
                cls = 0
                if data['text'].find('1학년') != -1:
                    grd = 1
                elif data['text'].find('2학년') != -1:
                    grd = 2
                elif data['text'].find('3학년') != -1:
                    grd = 3
                    
                if data['text'].find('1반') != -1:
                    cls = 1
                elif data['text'].find('2반') != -1:
                    cls = 2
                elif data['text'].find('3반') != -1:
                    cls = 3

                if grd != 0 and cls != 0:
                    if dday == 0 and dow == -1:
                        mod_classinfo.set_date(now.year, now.month, now.day)
                        class_list = mod_classinfo.get(grd, cls)
                        msg += '```'
                        msg += '*%2s학년 %s반 시간표*\n' % (grd, cls)
                        for row in class_list:
                            msg += '%1s교시. %s\n' % (row['PERIO'], row['ITRT_CNTNT'])
                        msg += '```'
                    elif dow != -1:
                        dday = dow - datetime.datetime.today().weekday()
                        now += datetime.timedelta(days=dday)
                        mod_classinfo.set_date(now.year, now.month, now.day)
                        class_list = mod_classinfo.get(grd, cls)
                        msg += '```'
                        msg += '*%2d월 %2d일 %2s학년 %s반 시간표*\n' % (now.month, now.day, grd, cls)
                        for row in class_list:
                            msg += '%1s교시. %s\n' % (row['PERIO'], row['ITRT_CNTNT'])
                        msg += '```'
                    else:
                        now += datetime.timedelta(days=dday)
                        mod_classinfo.set_date(now.year, now.month, now.day)
                        class_list = mod_classinfo.get(grd, cls)
                        msg += '```'
                        msg += '*%2d월 %2d일 %2s학년 %s반 시간표*\n' % (now.month, now.day, grd, cls)
                        for row in class_list:
                            msg += '%1s교시. %s\n' % (row['PERIO'], row['ITRT_CNTNT'])
                        msg += '```'
            elif data['text'].find('일정') != -1 or data['text'].find('행사') != -1 or data['text'].find('스케줄') != -1:
                mod_eventinfo.load()
                now = datetime.datetime.now()

                msg += '<@%s> %s:president::president::president:\n' % (data['user'], script["show_schedule"])
                msg += '```'
                for row in mod_eventinfo.get(now.year, now.month, now.day, 10):
                    #print(row['AA_YMD'], row['EVENT_NM'], row['TARGET'], end='')
                    holiday = False
                    
                    if row['SBTR_DD_SC_NM'] == '공휴일':
                        holiday = True
                    if row['SBTR_DD_SC_NM'] == '휴업일':
                        holiday = True

                    year = int(row['AA_YMD'][0:4])
                    month = int(row['AA_YMD'][4:6])
                    day = int(row['AA_YMD'][6:8])
                    msg += '%4d년 %2d월 %2d일' % (year, month, day)
                    if holiday:
                        msg += '[휴]'
                    else:
                        msg += '[　]'
                        
                    msg += ' %s %s\n' % (row['EVENT_NM'], row['TARGET'])
                    
                        
                msg += '```'
            elif data['text'].find('날씨') != -1:
                mod_weather.get()
                now = datetime.datetime(year=int(mod_weather.now[0:4]),month=int(mod_weather.now[4:6]),day=int(mod_weather.now[6:8]))
                
                for row in mod_weather.data:
                    curr = now
                    if int(row['hour']) == 24:
                        curr += datetime.timedelta(days=int(row['day']) + 1)
                        curr = curr.replace(hour=0)
                    else:
                        curr += datetime.timedelta(days=int(row['day']))
                        curr = curr.replace(hour=int(row['hour']))
                    dayofweek_name = ['월','화','수','목','금','토','일']
                    msg += '%s요일 %02d시 :thermometer:%s(%s,%s) ' % (dayofweek_name[curr.weekday()], int(curr.hour), mod_weather.check_temperature(row['temp']), mod_weather.check_temperature(row['tmn']), mod_weather.check_temperature(row['tmx']))
                    if row['sky'] == '1':
                        msg += ':sunny:'
                    elif row['sky'] == '3':
                        msg += ':sun_small_cloud:'
                    elif row['sky'] == '4':
                        msg += ':cloud: '
                    else:
                        msg += row['sky']
                        
                    if row['pty'] == '0':
                        msg += ':sunny:'
                    elif row['pty'] == '1':
                        msg += ':rain_cloud:'
                    elif row['pty'] == '2':
                        msg += ':cloud: '
                    elif row['pty'] == '3':
                        msg += ':snow_cloud: '
                    elif row['pty'] == '4':
                        msg += ':thunder_cloud_and_rain:'
                    else:
                        msg += row['pty']

                    pop = int(row['pop'])
                    if pop < 33:
                        msg += ' :closed_umbrella:'
                    elif pop < 66:
                        msg += ' :umbrella:'
                    else:
                        msg += ' :umbrella_with_rain_drops:'
                    msg += '%3s%%' % (row['pop'])
                    msg += ' :droplet:%3s%%' % (row['reh'])

                    wind_dir_emoji = [':arrow_down:', ':arrow_lower_left:', ':arrow_left:', ':arrow_upper_left:', ':arrow_up:', ':arrow_upper_right:', ':arrow_right:', ':arrow_lower_right:']

                    msg += ' %s%sm/s' % (wind_dir_emoji[int(row['wd'])], row['ws'][:3])
                        
                    msg += '\n'
                
                
        if len(data['text']) > 6 and data['text'][:6] == '&amp;^':
            msg = data['text'][6:]
        if msg != '':
            web_client.chat_postMessage(
            channel='#general',
            text=msg)
            
ssl_context = ssl.create_default_context(cafile=certifi.where())
slack_token = 'xoxb-849581889920-849264423684-WuWMYcGnmYu8qauEEgDDGmnx'
rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
rtm_client.start()

