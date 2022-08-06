from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver  # импортируем нужный декоратор
from .models import Post, PostCategory
from .tasks import new_post_subscription
from .apscheduler import its_time



@receiver(m2m_changed, sender=PostCategory)
def notify_subscribers(sender, instance, action, **kwargs):
    pass
    #if action == 'post_add':
         #print('notifying subscribers from signals...', instance.id)
         #new_post_subscription.apply_async([instance.id])



@receiver(its_time, sender='Weekly')
def notify_subscribers(sender, **kwargs):
    pass