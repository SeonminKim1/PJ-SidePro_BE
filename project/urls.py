from django.urls import path
from . import views 

# project/
urlpatterns = [
    path('', views.ProjectAPIView.as_view(), name="project_view"),
    path('upload/', views.UploadS3.as_view()),
    path('<int:project_id>', views.ProjectDetailAPIView.as_view(), name="project_detail_view")
]