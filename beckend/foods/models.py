from django.db import models

class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'

from django.conf import settings

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина {self.user.first_name}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name="Корзина", related_name="items")
    product = models.ForeignKey('foods.Food', on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return f"{self.product.name} - {self.quantity} шт."

    def total_price(self):
        return self.product.price * self.quantity

class Food(models.Model):
    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еды'
    name = models.CharField('название', max_length=50, unique=True)
    description = models.CharField('описание', max_length=400, help_text='Просто описание')
    price = models.DecimalField('цена', max_digits=10, decimal_places=2, default=0)
    is_published = models.BooleanField('публичность', default=True)
    image = models.ImageField('выберите изобрежение', upload_to='images/')
    category = models.ForeignKey('foods.Category', models.PROTECT, verbose_name='категория',help_text='Выберите категорию')
    user = models.ForeignKey('account.User', on_delete=models.CASCADE, verbose_name='пользователь')
    proteins = models.CharField(verbose_name="Белки (г)", max_length=50) 
    fats = models.CharField(verbose_name="Жиры (г)", max_length=50)
    carbohydrates = models.CharField(verbose_name="Углеводы (г)", max_length=50)
    calories = models.CharField(verbose_name="Ккал", max_length=50)
    weight = models.CharField(verbose_name="Вес (г)", max_length=50)
    def __str__(self):
        return self.name