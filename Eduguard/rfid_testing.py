import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Get the current working directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the JSON file
cred_path = os.path.join(current_dir, 'eduguard.json')

cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Specify the collection and document name
collection_name = 'scanned_data'
document_name = 'subject'

# Check if the document exists and clear data if it does
doc_ref = db.collection(collection_name).document(document_name)
document = doc_ref.get()

if document.exists:
    # Document exists, clear the data
    doc_ref.set({'data': []})
    scanned_data = []
else:
    # Document doesn't exist, initialize with empty data
    scanned_data = []

def add_or_remove_data(data_to_add):
    """Add data based on RFID reading."""
    # Add data to the list
    if data_to_add not in scanned_data:
        scanned_data.append(data_to_add)
    else:
        scanned_data.remove(data_to_add)  # Remove if it's already in the list

    # Update the document in Firestore
    doc_ref.set({'data': scanned_data})

# RFID to subject mapping
rfid_to_subject = {
    '1': 'Physics',
    '2': 'Chemistry',
    '3': 'Maths',
    '4': 'Biology',
    '5': 'Social Studies',
    '6': 'Sanskrit',
    '7': 'Drawing',
    '8': 'English'
}

# Manual input loop
print("Enter RFID readings ('exit' to quit):")
while True:
    # Manually input RFID reading
    line = input("Enter RFID reading: ").strip()

    if line == "exit":
        break

    # Process and use the received data
    if line:
        # Map RFID reading to subject name
        data_to_add = rfid_to_subject.get(line, line)  # Default to the raw input if not found
        print(f'Received data: {data_to_add}')

        add_or_remove_data(data_to_add)

# Close the Firestore client
firebase_admin.delete_app(firebase_admin.get_app())
