"""odop_backend URL Configuration

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
from django.urls import path, include
from django.conf.urls.static import static
from odop_backend import settings

from user.urls import router as userRouter

from django.shortcuts import render
def view(request):
    return render(request, "otp_email_template.html", context={
        "date": "12th Aug, 2012",
        "username": "Dhruv Lohar",
        "generated_otp": "123534"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("view/", view),
    
    path('user/', include(userRouter.urls)),
]

if settings.DEBUG:
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIR)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)