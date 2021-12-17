"""z_diary_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

import account_book_app.views
import common_app.views

urlpatterns = [
    # ADMIN
    path('admin/', admin.site.urls),

    # common_app
    path('', common_app.views.index),
    path('login/', common_app.views.login),
    path('logout/', common_app.views.logout),

    # account_book
    path('account_book/', account_book_app.views.show_contents),
    path('account_book/add_account/', account_book_app.views.add_account),
    path('account_book/del_account/', account_book_app.views.del_account),
    path('account_book/add_category/', account_book_app.views.add_category),
    path('account_book/del_category/', account_book_app.views.del_category),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)