from django.shortcuts import render
from rest_framework import viewsets
from .models import RegisteredUser
from .serializers import RegisteredUserSerializer
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

def index(request):
    return render(request, "motek/index.html")

def users(request):
    users = RegisteredUser.objects.all()
    users_data = RegisteredUserSerializer(users, many=True).data
    return JsonResponse(users_data, safe=False)

@api_view(['POST'])
def register(request):
    print('[The serializer - ] ',
           request.POST.get("ticket1"),
           request.POST.get("ticket2"),
           request.POST.get("ticket3"),
           request.POST.get("ticket4"),
           )
    # serializer = RegisteredUserSerializer(data=request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == "POST":
        try:
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            mobile = request.POST.get("mobile")
            mail = request.POST.get("mail")
            id_card = request.POST.get("id_card")
            city = request.POST.get("city")
            number_of_tickets = request.POST.get("num_tickets")
            ticket1 = request.POST.get("ticket1", "")
            ticket2 = request.POST.get("ticket2", "")
            ticket3 = request.POST.get("ticket3", "")
            ticket4 = request.POST.get("ticket4", "")
            ticket5 = request.POST.get("ticket5", "")
            ticket6 = request.POST.get("ticket6", "")

            RegisteredUser.objects.create(
                firstname=firstname,
                lastname=lastname,
                mobile=mobile,
                mail=mail,
                id_card=id_card,
                city=city,
                number_of_tickets=number_of_tickets,
                ticket1=ticket1,
                ticket2=ticket2,
                ticket3=ticket3,
                ticket4=ticket4,
                ticket5=ticket5,
                ticket6=ticket6
            )

            return JsonResponse({"message": "Registration successful!"}, status=201)

        except Exception as e:
            print('[Error - ] ', e)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)