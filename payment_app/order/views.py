import logging
from typing import Any

import stripe
from django.views import View
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from django.db import transaction
from django.urls import reverse

from payment_app.order.models import Order, OrderItem
from payment_app.item.models import Item


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class AddItemToOrderView(View):
    def post(self, request, *args, **kwargs):
        item_id = self.kwargs.get('item_id')
        order_pk = self.kwargs.get('order_pk')
        item = get_object_or_404(Item, id=item_id)
        quantity = int(request.POST.get('quantity', 1))
        with transaction.atomic():
            order = get_object_or_404(Order, id=order_pk)

            OrderItem.objects.create(
                order=order,
                item=item,
                quantity=quantity
            )
            order.calculate_total_price()
            order.save()
        return redirect('order_detail', order_pk=order.id)


class BuyOrderView(View):
    """Представление для создания платёжной сессии Stripe."""

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> JsonResponse:
        """
        Обрабатывает GET-запрос для создания платёжной сессии.

        Аргументы:
            request: Объект HTTP-запроса
            *args: Произвольные позиционные аргументы
            **kwargs: Произвольные именованные аргументы

        Возвращает:
            JsonResponse: Содержит ID сессии Stripe или сообщение об ошибке
        """
        order_id = self.kwargs.get('order_pk')
        order = get_object_or_404(Order, id=order_id)
        try:
            line_items = []
            for order_item in order.item_in_order.all():
                line_items.append({
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': order_item.item.id},
                        'unit_amount': int(order_item.item.price * 100),
                    },
                    'quantity':order_item.quantity,
                })
            stripe_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=line_items,
                mode='payment',
                success_url = request.build_absolute_uri(reverse('payment_success', args=[order.id])),
                cancel_url = request.build_absolute_uri(reverse('payment_cancel', args=[order.id]))
            )

            logger.info(f"Stripe session created: {stripe_session.id}")
            return JsonResponse({
                'stripe_session_id': stripe_session.id
            })

        except stripe.error.StripeError as e:
            logger.error(f"Unexpected error creating session: {e.user_message}")
            return JsonResponse(
                {'error': f'Error creating checkout session: {e.user_message}'},
                status=400
            )

        except Exception:
            logger.exception("Unexpected error")
            return JsonResponse(
                {'error': 'Internal server error'},
                status=500
            )


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        order_pk = self.kwargs.get('order_pk')
        return get_object_or_404(Order, pk=order_pk)

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Добавляет публичный ключ Stripe в контекст шаблона.
        Возвращает словарь.
        """
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'

    def post(self, request):
        with transaction.atomic():
            order = Order.objects.create()
            return redirect('order_detail', order_pk=order.id)


class PaymentSuccessView(TemplateView):
    """Представление для страницы успешной оплаты."""
    template_name = 'order/success.html'


class PaymentCancelView(TemplateView):
    """Представление для страницы отмены оплаты."""
    template_name = 'order/cancel.html'
