from django.urls import path
from api.views import CrawlerView,PaymentView,CallbackView,updateUserDetails,getUserDetails,bookSeat, cancelBookedSeat, getAllUsers, getBookedSeatsForMovie,getBookedSeatsForUser, loginView, movieView, searchMovies, signupView,upcomingMovieView

urlpatterns = [
    path('movies/<str:pk>',movieView.as_view(),name="movies"),
    path('upcoming-movies',upcomingMovieView.as_view(),name="upcoming-movie"),
    path('login',loginView.as_view(),name="login"),
    path('signup',signupView.as_view(),name="signup"),
    path('get-all-users',getAllUsers.as_view(),name="get-all-users"),
    path('search-movie/<str:pk>',searchMovies.as_view(),name="search-movie"),
    path('book-seat',bookSeat.as_view(),name="book-seat"),
    path('get-booked-seats-for-movie/<str:pk>',getBookedSeatsForMovie.as_view(),name="get-booked-seats-for-movie"),
    path('get-booked-seats-for-user/<str:pk>',getBookedSeatsForUser.as_view(),name="get-booked-seats-for-movie"),
    path('cancel-booked-seat',cancelBookedSeat.as_view()),
    path('get-user-details/<str:pk>',getUserDetails.as_view()),
    path('update-user-details',updateUserDetails.as_view()),
    path('razorpay_order', PaymentView.as_view(), name='razorpay_order'),
    path('razorpay_callback', CallbackView.as_view(), name='razorpay_callback'),
    path('crawl',CrawlerView.as_view(),name='web-crawler')
]