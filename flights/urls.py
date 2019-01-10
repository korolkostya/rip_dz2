from django.urls import path
from . import views


urlpatterns = [
    path('', views.FlightListView.as_view(), name='list'),
    path('mine/', views.FlightMineListView.as_view(), name='mine'),

    path('<int:pk>/', views.FlightDetailView.as_view(), name='get'),
    path('create/', views.FlightCreateView.as_view(), name='create'),
    path('edit/<int:pk>/', views.FlightUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.FlightDeleteView.as_view(), name='delete'),

    path('add/<int:pk>/', views.AddToBookingsView.as_view(), name='add'),

]