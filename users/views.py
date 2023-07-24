from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.auth import AuthToken
from rest_framework import status
from .serializers import RegisterSerializer, ProductSerializer, OrderSerializer, OrderItemSerializer, OrderDetails
# from .products import products
from .models import Product, Order, OrderItem

from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.views.decorators.cache import cache_page
from django.core.cache import cache

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)


@api_view(['POST'])
def login_api(request):
    serializer = AuthTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data['user']
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email':user.email
        },
        'token': token,
        'message': 'Logged in'
    
    })

@api_view(['GET'])
def get_user_data(request):
    user = request.user

    if user.is_authenticated:
        return Response({
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            },
        })
    
    return Response({'error': 'not authenticated'}, status=400)

@api_view(['POST'])
def register_api(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = serializer.save()
    _, token = AuthToken.objects.create(user)

    return Response({
        'user_info': {
            'id': user.id,
            'username': user.username,
            'email':user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        },
        'token': token,
        'message': 'Success'
    })

@api_view(['POST'])
def register_product_api(request):
    serializer = ProductSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    product = serializer.save()
    # _, token = AuthToken.objects.create(product)

    return Response({
        'product_info': {
            # 'id': product.id,
            'name': product.name
        },
        # 'token': token
    })

@api_view(['GET'])
def getProducts(request):
    products=Product.objects.all()
    serializer=ProductSerializer(products,many=True)
    return Response(serializer.data)


    
@api_view(['GET', 'PUT', 'DELETE'])
def product_gud(request, pk):

    try:
        product = Product.objects.get(id=pk)
        # product_id = request.GET.get(id=pk)
        # if cache.get(product_id):
        #     print("data from Caching")
        #     product = Product.objects.get(product_id)
        # else:
        #     if product_id:
        #         # prod = Product.objects.get(id=pk)
        #         product = Product.objects.get(product_id)
        #         cache.set(product_id, pk )
        #     else:
        #         product=Product.objects.get(id=pk)


    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = ProductSerializer(product, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        operation = product.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)


    
@api_view(['POST'])
def register_order_api(request):
    serializer = OrderSerializer(data=request.data)
    itemserializer = OrderItemSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    itemserializer.is_valid(raise_exception=True)
    order = serializer.save()
    orderitem = itemserializer.save(order_id=order)
    # _, token = AuthToken.objects.create(product)

    return Response({
        'order_info': {
        "status" : order.status,
        "user_id": order.user_id.id,
        "date_placed": order.date_placed,
        "order_id": order.id,
        "quantity": orderitem.quantity,
        "product_id": orderitem.product_id.id
        },
        # 'token': token
    })
    

@api_view(['GET'])
def getOrders(request):
    order_data = []
    orders=Order.objects.all()
    serializer = OrderSerializer(orders,many=True)
    # import pdb;pdb.set_trace()
    for order in serializer.data:
        # items = OrderItem.objects.all()
        # orderitemserializer=OrderItemSerializer(items,many=True)
        items = OrderItem.objects.get(order_id=order["id"])
        orderitemserializer=OrderItemSerializer(items)
        itemsdata = orderitemserializer.data
        order_data.append({
            "order_id": order["id"],
            "status" : order["status"],
            "user_id": order["user_id"],
            "date_placed": order["date_placed"],
            "quantity": itemsdata["quantity"],
            "product_id": itemsdata["product_id"]
            })
    return Response({"orders": order_data})
    


@api_view(['GET', 'PUT', 'DELETE'])
def order_gud(request, pk):

    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = OrderSerializer(order, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data["success"] = "update successful"
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == "DELETE":
        operation = order.delete()
        data = {}
        if operation:
            data["success"] = "delete successful"
        else:
            data["failure"] = "delete failed"
        return Response(data=data)