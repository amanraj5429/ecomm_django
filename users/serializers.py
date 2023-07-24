from django.contrib.auth.models import User
from rest_framework import serializers, validators
from users.models import Product, Order, OrderItem

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name', 'last_name')

        extra_kwargs = {
            "password": {"write_only": True},
            "email": {
                "required": True,
                "allow_blank": False,
                "validators": [
                    validators.UniqueValidator(
                        User.objects.all(), "A user with that Email already exists"
                    )
                ]
            },
            "first_name":{"allow_blank": True},
            "last_name":{"allow_blank": True},
        }


    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')    
        email = validated_data.get('email')    
        first_name = validated_data.get('first_name')    
        last_name = validated_data.get('last_name') 

        user = User.objects.create(
            username=username,
            password=password,
            email = email,
            first_name = first_name,
            last_name = last_name
        )

        return user   
    
class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=200)
    price = serializers.IntegerField()
    

    
    class Meta:
        model = Product
        fields = ('__all__')

    def create(self, validated_data):
        name = validated_data.get('name')
        description = validated_data.get('description')
        price = validated_data.get('price')
        # date_created = validated_data('date_created')
        # date_updated = validated_data('date_updated')

        product = Product.objects.create(
            # id = id,
            name = name,
            description = description,
            price = price
            # date_created = date_created,
            # date_updated = date_updated
        )
        return product
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id','date_placed', 'status', 'user_id')

    def create(self, validated_data):
        id = validated_data.get('id')
        date_placed = validated_data.get('date_placed')
        status = validated_data.get('status')
        user_id = validated_data.get('user_id')
        # date_created = validated_data('date_created')
        # date_updated = validated_data('date_updated')

        order = Order.objects.create(
            id = id,
            date_placed = date_placed,
            status = status,
            user_id = user_id
            # date_created = date_created,
            # date_updated = date_updated
        )
        return order
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order_id', 'product_id', 'quantity')

    def create(self, validated_data):
        order_id = validated_data.get('order_id')
        product_id = validated_data.get('product_id')
        quantity = validated_data.get('quantity')
        


        orderitem = OrderItem.objects.create(
            order_id = order_id,
            product_id = product_id,
            quantity = quantity
        )
        return orderitem
    

class OrderDetails(serializers.ModelSerializer):
    user_id = OrderSerializer()

    class Meta:
        model = OrderItem
        fields = ('product_id', 'quantity', 'order_id', 'user_id')

