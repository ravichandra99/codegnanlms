from django import template
from lms.models import CourseStatus
register = template.Library()

@register.simple_tag
def user_enrolled(user,course):
	return CourseStatus.objects.filter(user = user).filter(course = course).exists()
