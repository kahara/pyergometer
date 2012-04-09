from lxml import etree
import re


class Session:
    def __init__(self, session=None):
        root = etree.parse(session).getroot()
        self.name = root.attrib['name']
        self.duration = self.parse_timestring(root.attrib['duration'])
        
        for timeevent in root.find('timeEvents'):

            action = timeevent.find('action').attrib['type']
            value = float(timeevent.find('action').attrib['value'])

            time = timeevent.attrib['time']
            if time[0] == '+':
                for t in range(0, self.parse_timestring(time.split('+')[1])-1):
                    prevstep = self.steps[-1:][0]
                    self.steps.append({
                            'time': prevstep['time']+1,
                            'power': prevstep['power'],
                            'pulse': prevstep['pulse']
                            })

                prevstep = self.steps[-1:][0]
                self.steps.append({
                        'time': prevstep['time']+1,
                        'power': value if action == 'power' else 0,
                        'pulse': value if action == 'pulse' else 0
                        })
            
            elif time == '0' and action == 'power':
                self.steps = []
                self.steps.append({
                        'time': 0,
                        'power': value,
                        'pulse': 0
                        })
        
        for i in range(0, self.duration - len(self.steps)):
            prevstep = self.steps[-1]
            self.steps.append({
                    'time': prevstep['time']+1,
                    'power': prevstep['power'],
                    'pulse': prevstep['pulse']
                    })
    
    def parse_timestring(self, s):
        duration = 0
        for component in re.findall('(\d*(h|m|s))', s):
            if component[1] == 'h':
                duration += int(component[0].split('h')[0]) * 3600
            if component[1] == 'm':
                duration += int(component[0].split('m')[0]) * 60
            if component[1] == 's':
                duration += int(component[0].split('s')[0])
        
        return duration

    def step(self, second):
        return self.steps[second]
