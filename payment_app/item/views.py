from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404

from payment_app.item.models import Item


class ItemDetailView(DetailView):
    """Представление для отображения деталей товара."""
    model = Item
    template_name = 'item/item_detail.html'
    context_object_name = 'item'
    
    def get_object(self):
        item_id = self.kwargs.get('item_id')
        return get_object_or_404(Item, id=item_id)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_pk'] = self.kwargs.get('order_pk')
        return context

class ItemListView(ListView):
    model = Item
    template_name = 'item/item_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order_pk'] = self.kwargs.get('order_pk')
        return context
