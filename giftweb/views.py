
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import *
from .forms import PaymentForm
from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView
from datetime import timedelta
from django.core.paginator import Paginator

class ProductDetailView(DetailView):
    model = Product
    template_name = 'giftweb/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()

        # Calculate the remaining time for the countdown
        remaining_time = product.countdown_time - (timezone.now() - product.timestamp)
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        context['days'] = days
        context['hours'] = hours
        context['minutes'] = minutes
        context['seconds'] = seconds

        # Calculate the discounted price if a discount is applicable
        if product.discount:
            discounted_price = product.price - product.discount
            context['discounted_price'] = discounted_price

        return context

def home(request):
    products = Product.objects.all()

    # Calculate the remaining time for each product
    current_time = timezone.now()
    for product in products:
        remaining_time = product.countdown_time - (current_time - product.timestamp)
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        product.remaining_days = days
        product.remaining_hours = hours
        product.remaining_minutes = minutes
        product.remaining_seconds = seconds

        # Calculate the discounted price if a discount is applicable
        if product.discount:
            discounted_price = product.price - (product.price * product.discount / 100)
            product.discounted_price = discounted_price

    return render(request, 'giftweb/index.html', {'products': products})

def premium_home(request):
    products = PremiumProduct.objects.all()

    # Calculate the remaining time for each product
    current_time = timezone.now()
    for product in products:
        remaining_time = product.countdown_time - (current_time - product.timestamp)
        days = remaining_time.days
        hours, remainder = divmod(remaining_time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        product.remaining_days = days
        product.remaining_hours = hours
        product.remaining_minutes = minutes
        product.remaining_seconds = seconds

        # Calculate the discounted price if a discount is applicable
        if product.discount:
            discounted_price = product.price - (product.price * product.discount / 100)
            product.discounted_price = discounted_price

    return render(request, 'giftweb/products.html', {'products': products})


@login_required
def make_payment(request, model_name, product_id):
    if model_name == 'product':
        model = Product
    elif model_name == 'premium_product':
        model = PremiumProduct
    else:
        return HttpResponseBadRequest("Invalid model name.")

    product = get_object_or_404(model, id=product_id)

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = request.user
            payment.product = product  # Assign the product to the payment
            payment.status = 'PENDING'

            # Set the payment amount to the product price
            payment.amount = product.price

            payment.save()
            return redirect('giftweb:payment_success')
    else:
        form = PaymentForm()
    
    return render(request, 'giftweb/checkout.html', {'form': form, 'product': product})


@login_required
def payment_success(request):
    payment = Payment.objects.filter(user=request.user).order_by('-id').first()
    return render(request, 'giftweb/payment_success.html', {'payment': payment})

def about(request):
    return render(request, 'giftweb/about.html')


def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'giftweb/blog.html', {'blogs': blogs})


def contact(request):
    return render(request, 'giftweb/contact.html')

@login_required
def cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'giftweb/cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Check if the product is already in the user's cart
    cart_item = CartItem.objects.filter(user=request.user, product=product).first()

    if cart_item:
        # Product already exists in the cart, update the quantity
        cart_item.quantity += 1
        cart_item.save()
    else:
        # Product does not exist in the cart, create a new cart item
        cart_item = CartItem(user=request.user, product=product, quantity=1)
        cart_item.save()

    return redirect('giftweb:cart')

class PremiumProductDetailView(DetailView):
    model = PremiumProduct
    template_name = 'giftweb/premiumproduct_detail.html'
    context_object_name = 'premium_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premium_product = self.get_object()

        # Add any additional context data for premium products here

        return context


@login_required
def payment_history(request):
    payments = Payment.objects.filter(user=request.user).order_by('-id')

    # Apply pagination with 7 entries per page
    paginator = Paginator(payments, 7)
    page_number = request.GET.get('page')  # Get the current page number from the request (e.g., query string parameter)

    # Get the corresponding page from the paginator
    page_obj = paginator.get_page(page_number)

    return render(request, 'giftweb/payment_history.html', {'page_obj': page_obj})
