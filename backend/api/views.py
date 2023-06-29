from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
import jwt
from datetime import datetime,timedelta,timezone
from rest_framework import status
import razorpay
import json
from .models import RazorpayPayment
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

def query(q):
    with connection.cursor() as c:
        c.execute(q)
        if q[0:6].lower()=="select":
            return dictfetchall(c)
        else :
            return "success"

def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

class movieView(APIView):
    def get(self,req,pk,format=None):
        if pk=="all":
            result = query("select * from api_movie")
            return Response(result);            
        result = query(f"select * from api_movie where id={pk}")
        return Response(result)

class upcomingMovieView(APIView):
    def get(self,req,format=None):
        result = query("select * from api_upcomingmovie")
        return Response(result);    

class signupView(APIView):
    def post(self,req,format=None):
        username = req.data['username']
        password = req.data['password']
        first_name = req.data.get('first_name',"")
        last_name = req.data.get('last_name',"")
        email = req.data.get('email',"")
        if  len(query(f"select * from api_user where username='{username}'"))>0:
            return Response("Username already taken")
        newId = query("select * from api_user order by id desc")[0]['id'] + 1 
        result = query(f"insert into api_user values ('{newId}','{username}','{password}','{email}','{first_name}','{last_name}')")
        return Response("Signup success,proceed to Login")

class loginView(APIView) : 
    def post(self,req,format=None):
        response = Response()
        username = req.data['username']
        password = req.data['password']
        preuser = query(f"select * from api_user where username='{username}' and password='{password}' ")
        if len(preuser)<=0 : 
            return Response("Invalid Credentials")
        print(preuser[0])
        token = jwt.encode({"id":preuser[0]['id'],'exp': datetime.now(tz=timezone.utc)},"secret_key",algorithm="HS256")
        print(datetime.now() + timedelta(seconds=60))
        print(datetime.now())
        response.set_cookie(
            key = 'jwt', 
            value = token,
            expires = timedelta(seconds=60),
            secure = False,
            samesite = 'Lax'
        )
        preuser[0]['token'] = token
        response.data = preuser
        return response

class getAllUsers(APIView):
    def get(self,req,format=None):
        newId = query("select * from api_user order by id desc")[0]['id']
        result = query("select * from api_user")
        print(result)
        return Response(result)

class searchMovies(APIView):
    def get(self,request,pk,format=None):
        return Response(query(f"select * from api_movie where name like '%{pk}%'"))

class bookSeat(APIView):
    def post(self,req,format=None):
        userId = req.data['userId']
        movieId = req.data['movieId']
        for seat in req.data['selectedSeat']:
            preseat = query(f"select * from api_bookedseat where seat='{seat}' and userId='{userId}' and movieId='{movieId}'")
            if not preseat : 
                newId = query("select * from api_bookedseat order by id desc")[0]['id'] + 1 
                query(f"insert into api_bookedseat values('{newId}','{seat}','{userId}','{movieId}') ")
        return Response("Seats Booked successfully")

class getBookedSeatsForMovie(APIView):
    def get(self,req,pk,format=None):
        result = query(f"select seat from api_bookedseat where movieId='{pk}'")
        seats = [-1,-1]
        print(result)
        for item in result :
            seats.append(item['seat'])
        return Response(seats)

class getBookedSeatsForUser(APIView):
    def get(self,req,pk,format=None):
        result = query(f"select * from api_bookedseat join api_movie where userId='{pk}' and movieId=api_movie.id")
        return Response(result)


class cancelBookedSeat(APIView):
    def delete(self,req,format=None):
        print(req.data)
        userId = req.data['userId']
        movieId= req.data['movieId']
        seat = req.data['seat']
        query(f"delete from api_bookedseat where seat='{seat}' and userId='{userId}' and movieId='{movieId}' ")
        return Response("Booking canceled")

class getUserDetails(APIView):
    def get(self,req,pk,format=None):
        result= query(f"select * from api_user where id='{pk}' ")
        return Response(result)

class updateUserDetails(APIView):
    def put(self,req,format=None):
        print(req.data)
        id = req.data['id']
        first_name =req.data['first_name']
        last_name =req.data['last_name']
        username =req.data['username']
        email =req.data['email']
        password =req.data['password']

        result = query(f"update api_user set first_name='{first_name}',last_name='{last_name}',username='{username}',email='{email}',password='{password}' where id='{id}'")
        return Response(result)

# Get Razorpay Key id and secret for authorizing razorpay client.
RAZOR_KEY = "rzp_test_ZDi1axSFOde2A8"
RAZOR_SECRET = "x49WW98FAlDcka4WKBGmcUUe"

# Creating a Razorpay Client instance.
razorpay_client = razorpay.Client(auth=(RAZOR_KEY, RAZOR_SECRET))


class PaymentView(APIView):
    """
    APIView for Creating Razorpay Order.
    :return: list of all necessary values to open Razorpay SDK
    """

    http_method_names = ('post',)

    @staticmethod
    def post(request, *args, **kwargs):

        # Take Order Id from frontend and get all order info from Database.
        # order_id = request.data.get('order_id', None)

        # Here We are Using Static Order Details for Demo.
        name = "Swapnil Pawar"
        seats = request.data['seats']

        # Create Order
        razorpay_order = razorpay_client.order.create(
            {"amount": int(seats) * 10000, "currency": "INR", "payment_capture": "1"}
        )

        # Save the order in DB
        order = RazorpayPayment.objects.create(
            name=name, amount=seats*100, provider_order_id=razorpay_order["id"]
        )

        data = {
            "name" : name,
            "merchantId": "RAZOR_KEY",
            "amount": seats*100,
            "currency" : 'INR' ,
            "orderId" : razorpay_order["id"],
            }

        # save order Details to frontend
        return Response(data, status=status.HTTP_200_OK)

class CallbackView(APIView):
    
    """
    APIView for Verifying Razorpay Order.
    :return: Success and failure response messages
    """

    @staticmethod
    def post(request, *args, **kwargs):

        # getting data form request
        response = request.data.dict()

        """
            if razorpay_signature is present in the request 
            it will try to verify
            else throw error_reason
        """
        if "razorpay_signature" in response:

            # Verifying Payment Signature
            data = razorpay_client.utility.verify_payment_signature(response)

            # if we get here True signature
            if data:
                payment_object = RazorpayPayment.objects.get(provider_order_id = response['razorpay_order_id'])                # razorpay_payment = RazorpayPayment.objects.get(order_id=response['razorpay_order_id'])
                payment_object.status = "Success"
                payment_object.payment_id = response['razorpay_payment_id']
                payment_object.signature_id = response['razorpay_signature']          
                payment_object.save()

                return HttpResponseRedirect(redirect_to='http://localhost:3000/my-bookings')
            else:
                return Response({'status': 'Signature Mismatch!'}, status=status.HTTP_400_BAD_REQUEST)

        # Handling failed payments
        else:
            error_code = response['error[code]']
            error_description = response['error[description]']
            error_source = response['error[source]']
            error_reason = response['error[reason]']
            error_metadata = json.loads(response['error[metadata]'])
            razorpay_payment =   RazorpayPayment.objects.get(provider_order_id=error_metadata['order_id'])
            razorpay_payment.payment_id = error_metadata['payment_id']
            razorpay_payment.signature_id = "None"
            razorpay_payment.status = "Failure"
            razorpay_payment.save()

            error_status = {
                'error_code': error_code,
                'error_description': error_description,
                'error_source': error_source,
                'error_reason': error_reason,
            }

            return Response({'error_data': error_status}, status=status.HTTP_401_UNAUTHORIZED)


class CrawlerView(APIView):
    def get(self,req,format=None):
        headers = {
            'authority': 'www.imdb.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'dnt': '1',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        }
        URL = "https://www.imdb.com/calendar/?region=in"
        page = requests.get(URL,headers=headers)
        soup = BeautifulSoup(page.content,'html.parser')
        movies = soup.find_all('li',class_='ipc-metadata-list-summary-item')
        for movie in movies:
            image = movie.find('img')
            name = movie.find('a')
            print(image.attrs.get('src',None))
            print(name.text)
        # movie2 = movies.find_next()
        # print(movie2)
        return Response(str(movies))