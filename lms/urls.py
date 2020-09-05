from django.urls import path
from lms.views import index,about,blog,event,cart,checkout,detail,onended,allcourses,mycourses,CourseDetail,\
enrol,BlogView,ArticleDetailView,InterviewQuestionsView,InterviewQuestionsDetail,bootcamps,contact_us,signup
from authentication.views import profile

app_name = 'lms'

urlpatterns = [
    path('',index,name = 'index'),
    path('about/',about,name = 'about'),
    path('course/<slug:slug>/',CourseDetail,name = 'coursedetail'),
    path('allcourses/',allcourses,name = 'allcourses'),
    path('mycourses/',mycourses,name = 'mycourses'),
    path('contact_us/',contact_us,name = 'contact_us'),
    path('event/',event,name = 'event'),
    path('cart/',cart,name = 'cart'),
    path('checkout/<slug:slug>/',checkout,name = 'checkout'),
    path('detail/<slug:slug>/',detail.as_view(),name = 'detail'),
    path('ajax/onended/',onended,name = 'onended'),
    path('ajax/staus/',enrol,name = 'status'),
    path('blog/',BlogView.as_view(),name = 'blog'),
    path('blog/article/<slug:slug>',ArticleDetailView.as_view(),name = 'article-detail'),
    path('interview-questions/',InterviewQuestionsView.as_view(),name= 'interview-questions'),
    path('interview-questions/<slug:slug>', InterviewQuestionsDetail.as_view(), name = 'interview-detail'),
    path('bootcamps/', bootcamps,name = 'bootcamps'),
    path('signup/',signup,name = 'signup')
]