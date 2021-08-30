from datetime import  date,datetime,timedelta
import requests
from banxico_externalapi.models import Banxico

def call_banxico_api():
    headers={'Bmx-Token':'26ce267411694d00a92d21ae76e6e3da5a005aba9698ac5988a87bfa9817cd54'}
    request = requests.get(
        "https://www.banxico.org.mx/SieAPIRest/service/v1/series/SF43718/datos/2021-07-20/2021-08-30",
        headers=headers,
        timeout=10
    )
    
    print(request.json()['bmx']['series'][0]['datos'][-1])
    r_last_date=request.json()['bmx']['series'][0]['datos'][-1]
    date_split=r_last_date['fecha'].split('/')
    r_last_date['fecha']=date_split[-1]+'-'+date_split[-2]+'-'+date_split[-3]
    return r_last_date

def update_data_from_banxico():
    banxico_count=Banxico.objects.count()
    if(banxico_count==0):
        r_last_date=call_banxico_api()
        Banxico.objects.create(last_date=r_last_date['fecha'],dollar_price=r_last_date['dato'])
    elif(banxico_count>1):
        Banxico.objects.delete()
        r_last_date=call_banxico_api()
        Banxico.objects.create(last_date=r_last_date['fecha'],dollar_price=r_last_date['dato'])
    else:
        banxico_id=Banxico.objects.first()
        print(banxico_id.last_date)
        last_date=datetime.strptime(str(banxico_id.last_date), '%Y-%m-%d').date()
        today_date=date.today()
        today_week=today_date.weekday()
        last_operational_day=today_date
        
        if(today_week>4):
            last_operational_day=today_date-timedelta(days=today_week-4)

        if(last_operational_day > last_date):
            r_last_date=call_banxico_api()
            Banxico.objects.update(last_date=r_last_date['fecha'],dollar_price=r_last_date['dato'])