from django.shortcuts import render,reverse,redirect
from lms.models import Course,Module,Lesson,CourseStatus,Category,Question,Answer,Blog,InterviewQuestions,BlogCategory\
,Testimonials,VideoReviews,OnlineClassroom,Reviews,Slider,GetMoreInfo,WhyCodegnan,FollowUs,Footer
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect,JsonResponse,HttpResponse
from django.views.generic.edit import FormMixin
from lms.forms import QuestionForm, ContactUsForm, GetInfoForm, OnlineForm
from django.contrib import messages
from authentication.views import CustomUserCreationForm
from django.contrib.auth import login, authenticate
# Create your views here.

def index(request):
	category = Category.objects.all()
	testimonials = Testimonials.objects.all()
	blogcategory = BlogCategory.objects.all()
	videoreviews = VideoReviews.objects.all()
	sliders = Slider.objects.all()
	whycodegnan = WhyCodegnan.objects.all()
	return render(request,'index.html',{'category':category, 'testimonials':testimonials,\
	 'blogcategory':blogcategory, 'videoreviews':videoreviews, 'sliders':sliders, 'whycodegnan':whycodegnan})

def about(request):
	return render(request,'about-us.html')


def CourseDetail(request,slug):
    object = Course.objects.get(slug = slug)
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = OnlineForm(request.POST,course_id=object.id)
        infoform = GetInfoForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            batch = form.cleaned_data['batch']
            oc = OnlineClassroom.objects.get(id = batch)
            course_id = oc.course.id
            reg_course = oc.course
            reg_class = oc.batch
            print(course_id,reg_course,reg_class,request.user)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            request.session['course_id'] = course_id
            request.session['reg_class'] = batch
            request.session['user_id'] = request.user.id
            request.session['description'] = str(object)
            return render(request,'order.html',{'course_id':course_id,'reg_class':reg_class,'object':object})
            '''return HttpResponseRedirect(request.build_absolute_uri(
                reverse('payment:payment')))'''
        elif infoform.is_valid():
        	name = infoform.cleaned_data['name']
        	email = infoform.cleaned_data['email']
        	phone = infoform.cleaned_data['phone']
        	info = GetMoreInfo(name = name,email = email,phone = phone,course = object.title)
        	info.save()
        	messages.success(request, 'Thanks for your Interest!')
        	return HttpResponseRedirect(reverse('lms:coursedetail', kwargs={'slug':slug}))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = OnlineForm(course_id=object.id)
        infoform = GetInfoForm()

    return render(request, 'newcoursepage.html', {'form': form,'object':object,'infoform':infoform,'meta':object.as_meta()})

def blog(request):
	blogcategory = BlogCategory.objects.all()
	return render(request,'blog.html', {'blogcategory':blogcategory})

def contact_us(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactUsForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            form.save()
            messages.success(request, 'Thanks for your Interest!,Our Team will Contact You Shortly')
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('lms:contact_us'))

    # if a GET (or any other method) we'll create a blank form
    else:
        form = ContactUsForm()

    return render(request, 'contact-us.html', {'form': form})

def event(request):
	return render(request,'event.html')

def allcourses(request):
	return render(request,'allcourses.html')

def mycourses(request):
	mycourses = CourseStatus.objects.filter(user = request.user)
	return render(request,'mycourses.html',{'mycourses':mycourses})

def cart(request):
	return render(request,'cart.html')

def checkout(request,slug):
    return render(request,'checkout.html')


class detail(FormMixin, DetailView):
	model = Course
	template_name = 'coursedetail.html'
	form_class = QuestionForm

	def get_success_url(self):
		return reverse('lms:detail', kwargs={'slug': self.object.slug})

	def get_context_data(self, **kwargs):
		context = super(detail, self).get_context_data(**kwargs)
		is_enrolled = self.request.user.is_authenticated and CourseStatus.objects.filter(user = self.request.user).filter(course = kwargs['object']).exists()
		if is_enrolled:
			user_course_it = CourseStatus.objects.filter(user = self.request.user).filter(course = kwargs['object'])
			user_course = CourseStatus.objects.get(id = [i.id for i in user_course_it][0])
			context['viewed'] = [i.video_id for i in user_course.completed_lessons.all()]
			context['form'] = QuestionForm()
			context['questions'] = Question.objects.filter(course = kwargs['object'])
			
		return context

	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		course = Course.objects.get(slug = kwargs['slug'])
		form = self.get_form()
		question = request.POST.get('question')
		if form.is_valid():
			form.instance.user = self.request.user
			form.instance.course = course
			form.instance.question = question
			return self.form_valid(form)
		else:
			return self.form_invalid(form)

	def form_valid(self, form):
		form.save()
		return super(detail, self).form_valid(form)

def onended(request):
	if request.is_ajax():
		iframe_id = request.GET.get('iframe_id')
		status = CourseStatus.objects.get(user = request.user)
		current_lesson = Lesson.objects.get(video_id = iframe_id)
		status.completed_lessons.add(current_lesson)
		status.save()

		data = {'next':next_lesson.id,'get_slug':next_lesson.get_slug(),'percent':status.percent()}
	return JsonResponse(data)

def enrol(request):
	if request.is_ajax():
		username = request.GET.get('username')[0]
		data = request.GET.get('status')
		#print(data)
		r = data.split(':')
		slug = r[0]
		payment_id = r[1]
		enrol,created = CourseStatus.objects.get_or_create(user_id = request.user.id,course_id = Course.objects.get(slug = slug).id)
		data = {'slug':slug,'created':created}
		return JsonResponse(data)

def navbar(request):
   return {'category':Category.objects.all(),'blogcategory':BlogCategory.objects.all(),'reviews':Reviews.objects.all(),\
   'videoreviews':VideoReviews.objects.all(),'testimonials':Testimonials.objects.all(),'footer':Footer.objects.all()}

class BlogView(ListView):
	model = BlogCategory
	template_name = 'blog.html'

class ArticleDetailView(DetailView):
	model = Blog
	template_name = 'article-detail.html'

class InterviewQuestionsView(ListView):
	model = InterviewQuestions
	template_name = 'interview-questions.html'

class InterviewQuestionsDetail(DetailView):
	model = InterviewQuestions
	template_name = 'interview-detail.html'

def bootcamps(request):
	return render(request, 'bootcamps.html')

'''def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Thanks for your Interest!')
            return redirect('payment:payment')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})'''

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            print(raw_password)
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            if 'course_id' in request.session:
                return redirect('payment:payment')
            else:
            	return redirect('lms:index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


