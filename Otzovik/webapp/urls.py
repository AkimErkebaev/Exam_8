from django.urls import path

from webapp.views import IndexView, CreateReview, UpdateView, DeleteView, IndexViewProducts, CreateProduct, \
    ProductView, UpdateProduct, DeleteProduct

app_name = "webapp"

urlpatterns = [
    path('', IndexViewProducts.as_view(), name="index_product"),
    path('projects/add/', CreateProduct.as_view(), name="create_product"),
    path('project/<int:pk>/', ProductView.as_view(), name="product_view"),
    path('reviews/', IndexView.as_view(), name="index"),
    path('reviews/add/', CreateReview.as_view(), name="create_review"),
    path('review/<int:pk>/update', UpdateView.as_view(), name="update_review"),
    path('review/<int:pk>/delete', DeleteView.as_view(), name="delete_review"),
    path('project/<int:pk>/update', UpdateProduct.as_view(), name="update_product"),
    path('project/<int:pk>/delete', DeleteProduct.as_view(), name="delete_product"),
]
