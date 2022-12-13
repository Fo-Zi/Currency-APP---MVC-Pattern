import requests

class Model:
    def __init__(self):
        self._URL = {'exchangeR':'https://api.exchangerate.host/','gecko': 'https://api.coingecko.com/api/v3/'}

    # Parsing of present day exchange rates 
    def parseLatest(self):
        request = requests.get(self._URL['exchangeR']+'latest')
        jsonData = request.json()
        return jsonData['rates']

    # Parsing of series of data, as we want to plot only one currency at a time, we also include
    # 'base' and 'currency' in the query
    def parseTimeSeries(self,tsrequest,type):
        base = tsrequest['base']
        currency = tsrequest['currency']
        toDate = tsrequest['toDate'].toPyDate().strftime("%Y-%m-%d")
        fromDate = tsrequest['fromDate'].toPyDate().strftime("%Y-%m-%d")
 
        if type=='timeSeries':
            reqURL = self._URL['exchangeR']+'timeseries?'+'base='+base+'&symbols='+currency+'&start_date='+fromDate+'&end_date='+toDate
        elif type=='fluctuationData':
            reqURL = self._URL['exchangeR']+'fluctuation?'+'base='+base+'&symbols='+currency+'&start_date='+fromDate+'&end_date='+toDate
        
        request = requests.get(reqURL)
        jsonData = request.json()
        dates = [ d[0] for d in jsonData['rates'].items() ]
        rates = [ r[1][tsrequest['currency']] for r in jsonData['rates'].items() ] 
        return [dates,rates] 

    # Parsing available/suported currencies
    def getCurrencies(self):
        request = requests.get(self._URL['exchangeR']+'symbols')
        jsonData = request.json()
        symbols = [d[1] for d in jsonData['symbols'].items()]
        return symbols



