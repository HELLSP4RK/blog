from blog.models import Post


def get_comments_count_by_post(post):
    return post.comments.filter(status='visible').count()


def get_posts_count_by_user(user, auth_user):
    if user == auth_user:
        return user.posts.count()
    return Post.publications.filter(author=user).count()


def get_comments_count_by_user(user):
    return user.comments.count()


def get_queryset_count(queryset):
    return queryset.count()
