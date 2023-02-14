from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('user_manager.urls')),
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
]
