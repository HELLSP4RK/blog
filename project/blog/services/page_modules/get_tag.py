from blog.models import Post


def get_most_popular_tags():
    return Post.tags.most_common()[:5]