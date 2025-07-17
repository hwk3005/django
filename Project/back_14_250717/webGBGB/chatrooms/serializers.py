from rest_framework import serializers
from .models import ReadingGroup, ChatMessage # GroupChatRoom은 새로 정의한 모델

class GroupChatRoomSerializer(serializers.ModelSerializer):
    tags_list = serializers.SerializerMethodField()

    class Meta:
        model = ReadingGroup
        fields = '__all__' # 모든 필드를 포함
    def get_tags_list(self, obj):
    # ReadingGroup 객체의 tags 필드(콤마로 구분된 문자열)를 가져와서
        # 콤마로 분리하고 각 태그 앞뒤의 공백을 제거한 후 리스트로 반환
        if obj.tags:
            return [tag.strip() for tag in obj.tags.split(',') if tag.strip()]
        return [] # 태그가 없으면 빈 리스트 반환

class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = '__all__'