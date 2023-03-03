from django.shortcuts import render, redirect, get_object_or_404
from .forms import BlogForm, BookingForm
from django.urls import reverse
from .models import Blog, Appointment
from signup.models import User
from django.views.generic import FormView
from google.oauth2 import service_account
from django.contrib import messages
from django.http import HttpResponseRedirect
from googleapiclient.discovery import build
import pytz  
from datetime import timedelta



# Create your views here.
def CreateBlogView(request, userid):

    user = User.objects.get(id=userid)
    if request.method == "POST":
         form = BlogForm(request.POST,request.FILES)
                
         if form.is_valid():
            title = form.cleaned_data.get('title')
            img = form.cleaned_data.get('img')
            category = form.cleaned_data.get('category')
            summary = form.cleaned_data.get('summary')
            content = form.cleaned_data.get('content')
            draft = form.cleaned_data.get('draft')

            blog = Blog(title=title,img=img,category=category,summary=summary,content=content,draft=draft,user=user)
            blog.save()
            return redirect(reverse('doctorblogs', kwargs={"userid": userid}))
         else:
            print(form.errors)
    else:
        form = BlogForm()

    return render(request,"blog/create.html",{'form': form})


def DoctorBlogsView(request, userid):
    blogs = Blog.objects.filter(user=userid)
    blogs = {'blogs': blogs}
    
    return render(request,"blog/blogs.html", blogs)

def PatientBlogsView(request):
   blogs = Blog.objects.filter(draft=False)  
   blogs = {'blogs': blogs}
    
   return render(request,"blog/blogs.html", blogs)

def DetailBlogView(request, blogid):
    blog = get_object_or_404(Blog,id=blogid)
    context = {'blog': blog}
    return render(request,"blog/detail.html", context)

def ProfileView(request, userid):
    return render(request,"blog/home.html")

def DoctorsListView(request):
    doctors = User.objects.filter(user_type='Doctor')
    doctors = {'doctors': doctors}

    return render(request,"blog/doctorslist.html", doctors)

def build_service(request, doctor):

    SCOPES = ["https://www.googleapis.com/auth/calendar"]
    sservice_account_email = doctor.email
    credentials = service_account.Credentials.from_service_account_file('googleapi.json')
    scoped_credentials = credentials.with_scopes(SCOPES)
    
    service = build("calendar", "v3", credentials=scoped_credentials)
    return service

class BookApptView(FormView):
    form_class = BookingForm
    template_name = 'blog/bookappt.html'  
    

    def __init__(self):
        self.appt_instance = None
      
    def get_success_url(self):
        appt_id = self.appt_instance.id
        return reverse('apptconfirm', kwargs={'apptid': appt_id})

    def post(self, request, *args, **kwargs):
        form = BookingForm(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            print(form.errors)


    def form_valid(self, form):

        speciality = form.cleaned_data.get("speciality")
        start_date_data = form.cleaned_data.get("startDateTime")
        end_date_data = start_date_data + timedelta(minutes=45)
        doctor = User.objects.get(id=self.kwargs['doctorid'])

        service = build_service(self.request, doctor)
        calendarId = "55c23be4ae413e93a5a3a2798964e34d0b0c6a3aa90c0bdf2e538e11ba28b2e5@group.calendar.google.com"
        
        event = (
            service.events().insert(
                calendarId=calendarId,
                body={
                    "summary": speciality,
                    "start": {"dateTime": start_date_data.isoformat(),
                    },
                    "end": {"dateTime": end_date_data.isoformat(),
                          },
                    
                },
            ).execute()
        )

        appt = Appointment(speciality=speciality,startdate=start_date_data,enddate=end_date_data,doctor=doctor,patient=self.request.user)
        appt.save()
        self.appt_instance = appt
        return super().form_valid(form)


def ApptConfirmView(request, apptid):

    appt = Appointment.objects.get(id=apptid)
    appt = {'appt': appt}

    return render(request,'blog/apptconfirmation.html', appt)