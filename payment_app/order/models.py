from django.db import models
from payment_app.item.models import Item


class Order(models.Model):
    """Модель Order"""
    
    items = models.ManyToManyField(Item, through='OrderItem', related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def calculate_total_price(self):
        """
        Подсчет общей суммы всего заказа.
        """
        total = sum(item.get_item_price() for item in self.item_in_order.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id}: {self.total_price}"

    def get_items(self):
        return ",".join([str(item) for item in self.items.all()])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='item_in_order', on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name='orders_with_item', on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)

    def get_item_price(self):
        """
        Подсчет итоговой стоимости конкретной позиции(item).
        """
        return self.item.price * self.quantity
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.order.calculate_total_price()
