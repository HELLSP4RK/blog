from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication

from api.permissions import IsOwnerOrReadOnlyPermission
from api.serializers import *
from blog.services.get_category import get_root_categories, get_category
from blog.services.get_comment import get_comments_by_user, get_comments_by_post
from blog.services.get_post import *
from blog.services.get_user import get_user


class PostListView(ListAPIView):
    queryset = get_public_posts()
    serializer_class = PostSerializer


class PostView(RetrieveAPIView):
    serializer_class = PostSerializer

    def get_object(self):
        return get_post(pk=self.kwargs['id'], slug=self.kwargs['slug'])


class PostListByUserView(ListAPIView):
    serializer_class = PostSerializer

    def __own_page(self):
        return self.request.user.username == self.kwargs['username']

    def get_queryset(self):
        username = self.kwargs['username']
        if self.__own_page():
            return get_all_posts_by_user(username)
        return get_public_posts_by_user(username)


class PostListByCatView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_posts_by_category(slug=self.kwargs['slug'])


class PostListByTagView(ListAPIView):
    serializer_class = PostSerializer

    def get_queryset(self):
        return get_posts_by_tag(slug=self.kwargs['slug'])


class CommentListByUserView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return get_comments_by_user(username=self.kwargs['username'])


class CommentListByPostView(ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return get_comments_by_post(pk=self.kwargs['id'], slug=self.kwargs['slug'])


class UserView(RetrieveAPIView):
    serializer_class = UserSerializer

    def get_object(self):
        return get_user(username=self.kwargs['username'])


class AddPostView(CreateAPIView):
    serializer_class = AddPostSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )


class AddCommentView(CreateAPIView):
    serializer_class = AddCommentSerializer
    authentication_classes = (TokenAuthentication, SessionAuthentication)
    permission_classes = (IsAuthenticated, )


class EditPostView(RetrieveUpdateAPIView):
    serializer_class = AddPostSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission, )

    def get_object(self):
        return get_post(pk=self.kwargs['id'], slug=self.kwargs['slug'])


class RemovePostView(RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsOwnerOrReadOnlyPermission, )

    def get_object(self):
        return get_post(pk=self.kwargs['id'], slug=self.kwargs['slug'])


class RootCatListView(ListAPIView):
    serializer_class = CategorySerializer
    queryset = get_root_categories()


class CatListByCatView(ListAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        category = get_category(slug=self.kwargs['slug'])
        return get_child_categories(category)
