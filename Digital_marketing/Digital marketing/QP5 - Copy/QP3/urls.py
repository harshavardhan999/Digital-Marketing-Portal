"""QP3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path
from Q_app import views
from django.conf.urls.static import static
from django.conf import settings 


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('login/',views.login,name='login'),
    path('forgotpassword/',views.forgotpassword),
    path('piechat/',views.piechart,name='piechart'),
    path('homepage/',views.homepage,name='homepage'),
    path('userhomepage/',views.userhomepage,name='userhomepage'),
    
    path('clientform/',views.upload_image,name='clientform'),
    path('taskcreation/',views.taskcreation,name='taskcreation'),
    path('u_report/',views.u_report,name='report'),
    
    path('viewclientdetails/',views.viewclientdetails,name='viewclientdetails'),
    path('edit_client1/<int:id>',views.edit_client1),
    path('update_client/<int:id>',views.update_client,name='update_client'),
    path('delete_client/<int:id>',views.delete_client),
    

    path('taskdata/',views.taskdata,name='taskdata'),
    path('delete/<int:id>',views.delete),
    path('edit/<int:id>',views.edit),
    path('update/<int:id>',views.update),
    path('client1',views.client1,name='client1'),
    path('reportdata/',views.reportdata,name='reportdata'),
    path('delete_report/<int:id>',views.delete_report),
    path('edit_report/<int:id>',views.edit_report),
    path('update_report/<int:id>',views.update_report,name='update_report'),
    path('client1/<int:id>/',views.client1, name='client1'),
    #path('new',views.new),
    #path('edit_client/<int:id>',views.edit_client),
    #path('viewclient',views.viewclient),
    #path('newlogin',views.newlogin),
    
    #path('edit_client1/<int:id>',views.edit_client1),
    
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

'''
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$',serve,
        {'document_root':settings.MEDIA_ROOT})]

'''

