from rest_framework import serializers
from .models import Post, Comment, UserProfile, Like
from django.contrib.auth import get_user_model
from shareMain.models import ReadingGroup # ReadingGroup 모델이 shareMain 앱에 있으므로 이렇게 임포트합니다.

User = get_user_model()


class ReadingGroupSerializer(serializers.ModelSerializer):
    # ReadingGroup 모델의 ManyToManyField인 'member'를 직렬화합니다.
    # PrimaryKeyRelatedField를 사용하면 멤버들의 ID 목록을 반환합니다.
    member = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    # ReadingGroup 모델에 @property tags_list가 있으므로,
    # fields = '__all__' 에 포함될 경우 자동으로 직렬화됩니다.
    # 따라서, 이 시리얼라이저 내에서 별도로 SerializerMethodField를 정의할 필요는 없습니다.

    class Meta:
        model = ReadingGroup
        fields = '__all__' # tags_list @property가 자동으로 포함됩니다.

    # 이곳에 있던 get_tags_list 메서드는 모델의 @property와 중복되어 삭제되었습니다.


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    author_profile_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('author', 'post', 'created_at', 'updated_at')

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_profile_image_url(self, obj):
        if hasattr(obj.author, 'profile') and obj.author.profile.profile_image:
            return obj.author.profile.profile_image.url
        return None


class PostSerializer(serializers.ModelSerializer):
    author_username = serializers.SerializerMethodField()
    author_profile_image_url = serializers.SerializerMethodField()
    # group 필드를 ReadingGroupSerializer를 사용하여 그룹 정보 포함
    group = ReadingGroupSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ('author', 'group', 'created_at', 'updated_at')

    def get_author_username(self, obj):
        return obj.author.username

    def get_author_profile_image_url(self, obj):
        if hasattr(obj.author, 'profile') and obj.author.profile.profile_image:
            return obj.author.profile.profile_image.url
        return None

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked_by_user(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.likes.filter(user=request.user).exists()
        return False


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
        read_only_fields = ('user', 'post', 'created_at')