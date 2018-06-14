#from __future__ import absolute_import, unicode_literals 绝对导入，python3默认
import os
from celery import Celery

#overriding app.gen_task_name()
#  class MyCelery(Celery):

#     def gen_task_name(self, name, module):
#         if module.endswith('.tasks'):
#             module = module[:-6]
#         return super(MyCelery, self).gen_task_name(name, module)

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ClusterManager.settings')

app = Celery('ClusterManager')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
