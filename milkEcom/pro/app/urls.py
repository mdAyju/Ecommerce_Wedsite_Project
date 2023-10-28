from django.urls import path
from django.contrib import admin
from app import views
from django.conf import settings
from django.contrib.auth import views as auth_view
from django.conf.urls.static import static
from app.forms import  LoginForm,MyPasswordChange,PasswordResetForm,MySetPasswordForm

urlpatterns = [
    path('',views.main),
    path('About/',views.about,name='about'),
    path('Contact/',views.contact,name='contact'),
    path('category/<slug:val>',views.CategoryView.as_view(),name='categorys'),
    path('category-title/<val>',views.categorytitle.as_view(),name='category-title'),
    path('product-detail/<int:pk>',views.productDetails.as_view(),name='product-detail'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('address/',views.address,name='address'),
    path('AddressUpdate/<int:pk>',views.addressUpdate.as_view(),name='addressUpdate'),
    path('Registration/',views.customerRegistrationview.as_view(),name='customerRegistration'),


    # login
    path('login',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    path('logout/',auth_view.LogoutView.as_view(next_page='login'),name='logout'),

    # Password Change
    path('passwordchange/',auth_view.PasswordChangeView.as_view(template_name='changepassword.html',form_class=MyPasswordChange,success_url='/passwordchangedone'),name='passwordchange'),
    path('passwordchangedone/',auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'),name='passwordchangedone'),

    # Password Reset
    path('passwordreset/',auth_view.PasswordResetView.as_view(template_name='password_reset.html',form_class=PasswordResetForm),name='password_reset'),
    path('passwordResetdone/',auth_view.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('PasswordResetConfirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('passwordresetcomplete/',auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),

    # CART
    path('addtocart/',views.addtocart,name='add-to-cart'),
    path('cart/',views.showcart,name='showcart'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),

    # path
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart,name='removecart'),


    # payment
    path('paymentdone/',views.payment_done,name='payment_done'),
    path('order/',views.order ,name='order'),


    # WhishList

    path('pluswhishlist/',views.pluswishlist,name='wishlistplus'),
    path('minuswhishlist/',views.minuswhishlist,name='whishremoved'),

    # search
    path('search/',views.search,name='search')



]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_header='Ayjas Diary'
admin.site.site_title='Ayjas Diary'
admin.site.site_index_title=' Welcome to Ayjas Diary'

