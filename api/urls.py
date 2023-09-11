from home.views import index,person,login,personAPI,PersonViewSet,RegisterAPI
from django.urls import path,include
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'people', PersonViewSet,basename='people')
urlpatterns=router.urls


urlpatterns = [
    path('index/', index),
    path('person/', person),
    path('login/', login),
    path('persons/', personAPI.as_view()),
    path('register/', RegisterAPI.as_view()),
    path('', include(router.urls)),


]