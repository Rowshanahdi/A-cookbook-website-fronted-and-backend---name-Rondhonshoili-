from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect


from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash






from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

def homepage(request):
    # your homepage logic
    return render(request, 'homepage.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('homepage')
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Registration successful, please login.")
        return redirect('login')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('homepage')

from .models import Product

def shop(request):
    products = Product.objects.all()
    return render(request, 'shop.html', {'products': products})
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

@login_required
def profile(request):
    user = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if username and email:
            user.username = username
            user.email = email
            if password:
                user.set_password(password)
            user.save()
            messages.success(request, 'Profile updated successfully!')

            
            if password:
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)

            return redirect('profile')

    orders = Order.objects.filter(user=user).order_by('-created_at')
    return render(request, 'profile.html', {'orders': orders})




from django.shortcuts import render
from django.contrib.auth.decorators import login_required

def profile(request):
    user = request.user  # current logged-in user
    # pass user to template
    return render(request, 'profile.html', {'user': user})


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required  # Optional: requires login, remove if not needed
def payment(request):
    # Add your payment page logic here (e.g., form handling)
    return render(request, 'payment.html')




from django.shortcuts import render

def cart(request):
    # Your logic here
    return render(request, 'cart.html')




def reviews(request):
    # Your logic here
    return render(request, 'reviews.html')




def  About_us(request):
    # Your logic here
    return render(request, 'About_us.html')











from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def payment_view(request):
    total_price = request.GET.get('total', 0)
    return render(request, 'payment.html', {'total_price': total_price})









from django.contrib.auth.decorators import login_required

@login_required
def register_class(request):
    # This renders the form page where your HTML form is.
    return render(request, 'register_class.html')


# home/views.py
from django.shortcuts import render

def class_updates(request):
    # Your code here
    return render(request, 'class_updates.html')

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import FreeClassRegistration, PaidClassRegistration

@login_required
def register_free_class(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact')
        email = request.POST.get('email')

        FreeClassRegistration.objects.create(
            user=request.user,
            full_name=full_name,
            contact_number=contact_number,
            email=email
        )
        return redirect('class_updates')
    return redirect('class_updates')



from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from .models import PaidClassRegistration

@login_required
def register_paid_class(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        contact_number = request.POST.get('contact')
        email = request.POST.get('email')
        transaction_id = request.POST.get('transactionId')
        screenshot = request.FILES.get('paymentScreenshot')

        PaidClassRegistration.objects.create(
            user=request.user,
            full_name=full_name,
            contact_number=contact_number,
            email=email,
            transaction_id=transaction_id,
            payment_screenshot=screenshot
        )

        # Send confirmation email
        send_mail(
            'Paid Class Registration Received',
            f'Dear {full_name},\n\nWe received your registration and payment info for the PAID cooking class.\nTransaction ID: {transaction_id}\n\nYou will receive the Zoom link a day before the class.\n\nThanks,\nRondhonshoili Team',
            settings.EMAIL_HOST_USER,  # sender email
            [email],                   # recipient email
            fail_silently=False,
        )

        # Show success message on screen
        messages.success(request, 'Your registration and payment info has been submitted successfully! Confirmation email sent.')

        return redirect('class_updates')

    return redirect('class_updates')






















from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_msg = form.save(commit=False)
            if request.user.is_authenticated:
                contact_msg.user = request.user
            contact_msg.save()
            messages.success(request, "Thank you for contacting us. We will get back to you soon!", extra_tags='contact')
            return redirect('contact')
        else:
            messages.error(request, "Please correct the errors below.", extra_tags='contact')
    else:
        form = ContactForm()
        if request.user.is_authenticated:
            # Pre-fill the name and email if logged in
            form.fields['full_name'].initial = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username
            form.fields['email'].initial = request.user.email
    
    # Get only contact-related messages
    contact_messages = messages.get_messages(request)
    filtered_messages = [msg for msg in contact_messages if 'contact' in msg.tags.split()]
    
    return render(request, 'contact.html', {
        'form': form,
        'contact_messages': filtered_messages  # Pass only filtered messages
    })



























from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Recipe, SavedRecipe
from django.contrib import messages

@login_required
def save_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    already_saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()

    if not already_saved:
        SavedRecipe.objects.create(user=request.user, recipe=recipe)
        messages.success(request, "Recipe saved to favorites!")
    else:
        messages.info(request, "Recipe already in favorites.")

    return redirect(request.META.get('HTTP_REFERER', 'homepage'))




@login_required
def remove_recipe(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    SavedRecipe.objects.filter(user=request.user, recipe=recipe).delete()
    messages.success(request, "Recipe removed from favorites.")
    return redirect('saved_recipes')

@login_required
def saved_recipes(request):
    recipes = SavedRecipe.objects.filter(user=request.user)
    return render(request, 'my_saved_recipes.html', {'recipes': recipes})


def recipe_view(request, template_name, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    saved_recipes = SavedRecipe.objects.filter(user=request.user).values_list('recipe__id', flat=True) if request.user.is_authenticated else []
    return render(request, template_name, {
        'recipe': recipe,
        'saved_recipes': saved_recipes
    })




from django.shortcuts import render, get_object_or_404
from .models import Recipe

def recipe_detail(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    return render(request, 'recipe_detail.html', {'recipe': recipe})

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipe, SavedRecipe, Review

def custom_recipe_view(request, slug, template_name):
    recipe = get_object_or_404(Recipe, slug=slug)
    saved = False
    if request.user.is_authenticated:
        saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()

    # Handle Review Submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 0)
        comment = request.POST.get('comment', '')
        name = request.POST.get('name', request.user.username)

        # Only allow one review per user per recipe
        existing_review = Review.objects.filter(recipe=recipe, user=request.user).first()
        if not existing_review:
            Review.objects.create(
                recipe=recipe,
                user=request.user,
                rating=rating,
                comment=comment,
                name=name
            )
            messages.success(request, "Thank you for your review!")
        else:
            messages.info(request, "You have already reviewed this recipe.")

        return redirect(request.path)  # Reload the same page

    context = {
        'recipe': recipe,
        'saved': saved,
        'user_review': Review.objects.filter(recipe=recipe, user=request.user).first()
                        if request.user.is_authenticated else None
    }
    return render(request, template_name, context)











def popular(request):
    return render(request, 'pop.html')

def recipe(request):
    return render(request, 'recipe.html')

def snack(request):
    return render(request, 'snack&sweet.html')

def traditional(request):
    return render(request, 'traditional.html')

def drinks(request):
    return render(request, 'drinks.html')










def beefnihari(request):
    return custom_recipe_view(request, 'beefnihari', 'recipie-lay.html')

def biriyani(request):
    return custom_recipe_view(request, 'biriyani', 'biriyani.html')

def breadroll(request):
    return custom_recipe_view(request, 'breadroll', 'bread_roll.html')

def chickenroast(request):
    return custom_recipe_view(request, 'chickenroast', 'Chicken_roast.html')

def faluda(request):
    return custom_recipe_view(request, 'faluda', 'faluda.html')

def ilishpolao(request):
    return custom_recipe_view(request, 'ilishpolao', 'ilish_polao.html')

def kabsa(request):
    return custom_recipe_view(request, 'kabsa', 'kabsa.html')

def kulfi(request):
    return custom_recipe_view(request, 'kulfi', 'kulfi.html')

def lassi(request):
    return custom_recipe_view(request, 'lassi', 'lassi.html')

def masalatea(request):
    return custom_recipe_view(request, 'masalatea', 'masala_tea.html')

def mintlemonade(request):
    return custom_recipe_view(request, 'mintlemonade', 'mint_lamonade.html')

def mohito(request):
    return custom_recipe_view(request, 'mohito', 'mohito.html')

def samossa(request):
    return custom_recipe_view(request, 'samossa', 'samossa.html')

def sahitukra(request):
    return custom_recipe_view(request, 'sahitukra', 'shahi_tukra.html')

def sheerkurma(request):
    return custom_recipe_view(request, 'sheerkurma', 'sheer_kurma.html')

def banana_milk(request):
    return custom_recipe_view(request, 'banana_milk', 'banana_milk_shake.html')

def bhetki(request):
    return custom_recipe_view(request, 'bhetki', 'Bhetki Paturi.html')

def payesh(request):
    return custom_recipe_view(request, 'payesh', 'payesh.html')








































from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Recipe, Review, SavedRecipe

def recipe_detail(request, slug):
    # Fetch the recipe by slug or 404
    recipe = get_object_or_404(Recipe, slug=slug)
    
    # Check if this recipe is saved by the current user
    saved = False
    if request.user.is_authenticated:
        saved = SavedRecipe.objects.filter(user=request.user, recipe=recipe).exists()
    
    # Handle review form submission
    if request.method == 'POST' and request.user.is_authenticated:
        rating = request.POST.get('rating', 0)
        comment = request.POST.get('comment', '')
        name = request.POST.get('name', request.user.get_full_name() or request.user.username)
        
        Review.objects.create(
            recipe=recipe,
            user=request.user,
            rating=rating,
            comment=comment,
            name=name
        )
        messages.success(request, "Thank you for your review!")
        return redirect(request.path)  # Redirect to same recipe page
    
    # Map slugs to specific templates
    template_map = {
        'beefnihari': 'beefnihari.html',
        'biriyani': 'biriyani.html',
        'breadroll': 'bread_roll.html',
        'chickenroast': 'chicken_roast.html',
        'faluda': 'faluda.html',
        'ilishpolao': 'ilish_polao.html',
        'kabsa': 'kabsa.html',
        'kulfi': 'kulfi.html',
        'lassi': 'lassi.html',
        'masalatea': 'masala_tea.html',
        'mintlemonade': 'mint_lemonade.html',
        'mohito': 'mohito.html',
        'samossa': 'samossa.html',
        'sahitukra': 'shahi_tukra.html',
        'sheerkurma': 'sheer_kurma.html',
        'banana_milk': 'banana_milk_shake.html',
        'bhetki': 'bhetki_paturi.html',
        'payesh': 'payesh.html',
        # Add more if needed
    }
    template_name = template_map.get(slug, 'default_recipe_template.html')  # fallback template
    
    # Pass context
    context = {
        'recipe': recipe,
        'saved': saved,
        'user_review': Review.objects.filter(recipe=recipe, user=request.user).first() if request.user.is_authenticated else None,
    }
    
    return render(request, template_name, context)

def reviews_page(request):
    all_reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': all_reviews})
















from django.shortcuts import render, get_object_or_404
from .models import Recipe, Review

class ReviewMixin:
    """Handles reviews for all recipe views"""
    template_name = None  # Will be set by individual views
    
    def get(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=self.slug)
        context = self.get_review_context(request, recipe)
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        recipe = get_object_or_404(Recipe, slug=self.slug)
        
        if request.user.is_authenticated:
            rating = request.POST.get('rating', 0)
            comment = request.POST.get('comment', '')
            name = request.POST.get('name', request.user.username)
            
            Review.objects.create(
                recipe=recipe,
                user=request.user,
                rating=rating,
                comment=comment,
                name=name
            )
        
        context = self.get_review_context(request, recipe)
        return render(request, self.template_name, context)
    
    def get_review_context(self, request, recipe):
        return {
            'recipe': recipe,
            'user_review': Review.objects.filter(recipe=recipe, user=request.user).first() 
                          if request.user.is_authenticated else None
        }
    




































from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, CartItem, Order

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.subtotal() for item in cart_items)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
    })

@login_required
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'increase':
            cart_item.quantity += 1
            cart_item.save()
        elif action == 'decrease':
            if cart_item.quantity > 1:
                cart_item.quantity -= 1
                cart_item.save()
            else:
                cart_item.delete()
    return redirect('cart')

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

@login_required
def cancel_order(request):
    # Clear the user's cart
    CartItem.objects.filter(user=request.user).delete()
    return redirect('cart')

@login_required
def payment(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_amount = sum(item.subtotal() for item in cart_items)
    return render(request, 'payment.html', {'total_price': total_amount})
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import Order
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order
from decimal import Decimal
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def submit_order(request):
    if request.method == 'POST':
        try:
            total_raw = request.POST.get('total', '0').replace('৳', '').strip()
            total = Decimal(total_raw) if total_raw else Decimal('0.00')

            district = request.POST.get('district', '').strip()
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            address = request.POST.get('address', '').strip()

            # Make sure all required fields are filled
            if not all([district, name, phone, address]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('cart')

            Order.objects.create(
                user=request.user,
                total=total,
                district=district,
                name=name,
                phone=phone,
                address=address
            )

            messages.success(request, 'Your order has been confirmed!')
            return redirect('homepage')

        except Exception as e:
            messages.error(request, f"Error saving order: {e}")
            return redirect('cart')

    return redirect('cart')


    return render(request, 'order_form.html')  # যদি GET রিকোয়েস্ট আসে


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Order

from django.shortcuts import render
from .models import Order

def profile(request):
    user_orders = Order.objects.filter(user=request.user).prefetch_related('items__product')

    context = {
        'orders': user_orders,
    }
    return render(request, 'profile.html', context)
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from decimal import Decimal
from .models import Order, OrderItem, CartItem

@login_required
def submit_order(request):
    if request.method == 'POST':
        try:
            # Remove currency symbol and convert total to Decimal
            total_raw = request.POST.get('total', '0').replace('৳', '').strip()
            total = Decimal(total_raw) if total_raw else Decimal('0.00')

            district = request.POST.get('district', '').strip()
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            address = request.POST.get('address', '').strip()

            # Validate required fields
            if not all([district, name, phone, address]):
                messages.error(request, "Please fill in all required fields.")
                return redirect('cart')  # or wherever your cart page is

            # Create order
            order = Order.objects.create(
                user=request.user,
                total=total,
                district=district,
                name=name,
                phone=phone,
                address=address
            )

            # Get cart items for the user
            cart_items = CartItem.objects.filter(user=request.user)

            # Save order items
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            # Clear user's cart
            cart_items.delete()

            messages.success(request, 'Your order has been confirmed!')
            return redirect('homepage')

        except Exception as e:
            messages.error(request, f"Error saving order: {e}")
            return redirect('cart')

    # If not POST, redirect to cart or appropriate page
    return redirect('cart')
