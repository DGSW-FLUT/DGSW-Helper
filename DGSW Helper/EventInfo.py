import requests, json, io
import Module

class EventInfo(Module.Module):
    module_name = 'ClassInfo'
    def __init__(self, key, school_code, apart_code):
        self.key = key
        self.school_code = school_code
        self.apart_code = apart_code
        self.data = ''
    def load(self):
        url = 'https://open.neis.go.kr/hub/SchoolSchedule?Type=json&KEY={2}&ATPT_OFCDC_SC_CODE={0}&SD_SCHUL_CODE={1}&pSize=500'.format(self.apart_code, self.school_code, self.key)
        res = requests.get(url)
        if res.status_code == 200:
            self.data = json.loads(res.content)
        else:
            raise Exception('EventInfo::set_date Response status is not OK(200), {0}'.format(res.status_code))
    def get(self, year, month, day, maxsize=7):
        ret = []
        for row in self.data['SchoolSchedule'][1]['row']:
            if row['AA_YMD'] < '%04d%02d%02d' % (year, month, day): continue
            let = row
            #print(row['AA_YMD']) 일자
            #print(row['SBTR_DD_SC_NM']) 공휴일?
            #print(row['EVENT_NM']) 이름
                    
            grd = [row['ONE_GRADE_EVENT_YN'], row['TW_GRADE_EVENT_YN'], row['THREE_GRADE_EVENT_YN']]
            if grd[0] == 'Y' and grd[1] == 'Y' and grd[2] == 'Y':
                let['TARGET'] = '(전학년)'
            else:
                cnt = 0
                for _ in range(3):
                    if grd[_] == 'Y':
                        cnt += 1
                    
                s = '('
                for _ in range(3):
                    if grd[_] == 'Y':
                        s += str(_ + 1)
                        cnt -= 1
                        if cnt > 0:
                            s += ', '
                s += '학년)'
                let['TARGET'] = s

            ret.append(let)
            if len(ret) == maxsize: break
        return ret
    
    def state(self):
        print('<%s>' % self.module_name)
        print('Key is %s' % self.key)
        print('School Code is %s' % self.school_code)
        print('Apartment Code is %s' % self.apart_code)

print('Library, EventInfo is Loaded')
