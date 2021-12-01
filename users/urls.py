from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from DjangoFRCS import settings
from django.conf.urls import url

urlpatterns = [
    path('', views.index, name = 'home-view'),
    path('login/', views.login, name = 'login-view'),
    path('register/', views.register, name = 'register-view'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name = 'logout-view'),
    path('profile/', views.profile, name = 'profile-view'),
  
    path('<int:userId>/upload/', views.imageUpload, name = 'image-upload-view'),
    path('<int:userId>/passwordChange/', views.passwordUpdate, name = 'password-change-view'),
    path('team-management/', views.teamManagement, name = 'management-view'),
    path('user-manage/<int:userId>', views.teamManagementUserEdit, name = 'management-user-view'),
    path('<int:userId>/profile-edit/', views.ProfileSettings, name = 'profile-settings-view'),
    path('<int:userId>/account-edit/', views.accountEdit, name = 'account-settings-view'),

    path('guest/', views.guest, name = 'guest-view'),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate_account, name='activate'),
    path('changelog/', views.changelog, name='changelog-view'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),  name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),  name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),  name='password_reset_complete'),
    path('delete-user/', auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),  name='password_reset_complete'),
    
    path('pit/<str:team_num>/', views.pitUpdate, name = 'pit-update-view'),
    path('match/<str:match_id>/', views.gameUpdate, name = 'game-update-view'),
  ]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
