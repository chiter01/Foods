from django.db import models
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
class Category(models.Model):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=250, unique=True)

    def __str__(self):
        return f'{self.name}'


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь", related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Корзина {self.user.first_name}"

    def is_empty(self):
        return not self.items.exists()
    
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

    @property
    def price(self):
        return self.product.price



class Food(models.Model):
    
    class Meta:
        verbose_name = 'Еда'
        verbose_name_plural = 'Еды'
    
    name = models.CharField('название', max_length=50)
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


class Order(models.Model):
    DELIVERY_CHOICES = [
        ('delivery', 'Доставка'),
        ('pickup', 'Самовывоз'),
    ]
    
    PAYMENT_CHOICES = [
        ('online', 'Оплата онлайн'),
        ('card', 'Курьеру картой'),
        ('cash', 'Наличные'),
    ]
    
    DELIVERY_TIME_CHOICES = [
        ('soon', 'В ближайшее время'),
        ('time', 'Ко времени'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    name = models.CharField(max_length=100, verbose_name="Имя")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    delivery_type = models.CharField(max_length=10, choices=DELIVERY_CHOICES, verbose_name="Тип доставки")
    address_street = models.CharField(max_length=255, blank=True, null=True, verbose_name="Улица")
    address_house = models.CharField(max_length=10, blank=True, null=True, verbose_name="Дом")
    address_apartment = models.CharField(max_length=10, blank=True, null=True, verbose_name="Квартира/офис")
    address_floor = models.CharField(max_length=10, blank=True, null=True, verbose_name="Этаж")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, verbose_name="Метод оплаты")
    delivery_time = models.CharField(max_length=10, choices=DELIVERY_TIME_CHOICES, verbose_name="Время доставки")
    specific_time = models.TimeField(blank=True, null=True, verbose_name="Указанное время")
    person_count = models.PositiveIntegerField(default=1, verbose_name="Количество персон")
    callback_needed = models.BooleanField(default=False, verbose_name="Нужен звонок")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} - {self.name}"