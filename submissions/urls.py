from django.urls import path
from .views import SubmissionListView, SubmissionUpdateView

urlpatterns = [
    path('', SubmissionListView.as_view()),
    path('update/<uuid:pk>/', SubmissionUpdateView.as_view()),
]
