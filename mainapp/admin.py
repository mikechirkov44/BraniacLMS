from django.contrib import admin
from mainapp.models import News, Course, Lesson, CoursesTeacher
from django.utils.html import format_html
 #Register your models here.

admin.site.register(Course)
admin.site.register(Lesson)
admin.site.register(CoursesTeacher)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'slug', 'deleted')
    list_filter = ('deleted', 'created_at')
    ordering = ('pk', )
    list_per_page = 3
    search_fields = ('title', 'preamble', 'body')
    actions = ('mark_as_delete', )

    def slug(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.title.lower().replace(' ','-'),
            obj.title
                       )
    slug.short_description = 'Слаг'

    def mark_as_delete(self, request, queryset):
        queryset.update(deleted=True)
    
    mark_as_delete.short_description = 'Пометить удаленным'
      
