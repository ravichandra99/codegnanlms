from django.shortcuts import render

from django.http import HttpResponse, HttpRequest, JsonResponse

from django.views.generic.detail import DetailView
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
import json
import razorpay

from .models import Order, Checkout

from lms.models import Course, OnlineClassroom

from authentication.models import MyUser
import uuid
# Create your views here.


@csrf_exempt
def make_order(amount, user, course, online_class):
    client = razorpay.Client(
        auth=("rzp_test_wv0ntAoxdPAhGJ", "Gs7HnSJtGtYNkGrhHvpVASnM"))

    order_amount = amount
    order_currency = 'INR'
    if(Order.objects.last()):
        prev_rec_no = int(Order.objects.last().receipt_no[8:])
        order_receipt = f"receipt#{str(prev_rec_no+1)}"
    else:
        order_receipt = f"receipt#1"
    # notes = request_notes  # OPTIONAL

    DATA = {'amount': int(order_amount),
            'currency': order_currency, 'receipt': order_receipt, 'payment_capture': 1}

    res = client.order.create(data=DATA)

    order = Order(order_id=res["id"], entity="order", amount=res["amount"], amount_paid=res["amount_paid"],
                  amount_due=res["amount_due"], currency=res["currency"], receipt_no=res["receipt"], status=res["status"],
                  attempts=res["attempts"], notes=str(res["notes"]), created_at=res["created_at"], user=user, course=course,
                  online_class=online_class)
    order.save()
    return order.order_id


@csrf_exempt
def checkout_success(request, slug):

    order_id = slug
    razorpay_order_id = request.POST.get("razorpay_order_id")
    razorpay_payment_id = request.POST.get("razorpay_payment_id")
    razorpay_signature = request.POST.get("razorpay_signature")

    checkout = Checkout(order_id=Order.objects.filter(order_id=order_id)[0], razorpay_order_id=razorpay_order_id,
                        razorpay_payment_id=razorpay_payment_id, razorpay_signature=razorpay_signature, successful=False)
    params_dict = {
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    }

    status = verify_authenticity(params_dict)
    if(status):
        checkout.successful = True
        order = Order.objects.filter(order_id=order_id)[0]
        response = {"successful": status, "order_id": order_id,
                    "user": str(order.user),
                    "course": order.course.title,
                    "amount": order.amount,
                    "receipt": order.receipt_no,
                    "online_class": str(order.online_class)}
        return render(request,'success.html',response)
    else:
        return JsonResponse({"successful": status}, safe=False)
    checkout.save()


def verify_authenticity(params_dict):
    client = razorpay.Client(
        auth=("rzp_test_wv0ntAoxdPAhGJ", "Gs7HnSJtGtYNkGrhHvpVASnM"))
    try:
        client.utility.verify_payment_signature(params_dict)
    except:
        return False
    else:
        return True


class Payment(LoginRequiredMixin,DetailView):
    template_name = "payment.html"
    order_id = None
    description = None
    course_id = None
    model = Course

    def get(self, request, *args, **kwargs):
        self.course_id = request.session["course_id"]
        reg_class = request.session["reg_class"]
        user_id = request.user.id
        self.description = request.session["description"]
        # request.session.flush()
        del request.session["course_id"]
        del request.session["reg_class"]
        del request.session["user_id"]
        del request.session["description"]
        f = open("data.txt", "w")
        f.write(str(user_id))
        user = MyUser.objects.filter(id=user_id)[0]
        course = Course.objects.filter(id=self.course_id)[0]
        online_class = OnlineClassroom.objects.filter(id=reg_class)[0]
        self.order_id = make_order(
            course.gst_price(), user, course, online_class)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order = Order.objects.filter(order_id=self.order_id)[0]
        # context["name"] = str(order.user)
        context["order_id"] = self.order_id
        context["amount"] = order.amount
        context["description"] = self.description
        return context

    def get_object(self):
        return get_object_or_404(Course, pk=self.course_id)
