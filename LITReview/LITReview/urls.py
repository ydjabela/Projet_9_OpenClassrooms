"""LITReview URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path
import authentification.views
import blog.views
from django.conf import settings
from django.conf.urls.static import static

# ---------------------------------------------------------------------------------------------------------------------#

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', authentification.views.login_page, name='login'),
    path('logout/', authentification.views.logout_user, name='logout'),
    path('inscription/', authentification.views.inscription, name='inscription'),
    path('home/', blog.views.home, name='home'),
    path('creatreview/<int:pk>', blog.views.creatreview, name='creatreview'),
    path('post/', blog.views.post, name='post'),
    path('deletepost/<str:pk>', blog.views.deletepost, name='deletepost'),
    path('modifiepost/<int:pk>/post/<int:id_post>', blog.views.modifiepost, name='modifiepost'),
    path('deleteticket/<str:pk>', blog.views.deleteticket, name='deleteticket'),
    path('modifieticket/<str:pk>', blog.views.modifieticket, name='modifieticket'),
    path('abonnements/', blog.views.abonnements, name='abonnements'),
    path('desabonnement/<str:pk>', blog.views.desabonnement, name='desabonnement'),
    path('add_tickets/', blog.views.add_tickets, name='add_tickets'),
    path('add_critique/', blog.views.add_critique, name='add_critique'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
