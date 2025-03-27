# utils.py

import requests
import json
from django.conf import settings
from .models import RegisteredUser

def send_sms_via_activetrail(person_name, phone_number, user_id):
    """
    Send an SMS using ActiveTrail's API.

    Parameters:
    - recipient_number (str): The recipient's phone number in international format (e.g., '+1234567890').
    - message (str): The message content.

    Returns:
    - dict: Response from ActiveTrail API.
    """
    url = f"{settings.ACTIVETRAIL_API_BASE_URL}/smscampaign/OperationalMessage"

    # Retrieve the user from the user_id
    user = RegisteredUser.objects.get(id=user_id)

    # Construct the message with the main ticket and up to 6 extra tickets from the user if they are non-empty
    ticket_links = [user.ticket] + [getattr(user, f"extra_ticket{i}") for i in range(1, 7) if getattr(user, f"extra_ticket{i}", None)]
    ticket_links_text = "\n\n".join([f"https://www.motek.co.il/media/{link}" for link in ticket_links])

    print('[Ticket sms links ] - ', ticket_links, '\n\n', ticket_links_text)

    message = f"""שלום {person_name},  
        מצורפים הכרטיסים לאירוע "עושים באזז לסביבה", אנא הצג אותם בכניסה לאירוע.

        חשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.

        כדי לצפות בכרטיסים יש ללחוץ על הלינקים הבאים: 
    """
    message = message + '\n' + ticket_links_text
    
    headers = {
        'Authorization': f"{settings.ACTIVETRAIL_ACCESS_TOKEN}",
        'Content-Type': 'application/json',
    }
    
    payload = {
        "details": {
            "unsubscribe_text": "unsubscribe",
            "can_unsubscribe": False,
            "name": "test1",
            "from_name": "test",
            "content": message,
        },
        "scheduling": {
            "send_now": True,
        },
        "mobiles": [
            {
            "phone_number": phone_number
            },
            {
            "phone_number": phone_number
            }
        ]
    }

    print('payload - ', payload, '\n\n ', json.dumps(payload))

 # Send POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an error for HTTP codes 400+
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    

def send_email_via_activetrail(person_name, mail, user_id):
    """
    Send an EMAIL using ActiveTrail's API.

    Parameters:
    - recipient_email (str): The recipient's email.
    - message (str): The message content.

    Returns:
    - dict: Response from ActiveTrail API.
    """

    url = f"{settings.ACTIVETRAIL_API_BASE_URL}/OperationalMessage/Message"

    # Retrieve the user from the user_id
    user = RegisteredUser.objects.get(id=user_id)

    # Construct the message with the main ticket and up to 6 extra tickets from the user if they are non-empty
    ticket_links = [user.ticket] + [getattr(user, f"extra_ticket{i}") for i in range(1, 7) if getattr(user, f"extra_ticket{i}", None)]
    ticket_links_text = "<br /> <br />".join([f"https://www.motek.co.il/media/{link}" for link in ticket_links])

    print('[Ticket links ] - ', ticket_links, '\n\n', ticket_links_text)
    message = f"""שלום {person_name},  
        מצורפים הכרטיסים לאירוע "עושים באזז לסביבה", אנא הצג אותם בכניסה לאירוע.

        חשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.

        כדי לצפות בכרטיסים יש ללחוץ על הלינקים הבאים: 
    """
    message = message + "<br />" + ticket_links_text
    
    
    headers = {
        'Authorization': f"{settings.ACTIVETRAIL_ACCESS_TOKEN}",
        'Content-Type': 'application/json',
    }
    
    payload = {
        "email_package": [
            {
            "email": mail,
            },
        ],
        "details": {
            "name": "name",
            "subject": "subject",
            "user_profile_id": 39897,
            "classification": "sample string 3",
        },
        "design": {
            "content": message,
            "language_type": "UTF-8",
            "body_part_format": 1,
            "add_print_button": True,
            "add_Statistics": True
        }
    }
    
    print('payload - ', payload, '\n\n ', json.dumps(payload))

 # Send POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an error for HTTP codes 400+
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
