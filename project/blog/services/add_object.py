from blog.services.get_comment import get_comment
from blog.services.get_post import get_post

from blog.models import *


def add_comment(author, post_id, post_slug, content, parent_id):
    comment = Comment(author=author,
                      post=get_post(pk=post_id, slug=post_slug),
                      content=content)
    if parent_id:
        comment.parent = get_comment(pk=parent_id)
    comment.save()
