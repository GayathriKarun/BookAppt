from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import DoctorBlogsView,PatientBlogsView,DetailBlogView,CreateBlogView, \
        ProfileView, DoctorsListView, BookApptView, ApptConfirmView


urlpatterns = [
    path('', PatientBlogsView, name='patientblogs'),
    path('profile/<int:userid>/', ProfileView, name='profile'),
    path('<int:userid>/', DoctorBlogsView, name='doctorblogs'),
    path('detail/<int:blogid>/', DetailBlogView, name='detail'),
    path('create/<int:userid>/', CreateBlogView, name='create'),
    path('doctorslist/', DoctorsListView, name='doctorslist'),
    path('bookappt/<int:doctorid>/', BookApptView.as_view(), name='bookappt'),
    path('apptconfirm/<int:apptid>/', ApptConfirmView, name='apptconfirm'),

] + static(settings.MEDIA_URL_1, document_root=settings.MEDIA_ROOT_1)