import stripe
from typing import Any
from django import views
from django.views.generic import DetailView, TemplateView
from django.conf import settings
from django.http import JsonResponse, HttpRequest
from django.shortcuts import get_object_or_404
from payment_app.item.models import Item
import logging


logger = logging.getLogger(__name__)

stripe.api_key = settings.STRIPE_SECRET_KEY


class BuyItemView(views.View):
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
        item_id = self.kwargs.get('id')
        item = get_object_or_404(Item, id=item_id)
        quantity = self.request.GET.get('quantity', 1)
        try:
            stripe_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {'name': item.name},
                        'unit_amount': int(item.price * 100),
                    },
                    'quantity': quantity,
                }],
                mode='payment',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
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

        except Exception as e:
            logger.exception(f"Unexpected error: {str(e)}")
            return JsonResponse(
                {'error': 'Internal server error'},
                status=500
            )


class ItemDetailView(DetailView):
    """Представление для отображения деталей товара."""
    model = Item
    template_name = 'item/item_detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Добавляет публичный ключ Stripe в контекст шаблона.

        Возвращает словарь вида:
        {str: Any}
        """
        context = super().get_context_data(**kwargs)
        context["STRIPE_PUBLIC_KEY"] = settings.STRIPE_PUBLIC_KEY
        return context


class PaymentSuccessView(TemplateView):
    """Представление для страницы успешной оплаты."""
    template_name = 'item/success.html'


class PaymentCancelView(TemplateView):
    """Представление для страницы отмены оплаты."""
    template_name = 'item/cancel.html'
