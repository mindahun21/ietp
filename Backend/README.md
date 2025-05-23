# Smart Hospital Bed Backend
This is the backend system for the Smart Hospital Bed for Patients project, developed as part of the Integrated Engineering Team Project at Addis Ababa Science and Technology University by Group 44. The backend handles user authentication, patient data management, device integration, and administrative controls.

Developer: Mindahun Debebe (Software Engineering)

## 🌐 Overview
The backend is built using Django and Django REST Framework (DRF) to provide robust APIs and a web-based admin dashboard. It supports patient registration, vitals monitoring, treatment history, nurse assignments, and real-time device integration with the smart bed hardware and mobile app.

## 🔧 Key Features
RESTful API for patient, staff, treatment, and bed data

Admin Dashboard with Django templates for hospital staff management

User Roles & Permissions (Admin, Doctor, Nurse)

Patient Monitoring via hardware integration (Arduino sensors)

Dynamic Bed Control through API endpoints used by the Flutter mobile app

Device Data Logging to support real-time and historical health analysis

Templated Pages for staff, patients, and treatment views

## 🏗️ Project Structure
```code
main/
├── api/               # DRF API endpoints
├── core/              # Core models and admin views
├── patients/          # Patient-related models, views, and templates
├── templates/         # Base templates and layout components
├── theme/             # Tailwind-based static files
├── static/            # JS files for frontend interactivity
├── settings.py        # Project settings
├── urls.py            # Project-wide routing
```

## 🛠️ Technologies Used
- **Framework:** Django, Django REST Framework

- **Frontend (Admin):** Django Templates, Tailwind CSS

- **API Testing:** .rest files for VSCode REST Client

- **Database:** SQLite (default) – can be replaced with PostgreSQL

- **Device Communication:** Serial/Wireless interface with Arduino

- **Others:** Makefile for command automation, Tailwind CSS for styling

## 📁 Notable Directories
api/
Contains all API views, serializers, and permissions.

core/
Includes custom user models, authentication, and the admin site logic.

patients/
Handles everything related to patient records, treatments, and bed assignments.

templates/
Includes:

core/: Dashboard views and staff management

patients/: CRUD templates for patients and treatment info

theme/
Tailwind CSS setup for styling the dashboard.


👥 Contributors
Backend developed by Mindahun Debebe as part of Group 44's integrated team:

See full team credits in the main README

