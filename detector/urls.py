from django.urls import path
from django.conf.urls import url
from .views import *


urlpatterns = [
    url(r'^register/', UserRegistrationView.as_view()),
    url(r'^movie/rating', MovieRating.as_view()),

]