from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('',views.Index.as_view(),name='home'),
    path('shop/',views.Shop.as_view(),name='shop'),
    path('deals/',views.Deals.as_view(),name='deals'),
    path('cart/',views.Cart_View.as_view(),name='cart'),
    path('checkout/',views.Checkout.as_view(),name='checkout'),
    path('update_item/',views.UpdateItem.as_view(),name='update_item'),
    path('order_item_delete/<str:productid>/',views.Order_Item_Delete.as_view(),name='order_item_delete'),
    path('contact/',views.Contact.as_view(),name='contact'),
    path('search/',views.Search.as_view(),name='search'),
    path('offer/<str:keyword>/',views.Offer.as_view(),name='offer'),
    path('discount/<str:keyword>/',views.Discount.as_view(),name='discount'),
    path('about/',views.About.as_view(),name='about'),
    path('details/<str:id>',views.Detail.as_view(),name='detail'),
    path('manage_account/',login_required(views.ManageAccount.as_view()),name='manage_account'),
    path('customize_profile/',login_required(views.CustomizeProfile.as_view()),name='customize_profile'),
    path('login_security/',login_required(views.LoginSecurity.as_view()),name='login_security'),
    path('login_security/change_password/',login_required(views.ChangePassword.as_view()),name='change_password'),
    path('login_security/change_email/',login_required(views.ChangeEmail.as_view()),name='change_eamil'),
    path('your_reviews/',login_required(views.YourReviews.as_view()),name='your_reviews'),
    path('your_order/',login_required(views.YourOrder.as_view()),name='your_order'),
    path('add_review/',login_required(views.AddReview.as_view()),name='add_review'),
    path('add_review_for_account_manage/',login_required(views.AddReviewForAccountManage.as_view()),name='add_review_for_account_manage'),
    path('get_review/',login_required(views.GetReview.as_view()),name='get_review'),
    path('delete_review/',login_required(views.DeleteReview.as_view()),name='delete_review'),
    path('get_reviews/',views.GetReviews.as_view(),name='get_reviews'),
    path('subscribe/',views.Subscribe.as_view(),name='subscribe'),
    path('orders/',views.orders,name='orders'),
    path('order/<str:id>',views.order,name='order')
]