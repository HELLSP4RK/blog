from blog.models import Post


def get_most_popular_tags(how_much=5):
    return Post.tags.most_common()[:how_much]