from django.db import models


class Item(models.Model):
    
    name = models.CharField(unique=True, max_length=10, verbose_name='name')
    description = models.TextField(verbose_name='description')
    price = models.DecimalField(max_digits=20, decimal_places=3, verbose_name='price')

    class Meta:
        db_table = 'Item'
        ordering = ['id']
        verbose_name = 'Item'
    
    def __str__(self):
        return f"{self.name}: {self.price}"
