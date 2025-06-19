from django.shortcuts import render
from django.http import JsonResponse
import requests
import json

### 전역변수
dlist = []  # list함수에서 공공데이터를 가지고 와서 view함수에 전달

## ajax통신 - 리턴타입 JsonResponse
def searchAjax(request):
    ## 영화데이터 가져오기
    targetDt = request.POST.get('searchInput','20250617')
    print('targetDt : ',targetDt)
    # 공공데이터 가져오기에 필요한 정보
    key = 'b4cefdc91025f56609b0e03df7a460a0'
    # targetDt = '20250617'
    url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={targetDt}'
     # 공공데이터 가져오기
    response = requests.get(url)          # 공공데이터 가져온 타입 : str타입
    json_data = json.loads(response.text)  # json타입으로 변경 -> dict타입
    # 필요한 데이터, 리스트로 변경해서 전달
    dlist = json_data['boxOfficeResult']['dailyBoxOfficeList']
    print("10개 : ",dlist)
    context = {'list':dlist}
    return JsonResponse(context) 
    


# 공공데이터 리스트
def list(request):
    # 공통영역 : 영화데이터 호출
    context = publicScreen('20250617')
    return render(request,'pboard3/list.html',context)


## 공통영역 : 영화데이터 가져오기 함수
def publicScreen(targetDt):
    global dlist #전역변수 사용
    # 공공데이터 가져오기에 필요한 정보
    key = 'b4cefdc91025f56609b0e03df7a460a0'
    targetDt = '20250617'
    url = f'http://kobis.or.kr/kobisopenapi/webservice/rest/boxoffice/searchDailyBoxOfficeList.json?key={key}&targetDt={targetDt}'
     # 공공데이터 가져오기
    response = requests.get(url)          # 공공데이터 가져온 타입 : str타입
    json_data = json.loads(response.text)  # json타입으로 변경 -> dict타입
    # 필요한 데이터, 리스트로 변경해서 전달
    dlist = json_data['boxOfficeResult']['dailyBoxOfficeList']
    print("10개 : ",dlist)
    
    context = {'list':dlist}
    return context
