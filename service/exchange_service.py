import requests

def get_currency_rates(id_currency,count):
    URL = f"https://www.nbrb.by/api/exrates/rates/{id_currency}"
    r = requests.get(url = URL)
    data = r.json()
    rate=data.get("Cur_OfficialRate")
    scale=data.get("Cur_Scale")
    return count/(rate/scale)