from django.urls import re_path

from bootstrap_ui.views import set_theme

urlpatterns = [
    re_path(r'^set_theme/$', set_theme, name='set_theme'),
]
