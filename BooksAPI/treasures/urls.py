from django.urls import path
from . import views

urlpatterns = [
    # path('',views.PostAPIView.as_view()),
    path('',views.ListCreateAPIView.as_view()),
    path('<int:pk>/',views.BooksAPIView.as_view(),name="books-details"),
    path('<int:pk>/update/',views.PutAPIView.as_view(),name="books-edit"),
    path('<int:pk>/delete/',views.DeleteAPIView.as_view()),
    # path('list/',views.ListAPIView.as_view()),
    
]