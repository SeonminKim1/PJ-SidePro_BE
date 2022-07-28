from django.urls import path
from . import views 

# reommand/
urlpatterns = [
    path('', views.RecommendView.as_view()),
]