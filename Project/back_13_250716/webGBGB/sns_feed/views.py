from rest_framework import generics, status, serializers # serializers 임포트 추가
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404, render, Http404
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F
from shareMain.models import ReadingGroup
from member.models import Member

# GroupChatRoom 임포트 제거
from .models import Post, Comment, UserProfile, Like

# 시리얼라이저 임포트 (이름 변경 반영)
from .serializers import (
    ReadingGroupSerializer, PostSerializer, CommentSerializer,
    UserProfileSerializer, LikeSerializer
)


User = get_user_model()


# --- HTML 렌더링 뷰 ---
# chat_id를 인자로 받아 해당 독서 모임 정보를 HTML 템플릿에 전달
def sns_html_view(request, chat_id):
    try:
        # ReadingGroup 모델에서 chat_id에 해당하는 객체를 가져옴
        reading_group = ReadingGroup.objects.get(id=chat_id)
        # ReadingGroup 모델의 tags_list @property 사용
        tag_list = reading_group.tags_list
        context = {
            'readinggroup': reading_group,
            'tag_list': tag_list
        }
        return render(request, 'chatroom_sns.html', context)
    except ReadingGroup.DoesNotExist:
        raise Http404("Reading Group does not exist")
    except Exception as e:
        # 예외 발생 시 적절한 응답 또는 로깅
        return HttpResponse(f"Error: {e}", status=500)


# --- API View ---

class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        # URL에서 reading_group_id를 가져와 해당 그룹의 게시글만 필터링
        reading_group_id = self.kwargs.get('reading_group_id')
        if reading_group_id:
            return Post.objects.filter(group__id=reading_group_id).order_by('-created_at')
        return Post.objects.all().order_by('-created_at') # 특정 그룹이 아니면 전체 게시글

    def get_serializer_context(self):
        # PostSerializer에 request 객체를 context로 전달하여 is_liked_by_user 계산에 사용
        return {'request': self.request}

    def perform_create(self, serializer):
        # Post 생성 시 author와 group 정보를 함께 저장
        reading_group_id = self.kwargs.get('reading_group_id')
        if not reading_group_id:
            # 여기에서 'serializers.ValidationError'를 사용하기 위해 'serializers'가 임포트되어야 함
            raise serializers.ValidationError({"detail": "Reading group ID is required for creating a post."})
        
        reading_group = get_object_or_404(ReadingGroup, id=reading_group_id)
        
        serializer.save(author=self.request.user, group=reading_group) # group 정보 추가


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostLikeView(APIView):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user.is_authenticated:
            # 좋아요 토글 로직
            like, created = Like.objects.get_or_create(user=user, post=post)
            if not created: # 이미 존재하면 (즉, 새로 생성되지 않았다면)
                like.delete() # 좋아요 취소
                return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
            else: # 새로 생성되었다면
                return Response({"message": "Like added"}, status=status.HTTP_201_CREATED)
        return Response({"detail": "Authentication required"}, status=status.HTTP_401_UNAUTHORIZED)


class CommentListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        post_pk = self.kwargs.get('post_pk')
        return Comment.objects.filter(post__pk=post_pk).order_by('created_at')

    def perform_create(self, serializer):
        post_pk = self.kwargs.get('post_pk')
        post = get_object_or_404(Post, pk=post_pk)
        serializer.save(author=self.request.user, post=post)


class UserProfileUploadView(APIView): # 기존 ProfileUploadView에서 이름 변경
    def post(self, request, format=None):
        user = request.user
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(user=user)

        serializer = UserProfileSerializer(user.profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            image_url = request.build_absolute_uri(user.profile.profile_image.url) if user.profile.profile_image else None
            return Response({"message": "Profile image uploaded successfully", "imageUrl": image_url}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatRoomDetailView(generics.RetrieveAPIView):
    queryset = ReadingGroup.objects.all()
    serializer_class = ReadingGroupSerializer # GroupChatRoomSerializer 대신 ReadingGroupSerializer 사용
    lookup_field = 'pk'

class ChatRoomJoinView(APIView):
    def post(self, request, pk):
        try:
            with transaction.atomic():
                reading_group = get_object_or_404(ReadingGroup, pk=pk)

                if not request.user.is_authenticated:
                    return Response({"detail": "로그인 후 가입할 수 있습니다."}, status=status.HTTP_401_UNAUTHORIZED)

                try:
                    member_to_add = Member.objects.get(user=request.user)
                except Member.DoesNotExist:
                    return Response({"detail": "연결된 Member 프로필을 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

                if member_to_add in reading_group.member.all():
                    return Response({"detail": "이미 모임의 멤버입니다."}, status=status.HTTP_400_BAD_REQUEST)

                if reading_group.member.count() >= reading_group.max_member:
                    return Response({"detail": "최대 멤버 수를 초과하여 가입할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

                reading_group.member.add(member_to_add)

                serializer = ReadingGroupSerializer(reading_group) # GroupChatRoomSerializer 대신 ReadingGroupSerializer 사용
                return Response({
                    "message": "모임에 성공적으로 가입되었습니다.",
                    "current_members": reading_group.member.count(),
                    "max_members": reading_group.max_member,
                    "reading_group_details": serializer.data
                }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)