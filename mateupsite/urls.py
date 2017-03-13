from django.conf.urls import url, include
from mateupsite import views
urlpatterns = [
    url(r'^$', views.IndexPageView.as_view(), name='index'),
	url(r'^match', views.MatchPageView.as_view(), name='match'),
    url(r'^register/', views.RegisterPageView.as_view(), name='register'),
]