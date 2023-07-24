# from django.test import SimpleTestCase
# from django.urls import reverse,resolve
# from users.views import login_api, get_user_data, register_api, register_product_api, getProducts, product_gud

# class TestUrls(SimpleTestCase):
    
#     def test_login_api(self):
#         url = reverse('login')
#         # print(resolve(url))
#         self.assertEquals(resolve(url).func, login_api)

#     def test_user(self):
#         url = reverse('user')
#         self.assertEquals(resolve(url).func, get_user_data)

#     def test_register_api(self):
#         url = reverse('register')
#         self.assertEquals(resolve(url).func, register_api)

#     def test_register_product_api(self):
#         url = reverse('register_product')
#         self.assertEquals(resolve(url).func, register_product_api)

#     def test_getProducts(self):
#         url = reverse('products')
#         self.assertEquals(resolve(url).func, getProducts)

#     def test_prod_gud(self):
#         url = reverse("product_gud", args = ['some-pk'])
#         self.assertEquals(resolve(url).func, product_gud)