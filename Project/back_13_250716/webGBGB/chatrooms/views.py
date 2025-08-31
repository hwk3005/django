from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import ReadingGroup 
from .serializers import GroupChatRoomSerializer
from django.db import transaction
import os # 파일 업로드 경로를 위해
from django.conf import settings # MEDIA_URL, MEDIA_ROOT 사용을 위해

def chatroom_detail(request,chat_id):
    qs = ReadingGroup.objects.filter(id=chat_id)
    tag_list = qs[0].tag.split(",") if qs[0].tag else []
    context = {'readinggroup':qs[0],'tag_list':tag_list}
    return render(request,'chatroom_detail.html',context)
    
def chatroom_join(request):
    return render(request,'chatroom_sns.html',)