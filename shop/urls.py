from django.conf.urls import url
from . import views
from django.urls import path, re_path, include

app_name = 'shop'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('parts/', views.ProductListView.as_view(), name='Parts'),
    path('parts/<int:id>/',views.product_detail,name='product_detail'),
    path('categories/',views.CategorylistView.as_view(), name='categories'),
    path('categories/<int:id>',views.category_detail.as_view(),name='category_detail'),
    path('edit/', views.profile, name='profile'),
    path('newsletter/', include('newsletter.urls')),
]
