import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import requests
from rest_framework.pagination import PageNumberPagination


from rest_framework.decorators import api_view

from .models import Bitcoin
from .serializers import FetchSerializers, ListSerializers

from users.views import isAuthenticated

# Create your views here.

#Fetching current price of Bitcoin using Binance API and saving into the database
@api_view(http_method_names=['POST'])
def fetch_price(request):
    if request.method == "POST":
        try:
            user = isAuthenticated(request) #Checking for user authentication
            if not user:
                return Response(({'message': "User Not Logged In"}),
                                status=status.HTTP_400_BAD_REQUEST)

            #Using binance API
            url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"

            # requesting data from url
            data = requests.get(url)
            data = json.loads(data.text)
            price_dict = dict()
            price_dict['price'] = float(data['price'])
            data = price_dict
            required_data = dict(data)

            serialized_data = FetchSerializers(data=required_data)
            if serialized_data.is_valid():
                serialized_data.save()
                return Response(({
                    'message': 'Succesfully fetched and added to database',
                    'details': serialized_data.data,
                }),status=status.HTTP_200_OK)
            else:
                return Response(({
                    'message': "Error Occured",
                }), status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(({'message': "Exception found while fetching data"}),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(({'message': "Invalid Request"}), status=status.HTTP_400_BAD_REQUEST)


#Listing all the saved price list of bitcoin after fetching from database
@api_view(http_method_names=['GET'])
def list_price(request):
    if request.method == "GET":
        try:
            user = isAuthenticated(request) #Checking for user authentication
            if not user:
                return Response(({'message': "User Not Logged In"}),
                                status=status.HTTP_400_BAD_REQUEST)

            paginator = PageNumberPagination()
            data = Bitcoin.objects.all()
            total_count = data.count()
            required_page = paginator.paginate_queryset(data, request)
            serialized_data = ListSerializers(
                required_page, many=True).data
            

            if not request.GET.get('page'):
                return Response(({"message": "Please provide the page number. eg: ?page=1"}),
                                status=status.HTTP_400_BAD_REQUEST)
            page_number = request.GET.get('page')
            if paginator.get_next_link() == None:
                next_page = None
            else:
                next_page = int(page_number) + 1

            if paginator.get_previous_link() == None:
                previous_page = None
            else:
                previous_page = int(page_number) - 1

            return Response(({
                'message': 'Price lists fetched successfully',
                'total_count': total_count,
                'next_page': next_page,
                'previous_page': previous_page,
                'list_details': serialized_data
            }),status=status.HTTP_200_OK)

        except Exception as e:
            return Response(({'message': "Exception found while fetchig price lists"}),
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(({'message': "Invalid Request"}), status=status.HTTP_400_BAD_REQUEST)
