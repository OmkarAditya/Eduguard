import os
from twilio.rest import Client
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Twilio credentials
account_sid = ""
auth_token = ""
twilio_phone_number = ""
recipient_phone_number = ""

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
cred_path = os.path.join(current_dir, 'eduguard.json')

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Specify the paths to the documents
document_path_1 = 'scanned_data/subject'

# Get the current day of the week
today = datetime.now().strftime('%A')  # Get the full name of the day (e.g., 'Monday')
document_path_2 = f'21BRS1643/{today}'

# Retrieve the arrays from the first document
doc_ref_1 = db.document(document_path_1)
doc_1 = doc_ref_1.get()

if doc_1.exists:
    array1 = doc_1.to_dict().get('data', [])
else:
    print(f"Document {document_path_1} does not exist.")
    array1 = []

# Retrieve the arrays from the second document
doc_ref_2 = db.document(document_path_2)
doc_2 = doc_ref_2.get()

if doc_2.exists:
    document_data = doc_2.to_dict()
    if 'subjects' in document_data:
        array2 = document_data['subjects']
    else:
        print(f"Document {document_path_2} does not contain 'subjects' field. Document contents: {document_data}")
        array2 = []
else:
    print(f"Document {document_path_2} does not exist.")
    array2 = []

# Compare the arrays bidirectionally
missing_elements = set(array2) - set(array1)
extra_elements = set(array1) - set(array2)

# Prepare the message
message_lines = []

if not missing_elements and not extra_elements:
    message_lines.append("You have not missed anything today.. Enjoy!!")
else:
    if missing_elements:
        missing_message = "Missing items in the bag:\n" + "\n".join(missing_elements)
        message_lines.append(missing_message)

    if extra_elements:
        extra_message = "Extra items in the bag:\n" + "\n".join(extra_elements)
        message_lines.append(extra_message)


message_body = "\n\n".join(message_lines)
print(message_body)

# Initialize Twilio client
client = Client(account_sid, auth_token)

# Send the SMS message
sms_message = client.messages.create(
    body=message_body,
    from_=twilio_phone_number,
    to=recipient_phone_number
)

print("SMS sent with SID:", sms_message.sid)

# Clean up Firebase app
firebase_admin.delete_app(firebase_admin.get_app())
