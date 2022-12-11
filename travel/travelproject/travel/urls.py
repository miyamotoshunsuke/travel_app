from django.urls import path
from . import views
urlpatterns = [
    path('', views.index_view, name='index'),
    path('travel/', views.ListTravelView.as_view(), name='list-travel'),
    path('travel/<int:pk>/detail/', views.DetailTravelView.as_view(), name='detail-travel'),
    path('travel/create/', views.CreateTravelView.as_view(), name= 'create-travel'),
    path('travel/<int:pk>/delete/', views.DeleteTravelView.as_view(), name='delete-travel'),
    path('travel/<int:pk>/update/', views.UpdateTravelView.as_view(), name='update-travel'),
    path('travel/<int:travel_id>/review/', views.CreateReviewView.as_view(), name='review'),
]