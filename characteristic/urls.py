from django.urls import path
from characteristic.views import CreateFeatureView, CreateBrandView, CreateSubFeatureView, ListCharacteristicsView

urlpatterns = [
    path('brand/', CreateBrandView.as_view(), name='create_brand'),
    path('feature/', CreateFeatureView.as_view(), name='create_feature'),
    path('subfeature/', CreateSubFeatureView.as_view(), name='create_sub_feature'),



    path('all/', ListCharacteristicsView.as_view(), name='list-characteristic'),


]
