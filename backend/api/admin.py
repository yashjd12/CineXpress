from django.contrib import admin

from api.models import RazorpayPayment,BookedSeat, Movie, UpcomingMovie, User

# Register your models here.
admin.site.register(Movie)
admin.site.register(UpcomingMovie)
admin.site.register(User)
admin.site.register(BookedSeat)
admin.site.register(RazorpayPayment)