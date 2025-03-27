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
    url = f"{settings.ACTIVETRAIL_API_BASE_URL}/smscampaign/OperationalMessage"
    
    message = f'''שלום {person_name}, מצורפים הכרטיסים לאירוע "עושים באזז לסביבה", אנא הצג אותם בכניסה לאירוע.\n'''
    message += "חשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.\n"
    message += f"כדי לצפות בכרטיסים יש ללחוץ על הלינק הבא: \n{ticket_link}"
    
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
            "content": "שלום {person_name}, מצורפים הכרטיסים לאירוע \"מותק של יער\", אנא הצג אותם בכניסה לאירוע.\nחשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.\nכדי לצפות בכרטיסים יש ללחוץ על הלינק הבא: \n{ticket_link}"
        },
        "scheduling": {
            "send_now": True,
        },
        "mobiles": [
            {
            "phone_number": "0505760215"
            },
            {
            "phone_number": "0505760215"
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
    

def send_email_via_activetrail(person_name, phone_number, ticket_link):
    """
    Send an EMAIL using ActiveTrail's API.

    Parameters:
    - recipient_email (str): The recipient's email.
    - message (str): The message content.

    Returns:
    - dict: Response from ActiveTrail API.
    """

    url = f"{settings.ACTIVETRAIL_API_BASE_URL}/campaigns/Contacts"
    
    message = f'''שלום {person_name}, מצורפים הכרטיסים לאירוע "עושים באזז לסביבה", אנא הצג אותם בכניסה לאירוע.\n'''
    message += "חשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.\n"
    message += f"כדי לצפות בכרטיסים יש ללחוץ על הלינק הבא: \n{ticket_link}"
    
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
            "content": "שלום {person_name}, מצורפים הכרטיסים לאירוע \"מותק של יער\", אנא הצג אותם בכניסה לאירוע.\nחשוב: הכרטיס הוא אישי ואינו ניתן להעברה, אורח שאין ברשותו כרטיס לא יורשה להיכנס לאירוע.\nכדי לצפות בכרטיסים יש ללחוץ על הלינק הבא: \n{ticket_link}"
        },
        "scheduling": {
            "send_now": True,
        },
        "mobiles": [
            {
            "phone_number": "0505760215"
            },
            {
            "phone_number": "0505760215"
            }
        ]
    }

    payload = {
        "campaign": {
            "send_test": "sample string 1",

            "details": {
                "name": "sample string 1",
                "subject": "sample string 2",
                "user_profile_id": 1,
                "google_analytics_name": "sample string 3",
                "sub_account_id": 1,
                "content_category_id": 1,
                "preheader": "sample string 4",
                "predictive_delivery": True,
                "segmentation_id": 1
            },

            "design": {
                "content": "sample string 1",
                "language_type": "UTF-8",
                "header_footer_language_type": "UTF-8",
                "is_add_print_email": True,
                "is_auto_css_inliner": True,
                "is_remove_system_links": False
            },

            "template": {
                "id": 1
            },

        },

        "campaign_contacts": {
            "contacts_ids": [ 1, 2 ],
            "contacts_emails": [
                "vickytommy785@gmail.com",
            ]
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
    
