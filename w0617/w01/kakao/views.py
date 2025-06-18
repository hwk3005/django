from django.shortcuts import render
from django.http import HttpResponse
import requests
import json

# 카카오 로그인에서 code값을 전달받음.
def oauth(request):
    code = request.GET.get('code')
    print('code: ',code)
    
    # token키를 받기 위해 다음카카오로 code값을 전달
    ## 카카오로그인 정보
    client_id = 'd7b881ab422a9bbe1c5b2a51cf11d8ab'
    redirect_uri = 'http://localhost:8000/kakao/oauth'
    
    
    return HttpResponse(f'code: {code}')