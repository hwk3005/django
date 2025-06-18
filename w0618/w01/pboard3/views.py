from django.shortcuts import render
import requests
import json

### 전역변수
dlist = []  # list함수에서 공공데이터를 가지고 와서 view함수에 전달

# 공공데이터 리스트
def list(request):
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
    return render(request,'pboard3/list.html',context)

