import requests as req

r=req.get('https://rutube.ru/api/tags/video/5994/?noSubs=true').json()

q='сезон'
result=[]
for video in r['results']:
    if q in video['title']:
        result.append(video)

print('\n'.join([r['title'] for r in result]))


# from datetime import datetime, date
# datetime_str = '2023-11-09T11:00:15' #'09/19/22 13:55:26'
# days = date.today() - datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S').date()
# print(days.days)