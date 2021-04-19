from blog.services.get_user import get_subscribers_by_category


def subscribe_or_unsubscribe_user(category, user):
    subscribers = get_subscribers_by_category(category)
    if user in subscribers:
        category.subscription.subscribers.add(user)
    else:
        category.subscription.subscribers.remove(user)
