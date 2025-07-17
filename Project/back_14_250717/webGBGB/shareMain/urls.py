from django.urls import path,include
from . import views

app_name = 'shareMain'
urlpatterns = [
    path('Share_Main/', views.Share_Main, name='Share_Main'),
    path('Share_Main/', views.Share_Main, name='search_groups'),  # 검색 기능 메인 뷰에서 처리
    path('Share_AddGroup/', views.Share_AddGroup, name='Share_AddGroup'),
    path("shareMain/ajax_search/", views.ajax_search, name="ajax_search"),  # 책 모달창 검색 관련
]
