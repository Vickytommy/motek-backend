# utils.py

import requests
import json
from django.conf import settings

def send_sms_via_activetrail(person_name, phone_number, ticket_link):
    """
    Send an SMS using ActiveTrail's API.

    Parameters:
    - recipient_number (str): The recipient's phone number in international format (e.g., '+1234567890').
    - message (str): The message content.

    Returns:
    - dict: Response from ActiveTrail API.
    """
    url = f"{settings.ACTIVETRAIL_API_BASE_URL}/smscampaign/OperationalMessage/"
    
    message = f'שלום {person_name}, מצורפים הכרטיסים לאירוע "עושים באזז לסביבה", אנא הצג אותם בכניסה לאירוע.\n'
    message += "חשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.\n"
    message += f"כדי לצפות בכרטיסים יש ללחוץ על הלינק הבא: \n{ticket_link}"
    
    headers = {
        'Authorization': f"Bearer {settings.ACTIVETRAIL_ACCESS_TOKEN}",
        'Content-Type': 'application/json',
    }
    
    
    # Request body
    payload = {
        "details": {
            "unsubscribe_text": "TEST UNSUB TEXT",
            "can_unsubscribe": False,
            "name": "James",
            "from_name": "KKL",
            "sms_sending_profile_id": 5,
            "content": message
        },
        "scheduling": {
            "send_now": True
        },
        "mobiles": [
            {"phone_number": phone_number}
        ]
    }

 # Send POST request
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raises an error for HTTP codes 400+
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
    
    # response = requests.post(url, json=payload, headers=headers)
    # return response.json()
