from rest_framework import serializers

from accounts.api.serializers import UserDetailSerializer

from comments.models import Comment


from posts.models import Post

class PostCreateUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('title','content','publish')



post_detail_url = serializers.HyperlinkedIdentityField(
    view_name='posts-api:detail',
    lookup_field='slug'
)

class PostDetailSerializer(serializers.ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = serializers.SerializerMethodField()
    html = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ('url','id',
            'user','title','slug',
            'content','html','publish',
            'comments','image')

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    # def get_comments(self, obj):
    #     c_qs = Comment.objects.filter_by_instance(obj)
    #     comments = CommentSerializer(c_qs, many=True).data
    #     return comments

class PostListSerializer(serializers.ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ('url', 'user',
        'title','content','publish')

