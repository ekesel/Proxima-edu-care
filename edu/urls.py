from django.urls import include, path
from . import views
from django.conf.urls.static import static
from django.conf import settings 
from django.contrib.auth import views as auth

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/",views.signup,name="signup"),
    path("reg_tutor/", views.reg_tutor, name="reg_tutor"),
    path("reg_college/", views.reg_college, name="reg_college"),
    path("coursesearch/", views.coursesearch, name="coursesearch"),
    path("collegesearch/",views.collegesearch, name="collegesearch"),
    path("profilecollege/<int:id>",views.profilecollege,name="profilecollege"),
    path("tutorsearch/", views.tutorsearch, name="tutorsearch"),
    path("profiletutor/<int:id>",views.profiletutor,name="profiletutor"),
    path("profilecourse/<int:id>",views.profilecourse,name="profilecourse"),
    path("loginenroll/",views.loginenroll,name="loginenroll"),
    path("opencourse/<int:id>",views.opencourse,name="opencourse"),
    path("reg_school/",views.reg_school,name="reg_school"),
    path("success/<int:who>",views.success,name="success"),
    path("schoolsearch/",views.schoolsearch,name="schoolsearch"),
    path("profileschool/<int:id>",views.profileschool,name="profileschool"),
    path("sell/",views.sell,name="sell"),
    path("buy/",views.buy,name="buy"),
    path("profilebook/<int:id>",views.profilebook,name="profilebook"),
    path("sharespace/",views.sharespace,name="sharespace"),
    path("needspace/",views.needspace,name="needspace"),
    path("profilespace/<int:id>",views.profilespace,name="profilespace"),
    path("contact/",views.contact,name="contact"),
    path("about/",views.about,name="about"),
    path("reg_institute/",views.reg_institute,name="reg_institute"),
    path("institutesearch/",views.institutesearch,name="institutesearch"),
    path("profileinstitute/<int:id>",views.profileinstitute,name="profileinstitute"),
    path('login/',views.login,name="login"),
    path('logout/',auth.LogoutView.as_view(template_name='login.html'),name='logout'),
    path('enrolldetails/',views.enrolldetails,name='enrolldetails'),
]