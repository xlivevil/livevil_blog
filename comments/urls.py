from django.urls import path, include

from comments import views

app_name = 'comments'
urlpatterns = [
    path('<int:pk>', views.comment_preview, name='comment'),

]