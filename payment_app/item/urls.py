from payment_app.item import views
from django.urls import path

urlpatterns = [
    path('item/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('buy/<int:id>/', views.BuyItemView.as_view(), name='buy_item'),
    path('success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
]
