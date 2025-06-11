from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_appointment_email(appointment):
    patient = appointment.patient_id
    doctor = appointment.doctor_id

    # Get emails
    patient_email = getattr(getattr(patient, 'patient_id', patient), 'email', None)
    doctor_email = getattr(getattr(doctor, 'doctor_id', doctor), 'email', None)

    subject = "Appointment Confirmation"

    context = {
        "patient_name": getattr(getattr(patient, 'patient_id', patient), 'name', ''),
        "doctor_name": getattr(getattr(doctor, 'doctor_id', doctor), 'name', ''),
        "date": appointment.date,
        "day": appointment.day,
        "from_time": appointment.from_time,
        "to_time": appointment.to_time,
        "reserve_status": appointment.reserve_status,
        "reason_of_visit": appointment.reason_of_visit,
        "doctor_location": getattr(doctor, 'location', ''),
    }

    html_content = render_to_string('emails/appointment_confirmation.html', context)
    text_content = strip_tags(render_to_string('emails/appointment_confirmation.txt', context))

    recipients = []
    if patient_email:
        recipients.append(patient_email)
    if doctor_email:
        recipients.append(doctor_email)

    if recipients:
        email = EmailMultiAlternatives(
            subject,
            text_content,
            settings.EMAIL_HOST_USER,
            recipients,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()