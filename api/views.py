from django.shortcuts import render
from rest_framework import viewsets
from .models import RegisteredUser, UserLimit
from .serializers import RegisteredUserSerializer
from django.http import JsonResponse
from .utils import send_sms_via_activetrail
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
    # print('[The serializer - ] ',
    #        request.POST.get("time"),
    #        request.POST.get("date"),
    #        )
    
    date_map = {
        1: 'יום שני 15.04.25',
        2: 'יום שלישי 16.04.25',
        3: 'יום רביעי 17.04.25'
    }

    time_map = {
        1: 'מחזור א’: 9:00-12:00',
        2: 'מחזור ב’: 14:00-17:30'
    }

    if request.method == "POST":
        if RegisteredUser.objects.count() >= UserLimit.count:
            return JsonResponse({"error": "User limit reached"}, status=400)
        
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
            date = date_map[int(request.POST.get("date"))]
            time = time_map[int(request.POST.get("time"))]

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
                ticket6=ticket6,
                date=date,
                time=time
            )

            return JsonResponse({"message": "Registration successful!"}, status=201)

        except Exception as e:
            print('[Error - ] ', e)
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request"}, status=400)


def notify_user(request):
    person_name = "John Doe"
    phone_number = "+2349123254011"  # Example phone number
    ticket_link = "https://example.com/ticket"

    response = send_sms_via_activetrail(person_name, phone_number, ticket_link)

    print(response)
    return JsonResponse(response)


