import os
from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Step 1: Initialize the Flask application
app = Flask(__name__)

# Step 2: Get the full path to the Firebase credentials JSON file
current_dir = os.path.dirname(os.path.abspath(__file__))
cred_path = os.path.join(current_dir, 'eduguard.json')

# Step 3: Initialize Firebase Admin SDK with the credentials
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred)

# Step 4: Create a Firestore client
db = firestore.client()

# Step 5: Route for the home page which handles timetable creation
@app.route("/", methods=["GET", "POST"])
def create_timetable():
    success_message = ""
    if request.method == "POST":
        try:
            # Step 6: Retrieve form data: studentID, day, and number of subjects
            studentID = request.form.get("studentID")
            day = request.form.get("day")
            numbers = request.form.get("numbers")
            number = int(numbers)  # Convert number of subjects to integer
            items = []  # Initialize list to store subjects

            # Step 7: Collect subjects from form inputs
            for i in range(number):
                subject = request.form.get(f"subject{i}")
                if subject:
                    items.append(subject)
                else:
                    raise ValueError("All subjects must be selected.")

            # Step 8: Create and store the timetable in Firestore
            timetable = {"subjects": items}
            timetable_ref = db.collection(studentID).document(day)
            timetable_ref.set(timetable)

            # Step 9: Set success message if timetable creation is successful
            success_message = f"Success! Your timetable for {day} has been created."
        except Exception as e:
            # Step 10: On error, set failure message and print the error
            success_message = "Failed to create timetable. Please try again."
            print(f"Error: {e}")

    # Step 11: Render the HTML template with the success message
    return render_template("index.html", success_message=success_message)

# Step 12: Run the Flask application in debug mode
if __name__ == "__main__":
    app.run(debug=True)
