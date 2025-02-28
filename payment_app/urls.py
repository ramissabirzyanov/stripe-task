from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('order/', include('payment_app.order.urls')),
    path('item/', include('payment_app.item.urls')),
]
