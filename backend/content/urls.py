from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import *
 
from rest_framework.routers import DefaultRouter
from .views import PageViewSet, PageView

router = DefaultRouter()
router.register(r'pages', PageViewSet, basename='page-viewset')  
router.register(r'page-details', PageView, basename='page-view') 
router.register(r'sections', SectionViewSet,basename='sections')
router.register(r'modules', ModuleViewSet,basename='modules')
router.register(r'links', LinksViewSet,basename='links')

# urlpatterns = router.urls
 


urlpatterns = [
    path('setting-view/', SettingView.as_view(), name='setting-view'),
    path('update-section-order/', UpdateSectionOrderView.as_view(), name='update-section-order'),
    path('update-module-order/', UpdateModuleOrderView.as_view(), name='update-module-order'),
    path('sections/<int:pk>/clone/', CloneSectionView.as_view({'post': 'create'}), name='section-clone'),
    path('modules/active-state/', ActiveStateView.as_view(), name='active-state'),
    path('add-module-to-page/', AddModuleToPage.as_view(), name='add-module-to-page'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('page-link/<int:pk>/', PageLinksView.as_view(), name='page-link'),



   
    


    
 
]

# Include the router URLs
urlpatterns += router.urls







 