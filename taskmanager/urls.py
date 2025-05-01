from django.contrib import admin
from django.urls import path, include
from tasks.views import task_list  # Add this import

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('', task_list, name='task-list'),  # Add this line
]