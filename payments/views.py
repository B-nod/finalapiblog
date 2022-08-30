from django.shortcuts import render, get_object_or_404
from django.http.response import JsonResponse
from django.urls import reverse, reverse_lazy
from .models import *
import stripe
from django.views.generic import ListView, CreateView, DetailView, TemplateView
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import json

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = "payments/product_list.html"
    context_object_name = 'product_list'

class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = "payments/product_create.html"
    success_url = reverse_lazy("home")

class ProductDetailView(DetailView):
    model = Product
    template_name = "payments/product_detail.html"
    pk_url_kwarg = 'id'

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        context['stripe_publishable_key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context

@csrf_exempt
def create_checkout_session(request, id):

    request_data = json.loads(request.body)
    product = get_object_or_404(Product, pk=id)

    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                    'name': product.name,
                    },
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('success')
        ),
        cancel_url=request.build_absolute_uri(reverse('failed')),
    )


   
    # import pdb
    # pdb.set_trace()
    order = OrderDetail()
    order.customer_email = request_data['email']
    order.product = product
    order.stripe_payment_intent = checkout_session['payment_intent']
    order.amount = int(product.price * 100)
    order.save()

    # return JsonResponse({'data': checkout_session})
    return JsonResponse({'sessionId': checkout_session.id})

class PaymentSuccessView(TemplateView):
    template_name = "payments/payment_success.html"

    def get(self, request):

        return render(request, self.template_name)

class PaymentFailedView(TemplateView):
    template_name = "payments/payment_failed.html"

class OrderHistoryListView(ListView):
    model = OrderDetail
    template_name = "payments/order_history.html"