import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "UserCenter.settings")    # “你的项目.settings”
application = get_wsgi_application()  