from django.db import models
from authentication.models import MyUser
from lms.ytd import ytapi,minsec
import itertools,random
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from meta.models import ModelMeta

# Create your models here.

class TimeStamp(models.Model):
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	user = models.ForeignKey(MyUser,on_delete = models.CASCADE,null = True)

	class Meta:
		abstract = True

class Category(models.Model):
	category = models.CharField(max_length = 200)
	img380x256 = models.ImageField(upload_to = '',default = 'market.jpg',blank = True,null = True)

	def __str__(self):
		return self.category

	def trending_courses(self):
		objects = [i for i in Course.objects.all()]
		random.shuffle(objects)
		return objects[:8]

class BlogCategory(models.Model):
	category = models.CharField(max_length = 200)
	def latest_blogs(self):
		objects = [i for i in Blog.objects.all()]
		random.shuffle(objects)
		return objects[:3]

	def __str__(self):
		return self.category

class InterviewCategory(models.Model):
	category = models.CharField(max_length = 200)

	def __str__(self):
		return self.category

class Project(models.Model):
	title = models.CharField(max_length = 100)
	description = models.TextField()

	def __str__(self):
		return self.title

class Trainer(models.Model):
	name = models.CharField(max_length = 100)
	image = models.ImageField(upload_to = '',default = 'market.jpg')
	about = models.CharField(max_length = 200)
	description = models.TextField()
	linkedin = models.URLField()
	quora = models.URLField()

	def __str__(self):
		return self.name

class FAQ(models.Model):
	question = models.CharField(max_length = 300)
	answer = models.TextField()

	def __str__(self):
		return self.question

class Certificate(models.Model):
	title = models.CharField(max_length = 300)
	image = models.ImageField(upload_to = '',blank = True,null = True)

	def __str__(self):
		return self.title

class CertQuestion(models.Model):
	certificate = models.ForeignKey(Certificate,on_delete = models.CASCADE)
	question = models.CharField(max_length = 300)
	answer = models.TextField()

	def __str__(self):
		return self.question


class Course(ModelMeta,models.Model):
	category = models.ForeignKey(Category, on_delete = models.CASCADE)
	trainer = models.ManyToManyField(Trainer)
	project = models.ManyToManyField(Project)
	title = models.CharField(max_length = 100)
	big_title = models.CharField(max_length = 300)
	short_description = models.TextField()
	description = models.TextField(verbose_name = 'Course Overview')
	video_id = models.CharField(max_length = 20,default = 'bY6m6_IIN94',verbose_name = "Introduction Video ID")
	img293x274 = models.ImageField(upload_to = '',blank = True,null = True)
	duration = models.CharField(max_length = 10)
	credits = models.IntegerField()
	rating = models.FloatField()
	enrolled = models.IntegerField()
	slug = models.SlugField()
	offer_price = models.IntegerField()
	original_price = models.IntegerField()
	offer_expires = models.IntegerField(default = 3)
	tags = models.TextField(verbose_name = 'Key Skills')
	cert1 = models.ImageField(upload_to = '',default = 'img/img/microsoft-logo.png')
	cert2 = models.ImageField(upload_to = '',default = 'img/img/microsoft-logo.png')
	certification = models.ManyToManyField(Certificate)
	faq = models.ManyToManyField(FAQ)

	_metadata = {
		'title': 'title',
		'description': 'get_description',
		'image': 'get_meta_image',
		}


	def __str__(self):
		return self.title

	def get_tags(self):
		return self.tags.split(",")

	def lesson_count(self):
		lesson_list = [i.lesson_set.all().count() for i in Course.objects.get(id = self.id).module_set.all()]
		return list(itertools.accumulate(lesson_list))[-1]

	def get_meta_image(self):
		if self.image293x274:
			return self.image293x274.url

	def get_description(self):
		return self.description[:200]

	def gst_price(self):
		return self.offer_price + (self.offer_price*0.18)



class Module(models.Model):
	course = models.ForeignKey(Course,on_delete = models.CASCADE)
	module = models.CharField(max_length = 1000)
	#pdf = models.FileField(upload_to = '',default = 'mozilla.pdf',blank = True,null = True)
	
	def __str__(self):
		return self.module

	def duration(self):
		obj = Module.objects.get(id = self.id)
		videos = [ytapi(i.video_id) for i in obj.lesson_set.all()]
		return minsec(list(itertools.accumulate(videos))[-1])


class Lesson(models.Model):
	module = models.ForeignKey(Module,on_delete = models.CASCADE)
	lesson = models.TextField()
	#pdf = models.FileField(upload_to = '',default = 'mozilla.pdf',blank = True,null = True)
	video_id = models.CharField(max_length = 11,blank = True,null = True)

	def __str__(self):
		return self.lesson

	def duration(self):
		return minsec(ytapi(self.video_id))

	def get_slug(self):
		return slugify(self.lesson,allow_unicode = True)

	def all_lessons(self):
		return Lesson.objects.all().count()


class CourseStatus(models.Model):
	course = models.ForeignKey(Course,on_delete = models.CASCADE)
	user = models.ForeignKey(MyUser,on_delete = models.CASCADE)
	completed_lessons = models.ManyToManyField(Lesson,related_name = 'completed_lessons',blank = True)
	current_lesson = models.ForeignKey(Lesson,on_delete = models.CASCADE, related_name = 'current_lesson',blank = True,null = True)

	class Meta:
		verbose_name_plural = "Course Status"

	def percent(self):
		status = CourseStatus.objects.get(id = self.id)
		return (status.completed_lessons.all().count()/status.course.lesson_count())*100

class Question(TimeStamp):
	question = models.TextField()
	course = models.ForeignKey(Course,on_delete = models.CASCADE)

	def __str__(self):
		return self.question

class InterviewQuestion(Question):
	pass

class Answer(TimeStamp):
	question = models.ForeignKey(Question,on_delete = models.CASCADE,related_name = "answers")
	answer = models.TextField()

	def __str__(self):
		return self.answer

class InterviewAnswer(Answer):
	pass

class GetMoreInfo(models.Model):
	course = models.CharField(max_length = 50)
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.IntegerField()

	def __str__(self):
		return self.name

class ContactUs(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField()
	phone = models.IntegerField()
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	#Course Mode Field Here
	msg = models.TextField()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "Contact Us"


class InterviewQuestions(models.Model):
	category = models.ForeignKey(InterviewCategory, on_delete=models.CASCADE)
	title = models.CharField(max_length=200)
	description = models.TextField()
	question = models.ForeignKey(InterviewQuestion,default = 1, on_delete=models.CASCADE, blank=True,null=True)
	answer = models.ForeignKey(InterviewAnswer,default = 1, on_delete=models.CASCADE, blank=True,null=True)
	slug = models.SlugField()

	def __str__(self):
		return self.title


class Blog(TimeStamp):	
	category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
	title = models.CharField(max_length=100)
	image1024x576 = models.ImageField(upload_to='', default='market.jpg') 
	body = RichTextUploadingField()
	slug = models.SlugField()
	views = models.IntegerField(default = 0)
	author = models.CharField(max_length = 30,default = '')
	tags = models.CharField(max_length=200)
	facebook = models.URLField()
	twitter = models.URLField()
	linkedin = models.URLField()

	def __str__(self):
		return self.title

	def get_tags(self):
		return self.tags.split(",")


class Reviews(models.Model):
	reviews = models.IntegerField()
	image = models.ImageField(upload_to = '')
	name = models.CharField(max_length = 20)

	def __str__(self):
		return self.name

class Testimonials(models.Model):
	image = models.ImageField(upload_to = '')
	name = models.CharField(max_length=100)
	organization = models.CharField(max_length=100)
	review = models.TextField()
	logo = models.ForeignKey(Reviews,on_delete = models.CASCADE)

	def __str__(self):
		return self.name

class VideoReviews(models.Model):
	title = models.CharField(max_length=100)
	embed_link = models.URLField()

	def __str__(self):
		return self.title

class Slider(models.Model):
	title = models.CharField(max_length=100)
	image = models.ImageField(upload_to = '')

	def __str__(self):
		return self.title

class OnlineClassroom(models.Model):
	course = models.ForeignKey(Course,on_delete = models.CASCADE)
	batch = models.CharField(max_length = 200)

	def __str__(self):
		return self.batch

class WhyCodegnan(models.Model):
	why = models.TextField()

	class Meta:
		verbose_name_plural = "Why Codegnan"

class Codegnan(models.Model):
	why = models.ForeignKey(WhyCodegnan,on_delete = models.CASCADE)
	title = models.CharField(max_length = 100)
	number = models.IntegerField()

	class Meta:
		verbose_name_plural = "Codegnan"

class Footer(models.Model):
	logo = models.ImageField(upload_to = '')
	description = models.TextField()

	class Meta:
		verbose_name_plural = "Footer"

class FollowUs(models.Model):
	footer = models.ForeignKey(Footer,on_delete = models.CASCADE)
	follow = models.ImageField(upload_to = '')
	url = models.URLField()

	def __str__(self):
		return str(self.url)

