from rest_framework import routers

from . import views

app_name = 'rates'

rates_router = routers.DefaultRouter()
rates_router.register('', views.RateViewSet, basename='rates')
urlpatterns = rates_router.urls
