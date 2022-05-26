#from django.shortcuts import render
#from urllib3 import HTTPResponse
# from django.http import HttpResponse
# from tempfile import template

from django.views.generic import TemplateView
from datetime import datetime

from .models import News
from django.shortcuts import get_object_or_404
from mainapp import models as mainapp_models

# Create your views here.


class MainPageView(TemplateView):
    template_name = "mainapp/index.html"


class NewsPageView(TemplateView):
    template_name = "mainapp/news.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context['news_title'] = "Громкий новостной заголовок"
        # context[
        #     "news_preview"
        # ] = "Предварительное описание, которое заинтересует каждого"
        # context["news_range"] = range(5)
        # context["datetime_obj"] = datetime.now()
        context['object_list'] = News.objects.all()[:5]
        return context

class CoursesPageView(TemplateView):
    template_name = "mainapp/courses_list.html"

    def get_context_data(self, **kwargs):
        context = super(CoursesPageView, self).get_context_data(**kwargs)
        context["objects_list"] = mainapp_models.Course.objects.all()[:7]
        return context


class ContactsPageView(TemplateView):
    template_name = "mainapp/contacts.html"


class CoursesDetailView(TemplateView):
    template_name = "mainapp/courses_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super(CoursesDetailView, self).get_context_data(**kwargs)
        context["course_object"] = get_object_or_404(mainapp_models.Courses, pk=pk)
        context["lessons"] = mainapp_models.Lesson.objects.filter(
    course=context["course_object"]
)
        context["teachers"] = mainapp_models.CourseTeachers.objects.filter(
    course=context["course_object"]
)
        return context



class DocSitePageView(TemplateView):
    template_name = "mainapp/doc_site.html"


class LoginPageView(TemplateView):
    template_name = "mainapp/login.html"

class NewsWithPaginatorView(NewsPageView):
    def get_context_data(self, page, **kwargs):
        context = super().get_context_data(page=page, **kwargs)
        context["page_num"] = page
        return context

class NewsPageDetailView(TemplateView):
    template_name = "mainapp/news_detail.html"

    def get_context_data(self, pk=None, **kwargs):
        context = super().get_context_data(pk=pk, **kwargs)
        context["news_objects"] = get_object_or_404(News, pk=pk)
        return context
