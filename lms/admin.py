from django.contrib import admin

# Register your models here.
from lms.models import Course,Module,Lesson,CourseStatus,Category,BlogCategory,Project,Trainer,FAQ,Question,Answer,\
GetMoreInfo,ContactUs,Blog,Testimonials,VideoReviews,Slider,Certificate,CertQuestion,OnlineClassroom,Reviews,WhyCodegnan,Codegnan,Footer,FollowUs

import nested_admin

class OnlineClassroomInline(nested_admin.NestedStackedInline):
	model = OnlineClassroom

class LessonInline(nested_admin.NestedStackedInline):
    model = Lesson

class ModuleInline(nested_admin.NestedStackedInline):
    model = Module
    inlines = [LessonInline]

class CourseAdmin(nested_admin.NestedModelAdmin):
    inlines = [ModuleInline,OnlineClassroomInline]

class CertQuestionAdmin(admin.TabularInline):
    model = CertQuestion

class CertificateAdmin(admin.ModelAdmin):
   inlines = [CertQuestionAdmin,]

admin.site.register(Certificate,CertificateAdmin)

class CodegnanAdmin(admin.TabularInline):
    model = Codegnan

class WhyCodegnanAdmin(admin.ModelAdmin):
   inlines = [CodegnanAdmin,]

admin.site.register(WhyCodegnan,WhyCodegnanAdmin)

class FollowUsAdmin(admin.TabularInline):
    model = FollowUs

class FooterAdmin(admin.ModelAdmin):
   inlines = [FollowUsAdmin,]

admin.site.register(Footer,FooterAdmin)


admin.site.register(Category)
admin.site.register(Project)
admin.site.register(Trainer)
admin.site.register(FAQ)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(CourseStatus)
admin.site.register(GetMoreInfo)
admin.site.register(ContactUs)
admin.site.register(Blog)
admin.site.register(Course, CourseAdmin)
admin.site.register(BlogCategory)
admin.site.register(Testimonials)
admin.site.register(VideoReviews)
admin.site.register(Slider)
admin.site.register(Reviews)

