from django.urls import include, path
from rest_framework import routers

from . import views
router = routers.DefaultRouter()


urlpatterns = [
    path('', include(router.urls)),
    path('encode',views.model_encode),
     path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('admin/', admin.site.urls,name="admin"),
]