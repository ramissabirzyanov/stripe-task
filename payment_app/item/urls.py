from payment_app.item import views
from django.urls import path

urlpatterns = [
    path('', views.ItemListView.as_view(), name='item_list'),
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
]
