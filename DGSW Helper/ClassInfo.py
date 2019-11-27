import requests, json, io
import Module

class ClassInfo(Module.Module):
    module_name = 'ClassInfo'
    def __init__(self, key, school_code, apart_code):
        self.key = key
        self.school_code = school_code
        self.apart_code = apart_code
        self.year = 0
        self.month = 0
        self.day = 0
        self.data = ''
    def set_date(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day
        url = 'https://open.neis.go.kr/hub/hisTimetable?Type=json&KEY={2}&ATPT_OFCDC_SC_CODE={0}&SD_SCHUL_CODE={1}&TI_FROM_YMD={3:04d}{4:02d}{5:02d}&TI_TO_YMD={3:04d}{4:02d}{5:02d}'.format(self.apart_code, self.school_code, self.key, year, month, day)
        res = requests.get(url)
        if res.status_code == 200:
            self.data = json.loads(res.content)
        else:
            raise Exception('ClassInfo::set_date Response status is not OK(200), {0}'.format(res.status_code))
    def get(self, grade, cls):
        ret = []
        for row in self.data['hisTimetable'][1]['row']:
            if row['GRADE'] == '%d' % grade and row['CLRM_NM'] == '%d' % cls:
                ret.append(row)
                
        return ret
    def state(self):
        print('<%s>' % self.module_name)
        print('Key is %s' % self.key)
        print('School Code is %s' % self.school_code)
        print('Apartment Code is %s' % self.apart_code)

print('Library, ClassInfo is Loaded')
