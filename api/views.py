from django.shortcuts import render
from rest_framework import viewsets
from .models import RegisteredUser, UserLimit
from .serializers import RegisteredUserSerializer
from django.http import JsonResponse
from .utils import send_email_via_activetrail, send_sms_via_activetrail
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
    day_map = {
        1: 'יום שני 15.04.25',
        2: 'יום שלישי 16.04.25',
        3: 'יום רביעי 17.04.25'
    }

    time_map = {
        1: 'מחזור א’: 9:00-12:30',
        2: 'מחזור ב’: 14:00-17:30'
    }

    if request.method == "POST":
        print('[Processing post request]')
        if RegisteredUser.objects.filter(id_card=request.POST.get("id_card")).exists():
            # ID card already registered
            print('[Id card exists]')
            return JsonResponse({"message": "לא ניתן להירשם עם פרטים אלו. מספר הטלפון ו/או האימייל כבר קיימים במערכת"}, status=400)
        
        if RegisteredUser.objects.filter(mail=request.POST.get("mail")).exists():
            # Email already registered
            print('[Email exists]')
            return JsonResponse({"message": "לא ניתן להירשם עם פרטים אלו. מספר הטלפון ו/או האימייל כבר קיימים במערכת"}, status=400)
        
        try:
            firstname = request.POST.get("firstname")
            lastname = request.POST.get("lastname")
            mobile = request.POST.get("mobile")
            mail = request.POST.get("mail")
            id_card = request.POST.get("id_card")
            city = request.POST.get("city")
            number_of_tickets = request.POST.get("num_tickets")
            extra_name1 = request.POST.get("ticket1", "")
            extra_name2 = request.POST.get("ticket2", "")
            extra_name3 = request.POST.get("ticket3", "")
            extra_name4 = request.POST.get("ticket4", "")
            extra_name5 = request.POST.get("ticket5", "")
            extra_name6 = request.POST.get("ticket6", "")
            date = day_map[int(request.POST.get("date"))]
            time = time_map[int(request.POST.get("time"))]

            user_limit_entry = UserLimit.objects.filter(ticket_day=date, ticket_time=time).first()
            user_limit_current = user_limit_entry.current_count
            user_limit = user_limit_entry.cycle_count

            if user_limit_current >= user_limit:
                # User limit reached
                return JsonResponse({"message": "ההרשמה סגורה"}, status=400)

            user = RegisteredUser.objects.create(
                firstname=firstname,
                lastname=lastname,
                mobile=mobile,
                mail=mail,
                id_card=id_card,
                city=city,
                number_of_tickets=number_of_tickets,
                extra_name1=extra_name1,
                extra_name2=extra_name2,
                extra_name3=extra_name3,
                extra_name4=extra_name4,
                extra_name5=extra_name5,
                extra_name6=extra_name6,
                date=date,
                time=time
            )

            user_limit_entry.current_count = user_limit_current + 1
            user_limit_entry.save()
            print('[User saved]')

            try:
                send_sms_via_activetrail(firstname, mobile, user.id)
                send_email_via_activetrail(firstname, mail, user.id)
                print('[sms & email sent]')
            except:
                print('[Error - ] ', e)
                return JsonResponse({"message": "הרישום נכשל"}, status=400)

            # Registration successful
            return JsonResponse({"message": "הרישום בוצע בהצלחה"}, status=201)

        except Exception as e:
            print('[Error - ] ', e)
            return JsonResponse({"message": "הרישום נכשל"}, status=400)

    print('[Method is not POST]')
    # Invalid request
    return JsonResponse({"message": "הרישום נכשל"}, status=400)


def notify_user(request):
    # person_name = "Victor"
    # phone_number = "+2349123254011"  # Example phone number
    # email = "vickytommy785@gmail.com"
    # ticket_link = "https://example.com/ticket"

    response = send_sms_via_activetrail('Victor', '9123254011', 34)
    response2 = send_email_via_activetrail('Victor', 'vickytommy785@gmail.com', 34)
    # response = send_sms_via_activetrail(person_name, phone_number, ticket_link)
    # response2 = send_email_via_activetrail(person_name, email, ticket_link)

    print(response, '\n\n')
    print(response2)
    return JsonResponse(response)


