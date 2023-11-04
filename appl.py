import firebase_admin

from firebase_admin import credentials, initialize_app
from firebase_admin import firestore



# Initialize Firebase
cred = credentials.Certificate('medtech-896ec-firebase-adminsdk-8q3sw-daed98cb79.json')
app=firebase_admin.initialize_app(cred)

db = firestore.Client()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        patient_specialization = request.form.get('patientSpecialization')
        patient_landmark = request.form.get('patientLandmark')
        matching_doctors = get_matching_doctors(patient_specialization, patient_landmark)
        return render_template('results.html', doctors=matching_doctors)

    return render_template('index.html')

def get_matching_doctors(specialization, landmark):
    matching_doctors = []
    doctors_data = db.collection('Doctors').where('specialization', '==', specialization).where('location', '==', landmark).stream()

    for doctor_info in doctors_data:
        doctor_data = doctor_info.to_dict()
        matching_doctors.append({
            'name': doctor_data['name'],
            'specialization': doctor_data['specialization'],
            'location': doctor_data['location'],
            'availability': doctor_data.get('availability', ''),
        })

    return matching_doctors

if __name__ == '__main__':
    app.run(debug=True)