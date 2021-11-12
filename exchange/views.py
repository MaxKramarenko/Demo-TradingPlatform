from django.shortcuts import render
from .trade import Trade
from django.http import HttpResponse, JsonResponse
from .models import TradeHistory, Portfolio
from .common_functions import Give_equivalent
from django.contrib.auth.decorators import login_required
import json
import re

# Create your views here.
def home(request):
	return render(request, 'exchange/index.html')


def signUp(request):
	return render(request, 'registration/signup.html')

def markets(request):
	return render(request, 'exchange/markets.html')

def symbolInfo(request):
	return render(request, 'exchange/symbol-info.html')

def heatMap(request):
	return render(request, 'exchange/heatmap.html')

def messages(request):
	context = {
		'title' : 'Test',
		'redirect' : 'login',
		'message' : 'Succesfull',
	}
	return render(request, 'registration/messages.html', context=context)

# _________________________________________________________

@login_required()
def trade(request, value):
	# value = re.sub('\'', '\"', value)
	# value = json.loads(value)

	# try:
	# 	Portfolio.objects.get(cryptoName='USDT')
	# except:
	# 	newObj = Portfolio(cryptoName='USDT', amount=1000.0, equivalentAmount=None)
	# 	newObj.save()
	#
	# tradeObject = Trade(value['type'], value['pair'], float(value['amount']))
	# result = tradeObject.result

	# obj = Portfolio.objects.get(cryptoName='ETH')
	# obj.amount = 1
	# obj.save()
	obj = Portfolio.objects.filter(usr=request.user)
	print(obj)


	return HttpResponse(str(request.user))


def portfolio(request):
	eq = Give_equivalent()
	resJson = {}
	i = 0
	for item in Portfolio.objects.all().iterator():
		if item.cryptoName == 'USDT':
			equivalentAmount = None
		else:
			equivalentAmount = eq.calc_equivalent(item.cryptoName, 'USDT', item.amount)[1]
		resJson[i] = {'cryptoName': item.cryptoName, 'amount': item.amount, 'equivalentAmount': equivalentAmount}
		i += 1

	return JsonResponse(resJson)


def tradinghistory(request):
	resJson = {}
	i = 0
	for item in TradeHistory.objects.all().iterator():
		resJson[i] = {'type': item.type, 'pair': item.pair, 'pairPrice': item.pairPrice, 'amount': item.amount,'price': item.price, 'timeStamp': item.timeStamp}
		i += 1

	return JsonResponse(resJson)



