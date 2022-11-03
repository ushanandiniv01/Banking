"""Banking_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from bank.views import signupaction
from bank.views import loginaction
from bank.views import deposit_amount
from bank.views import bal_inq
from bank.views import money_transfer
from bank.views import m_passbook
from bank.views import home_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/',signupaction),
    path('login/',loginaction),
    path('deposit/',deposit_amount),
    path('balinq/',bal_inq),
    path('money/',money_transfer),
    path('passbook/',m_passbook),

    path('',home_page)
]
