from django.urls import path
from characteristic import views

urlpatterns = [
    path('brand/', views.CreateBrandView.as_view(), name='create_brand'),
    path('update/brand/<slug:slug>/', views.UpdateBrandView.as_view(), name='update_brand'),
    path('delete/brand/<slug:slug>/', views.DeleteBrandView.as_view(), name='delete_brand'),

    path('feature/', views.CreateFeatureView.as_view(), name='create_feature'),
    path('update/feature/<slug:slug>/', views.UpdateFeatureView.as_view(), name='update_feature'),
    path('delete/feature/<slug:slug>/', views.DeleteFeatureView.as_view(), name='delete_feature'),

    path('subfeature/', views.CreateSubFeatureView.as_view(), name='create_sub_feature'),
    path('update/subfeature/<slug:slug>/', views.UpdateSubFeatureView.as_view(), name='update_sub_feature'),
    path('delete/subfeature/<slug:slug>/', views.DeleteSubFeatureView.as_view(), name='delete_sub_feature'),

    # path('subfeature/', UpdateSubFeatureView.as_view(), name='create_sub_feature'),

    path('all/', views.ListCharacteristicsView.as_view(), name='list-characteristic'),

]
