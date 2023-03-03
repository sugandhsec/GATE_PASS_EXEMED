from django.urls import path
from . import views
urlpatterns = [
    path('',views.index,name='index'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('rgp_signup/',views.rgp_signup,name='rgp_signup'),
    path('nrgp_signup/',views.nrgp_signup,name='nrgp_signup'),
    path('back/',views.back,name='back'),
    path('rgp_search/',views.rgp_search,name='rgp_search'),
    path('rgp_view/',views.rgp_view,name='rgp_view'),
    path('rgp_view_operator/',views.rgp_view_operator,name='rgp_view_operator'),
    path('rgp_exit/<int:pk>',views.rgp_exit,name='rgp_exit'),
    path('change_password/',views.change_password,name='change_password'),
    path('new_password/',views.new_password,name='new_password'),
    path('rgp_print/<int:pk>',views.rgp_print,name='rgp_print'),
    path('nrgp_view/',views.nrgp_view,name='nrgp_view'),
    path('rgp_all/',views.rgp_all,name='rgp_all'),
    path('nrgp_all/',views.nrgp_all,name='nrgp_all'),
    path('nrgp_print/<int:pk>',views.nrgp_print,name='nrgp_print'),
    path('rgp_outward/',views.rgp_outward,name='rgp_outward'),
    path('rgp_inward/',views.rgp_inward,name='rgp_inward'),
    path('nrgp_outward/',views.nrgp_outward,name='nrgp_outward'),
    path('nrgp_view_operator/',views.nrgp_view_operator,name='nrgp_view_operator'),
    path('<id>/update', views.update_view ),
    # path('<id>/update', views.update_view_nrgp ),
   

   
    path('send_email/<int:pk>',views.send_email,name='send_email'),
    path('ajax/validate_email/',views.validate_email,name='validate_email'),
 
  
    path('log_print/<int:pk>',views.log_print,name='log_print'), 
]