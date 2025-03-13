"""
URL configuration for lotokbank project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from banklotkov.views import (
    signup, lk_view, logout_view, CustomLoginView, thanks_view,
    product_list_view, product_detail_view as pdv, home_page,
    purchase_product, balance_request, transaction_history,
    new_loan, edit_profile, add_review, add_product_view
)

urlpatterns = [
    # path('', home_page, name='home'),
    path('',  product_list_view, name='product_list'),
    path('admin/', admin.site.urls),
    path('signup/', signup, name='signup'),
    path('lk/', lk_view, name='lk'),
    path('logout/', logout_view, name='logout'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('thanks/', thanks_view, name='thanks'),
    path('products/', product_list_view, name='product_list'),
    path('products/add/', add_product_view, name='add_product'),
    path('products/<int:product_id>/', pdv, name='product_detail'),
    path('products/<int:product_id>/add_review/', add_review, name='add_review'),
    path('products/<int:product_id>/purchase/', purchase_product, name='purchase_product'),
    path('loan/<int:loan_id>/repay/', purchase_product, name='repay_loan'),
    path('balance-request/', balance_request, name='balance_request'),
    path('transaction-history/', transaction_history, name='transaction_history'),
    path('new-loan/', new_loan, name='new_loan'),
    path('edit-profile/', edit_profile, name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)