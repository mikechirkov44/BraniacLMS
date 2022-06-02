from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, DetailView, CreateView  
from datetime import datetime

from requests import delete

from mainapp.forms import CourseFeedbackForm

from .models import Course, CourseFeedback, CoursesTeacher, Lesson, News
from django.shortcuts import get_object_or_404
from mainapp import models as mainapp_models
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.template.loader import render_to_string 

# Create your views here.
class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(ListView):
    model = News
    paginate_by = 3
    
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)
    

class NewsDetailView(DetailView):
    model = News


class NewsCreateView(PermissionRequiredMixin, CreateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.add_news',)

class NewsUpdateView(PermissionRequiredMixin, UpdateView):
    model = News
    fields = '__all__'
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.change_news',)

class NewsDeleteView(PermissionRequiredMixin, DeleteView):
    model = News
    success_url = reverse_lazy('mainapp:news')
    permission_required = ('mainapp.delete_news',) 

class CoursesPageView(ListView):
    template_name = "mainapp/courses_list.html"
    model = Course

  

class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


# class CoursesDetailView(TemplateView):
#     template_name = "mainapp/courses_detail.html"

#     def get_context_data(self, pk=None, **kwargs):
#         context = super(CoursesDetailView, self).get_context_data(**kwargs)
#         context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
#         context["lessons"] = mainapp_models.Lesson.objects.filter(
#     course=context["course_object"]
# )
#         context["teachers"] = mainapp_models.CourseTeachers.objects.filter(
#     course=context["course_object"]
# )
#         return context



class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"

class CourseDetailView(TemplateView):
    template_name = 'mainapp/courses_detail.html'

    def get_context_data(self, pk=None,  **kwargs):
        context = super(CourseDetailView, self).get_context_data(**kwargs)
        context['course_object'] = get_object_or_404(Course, pk=self.kwargs.get('pk'))
        context['lessons'] = Lesson.objects.filter(course=context['course_object'])       
        context['teachers'] = CoursesTeacher.objects.filter(course=context['course_object'])
        context['feedback_list'] = CourseFeedback.objects.filter(course=context['course_object'])
        
        if self.request.user.is_authenticated:
            context['feedback_form'] = CourseFeedbackForm(
                course=context['course_object'], 
                user=self.request.user
                )
        
        return context
        
class CourseFeedbackCreateView(CreateView):
    model = CourseFeedback
    form_class = CourseFeedbackForm

    def form_valid(self, form):
        self.object = form.save()
        rendered_template = render_to_string('includes/feedback_card.html', context={'item': self.object})
        return JsonResponse({'card': rendered_template })