from rest_framework import serializers
from foods.models import Food, Category, Cart, CartItem, Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class FoodSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )

    class Meta:
        model = Food
        fields = '__all__'
class CartItemSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='cart.user.username', read_only=True)
    price = serializers.ReadOnlyField(source='product.price')
    total_price = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'cart', 'user_username', 'price', 'total_price']

    def create(self, validated_data):
        validated_data.pop('user_username', None)
        return CartItem.objects.create(**validated_data)


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'created_at', 'items', 'total_price']
