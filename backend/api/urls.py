from django.urls import include, path
from rest_framework import routers

from bicycles.views import BicycleViewSet, FinishRentView, RentView
from users.views import GetTokenView, UserRegView, UserViewSet

app_name = 'api'

router_v1 = routers.DefaultRouter()
router_v1.register('users', UserViewSet, basename='user')
router_v1.register('bicycles', BicycleViewSet, basename='bicycle')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('signup/', UserRegView.as_view(), name='auth_signup'),
    path('token/', GetTokenView.as_view(), name='token'),
    path('finish/<int:bicycle_nr>/', FinishRentView.as_view(),
         name='finish_rent'),
    path('rent/<int:bicycle_nr>/', RentView.as_view(),
         name='start_rent'),
]
