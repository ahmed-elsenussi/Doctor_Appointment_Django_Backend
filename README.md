# Doctor Appointment System – Backend

This is the backend part of a full-stack project designed to connect doctors and patients by enabling online appointment reservations. The project was developed under the supervision of the **Information Technology Institute (ITI), Minya Branch**.

## 🩺 Project Description

This backend system supports a healthcare platform where patients can book appointments with doctors. It handles core functionalities such as:

- Doctor and patient management
- Appointment scheduling
- Notifications
- User authentication and management

Built using **Django**, the project is structured into multiple apps to ensure modularity and maintainability.

## 📁 Project Structure

```
DoctorAppointmentSystemBackend/
├── appointment/       # Manages appointments between patients and doctors
├── doctor/            # Handles doctor-related data
├── notification/      # Sends notifications (e.g., appointment confirmations)
├── patient/           # Manages patient data
├── user/              # Custom user management and authentication
├── DoctorAppointmentSystemBackend/  # Main Django settings and routing
├── manage.py          # Django project management script
├── note.txt           # Additional developer notes
```

Each app contains:

- `models.py` – Database models
- `views.py` – API views
- `admin.py` – Django admin configuration
- `apps.py`, `migrations/`, `tests.py`, etc.

## 🛠️ Technologies Used

- Python 3.12
- Django (Backend Framework)
- SQLite (Default development database)

## 🚀 Getting Started

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd DoctorAppointmentSystemBackend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

4. **Run the server:**
   ```bash
   python manage.py runserver
   ```

## 👨‍💻 Developed Under Supervision Of

**Information Technology Institute (ITI), Minya Branch**
