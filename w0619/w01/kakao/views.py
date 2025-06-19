from django.shortcuts import render,redirect
from django.http import HttpResponse
import requests
import json

# 카카오 로그인에서 code값을 전달 받음.
def oauth(request):
    code = request.GET.get('code')
        
    # token키를 받기 위해 다음카카오로 code값을 전달
    ## 카카오로그인 정보
    Content_Type = 'application/x-www-form-urlencoded;charset=utf-8'
    grant_type = 'authorization_code' 
    client_id = 'd558062bbe7633e69b9878d4e029696e'
    redirect_uri = 'http://localhost:8000/kakao/oauth'
    kakao_token_url = 'https://kauth.kakao.com/oauth/token'
    
    # data파일 묶음
    request_data = {
        'grant_type':grant_type,
        'client_id':client_id,
        'redirect_uri':redirect_uri,
        'code':code
    }
    
    # header 묶음
    token_headers = {
        'Content-Type':Content_Type
    }
    
    # 카카오로그인 토큰 요청 - post
    token_data = requests.post(kakao_token_url,data=request_data,headers=token_headers)
    
    # json타입으로 변경
    token_json = token_data.json()
    
    # 토큰키 받음.
    access_token = token_json.get('access_token')
    
    # 개인프로필 받기에 필요한 정보
    kakao_profile_url = 'https://kapi.kakao.com/v2/user/me'
    auth_headers = {
        'Authorization':f'Bearer ${access_token}',
        'Content-Type':'application/x-www-form-urlencoded;charset=utf-8',
    }
    # 개인정보 요청
    user_info = requests.get(kakao_profile_url,headers=auth_headers)
    # json타입으로 변경
    user_info_json = user_info.json()
    print('전체응답정보 : ',user_info_json)
    print('회원번호 : ',user_info_json.get('id'))
    kakao_account = user_info_json.get('kakao_account')
    kakao_profile = kakao_account.get('profile')
    kakao_nickname = kakao_profile.get('nickname')
    kakao_thumbnail_image_url = kakao_profile.get('thumbnail_image_url')
    kakao_profile_image_url = kakao_profile.get('profile_image_url')
    print('카카오계정 전체정보 : ',kakao_account)
    print('카카오계정 프로필 정보 : ',kakao_profile)
    print('카카오계정 닉네임 : ',kakao_nickname)
    print('프로필 미리보기 이미지 URL : ',kakao_thumbnail_image_url)
    print('프로필 사진 URL : ',kakao_profile_image_url)
    
    # request.session.session_id = user_info_json.get('id')
    # return redirect('/')
    return HttpResponse(f'code : {code}, token json:{token_json}<br>닉네임:{kakao_nickname},<br>프로필 사진:{kakao_thumbnail_image_url}')
