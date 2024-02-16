from django.contrib import admin
from django.urls import path, include
from web_tool import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('web_tool/', include('web_tool.urls'))#用來新增管理網址
]
