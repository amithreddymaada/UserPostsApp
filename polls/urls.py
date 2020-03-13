from django.urls import path
from django.contrib import admin
from . import views

app_name='polls'
urlpatterns=[
    path('',views.IndexView.as_view(),name='index'),
    path('<int:pk>/',views.DetailsView.as_view(),name='details'),
    # path('<int:id>/',views.details,name='details'),
    path('<int:pk>/results/',views.ResultView.as_view(),name='results'),
    path('<int:id>/vote/',views.vote,name='vote'),

    # path('<int:id>/',views.details,name='details'),
    # path('<int:id>/results/',views.results,name='results'),

]


admin.AdminSite.site_header="Polls Administration"