from django.urls import path
from .views import ProductViews, OrderViews

urlpatterns = [
    path('product', ProductViews.as_view({"get": "get_product",
                                                "post": "post_product",
                                                "patch": "update_product",
                                                "delete": "delete_product"})),
    path('order', OrderViews.as_view({"get": "get_order",
                                                "post": "post_order",
                                                "patch": "update_order",
                                                "delete": "delete_order"})),
]