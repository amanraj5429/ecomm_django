from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_api),
    path('user/', views.get_user_data),
    path('register/', views.register_api),
    path('register_product/', views.register_product_api),
    path('products/', views.getProducts),
    path('products/<str:pk>',views.product_gud,name="product_gud"),
    path('orders/', views.register_order_api),
    path('all_orders/', views.getOrders),
    path('all_orders/<str:pk>', views.order_gud)

]
