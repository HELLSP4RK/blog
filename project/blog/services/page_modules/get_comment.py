from blog.models import Comment


def get_comments_by_post(post):
    return post.comments.filter(status=Comment.Status.VISIBLE).select_related('author').get_cached_trees()