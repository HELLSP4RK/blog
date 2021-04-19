def get_comments_count_by_post(post):
    return post.comments.filter(status='visible').count()


def get_posts_count_by_user(user):
    return user.posts.count()


def get_comments_count_by_user(user):
    return user.comments.count()


def get_queryset_count(queryset):
    return queryset.count()
