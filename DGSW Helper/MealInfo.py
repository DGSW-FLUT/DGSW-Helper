import requests, json, io
import Module

class MealInfo(Module.Module):
    module_name = 'MeanInfo'
    def __init__(self, key, school_code, apart_code):
        self.key = key
        self.school_code = school_code
        self.apart_code = apart_code
        self.year = 0
        self.month = 0
        self.data = ''
    def set_date(self, year, month):
        self.year = year
        self.month = month
        url = 'https://open.neis.go.kr/hub/mealServiceDietInfo?Type=json&KEY={2}&ATPT_OFCDC_SC_CODE={0}&SD_SCHUL_CODE={1}&MLSV_FROM_YMD={3:04d}{4:02d}01&MLSV_TO_YMD={3:04d}{4:02d}31'.format(self.apart_code, self.school_code, self.key, year, month)
        res = requests.get(url)

        if res.status_code == 200:
            self.data = json.loads(res.content)
        else:
            raise Exception('MealInfo::set_date Response status is not OK(200), {0}'.format(res.status_code))
    def get(self, day):
        ret = []
        for row in self.data['mealServiceDietInfo'][1]['row']:
            if row['MLSV_FROM_YMD'] == '%04d%02d%02d' % (self.year, self.month, day):
                ret.append(row)
                
        return ret
    def state(self):
        print('<%s>' % self.module_name)
        print('Key is %s' % self.key)
        print('School Code is %s' % self.school_code)
        print('Apartment Code is %s' % self.apart_code)

print('Library, MealInfo is Loaded')
