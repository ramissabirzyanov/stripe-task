from django.urls import path
from payment_app.order import views
from payment_app.item.views import ItemListView, ItemDetailView


urlpatterns = [
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<int:order_pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:order_pk>/add/item/', ItemListView.as_view(), name='add'),
    path('<int:order_pk>/add/item/<int:item_id>/', ItemDetailView.as_view(), name='add_item_to_order'),
    path('<int:order_pk>/add/item/<int:item_id>/submit/', views.AddItemToOrderView.as_view(), name='submit_order'),
    path('buy/<int:order_pk>/', views.BuyOrderView.as_view(), name='buy_order'),
    path('buy/<int:order_pk>/success/', views.PaymentSuccessView.as_view(), name='payment_success'),
    path('buy/<int:order_pk>/cancel/', views.PaymentCancelView.as_view(), name='payment_cancel'),
]
