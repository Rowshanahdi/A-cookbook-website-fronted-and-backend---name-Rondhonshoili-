from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('shop/', views.shop, name='shop'),
    path('profile/', views.profile, name='profile'),
    path('logout/', views.logout_view, name='logout'),

 path('cart/', views.cart_view, name='cart'),
    path('cart/update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cancel-order/', views.cancel_order, name='cancel_order'),
    path('payment/', views.payment, name='payment'),
    path('submit_order/', views.submit_order, name='submit_order'),
    
    
    
    path('recipe/<slug:slug>/', views.recipe_detail, name='recipe_detail'),  # keep only this one
   path('reviews/', views.reviews_page, name='reviews'),  # Change name from 'reviews_page' to 'reviews'

    path('contact/', views.contact_view, name='contact'),

    path('popular/', views.popular, name='popular'),
    path('recipe/', views.recipe, name='recipe'),
    path('snack/', views.snack, name='snack'),
    path('traditional/', views.traditional, name='traditional'),
    path('drinks/', views.drinks, name='drinks'),

    path('About_us/', views.About_us, name='About_us'),

    path('save-recipe/<int:recipe_id>/', views.save_recipe, name='save_recipe'),
    path('remove-recipe/<int:recipe_id>/', views.remove_recipe, name='remove_recipe'),
    path('saved-recipes/', views.saved_recipes, name='saved_recipes'),

    path('class-updates/', views.class_updates, name='class_updates'),
    path('register-class/', views.register_class, name='register_class'),
    path('register-free-class/', views.register_free_class, name='register_free_class'),
    path('register-paid-class/', views.register_paid_class, name='register_paid_class'),

    path('biriyani/', views.biriyani, name='biriyani'),
    path('breadroll/', views.breadroll, name='breadroll'),
    path('chicken-roast/', views.chickenroast, name='chickenroast'),
    path('faluda/', views.faluda, name='faluda'),
    path('ilishpolao/', views.ilishpolao, name='ilishpolao'),
    path('kabsa/', views.kabsa, name='kabsa'),
    path('kulfi/', views.kulfi, name='kulfi'),
    path('lassi/', views.lassi, name='lassi'),
    path('masala-tea/', views.masalatea, name='masalatea'),
    path('mint-lemonade/', views.mintlemonade, name='mintlemonade'),
    path('mohito/', views.mohito, name='mohito'),
    path('samossa/', views.samossa, name='samossa'),
    path('shahi-tukra/', views.sahitukra, name='shahi_tukra'),
    path('sheerkurma/', views.sheerkurma, name='sheerkurma'),
    path('beefnihari/', views.beefnihari, name='beefnihari'),
    path('banana-milk/', views.banana_milk, name='banana_milk'),
    path('bhetki/', views.bhetki, name='bhetki'),
    path('payesh/', views.payesh, name='payesh'),
]
