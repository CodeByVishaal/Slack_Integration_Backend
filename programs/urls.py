from django.urls import path
from .views import ProgramListView, ProgramUpdateView

urlpatterns = [
    path('', ProgramListView.as_view()),
    path('update/<uuid:pk>/', ProgramUpdateView.as_view()),
]
