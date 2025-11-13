from django.db import models
from django.contrib.auth.models import User
from todolist.models import UserProfile


class ShopItem(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    cost = models.IntegerField(default=0)
    image = models.ImageField(upload_to='shop_items/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.cost} pts"

class Purchase(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(ShopItem, on_delete=models.CASCADE)
    purchased_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} bought {self.item.name}"
