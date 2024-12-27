import random
from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth import get_user_model
from patients.models import (
    Patient, Insurance, Bed
)
from core.models import (
    Case, MedicalHistory, Treatment,
    LabResult, Immunization, CheckUp
)


class Command(BaseCommand):
    help = 'Generate fake data for patients'

    def handle(self, *args, **kwargs):

        fake = Faker()
        User = get_user_model()

        # Clear existing data
        Patient.objects.all().delete()
        User.objects.filter(role__in=['doctor', 'nurse']).delete()

        # Create doctors and nurses
        doctors = [User.objects.create_user(username=f"doctor{i}", password="password", role="doctor") for i in range(10)]
        nurses = [User.objects.create_user(username=f"nurse{i}", password="password", role="nurse") for i in range(10)]

        # Create patients
        for _ in range(30):
            patient = Patient.objects.create(
                full_name=fake.name(),
                address=fake.address(),
                email=fake.email(),
                phone_number=fake.phone_number(),
                marital_status=random.choice(['single', 'married', 'divorced', 'widowed']),
                gender=random.choice(['male', 'female']),
                age=random.randint(1, 99),
                date_of_birth=fake.date_of_birth(),
                emergency_contact={"name": fake.name(), "phone": fake.phone_number()},
            )

            # Assign nurses to the patient
            patient.assigned_nurses.set(random.sample(nurses, random.randint(2, 3)))

            # Create insurance for the patient
            Insurance.objects.create(
                patient=patient,
                provider_name=fake.company(),
                policy_number=fake.bothify(text="???-########"),
                coverage_start_date=fake.date_this_decade(),
                coverage_end_date=fake.date_this_decade(),
                coverage_details=fake.text(max_nb_chars=200)
            )

            # Create a medical history for the patient
            MedicalHistory.objects.create(
                patient=patient,
                history={"allergies": "penicillin", "past_conditions": "asthma"}
            )

            # Create cases for the patient
            for i in range(random.randint(1, 3)):
                if i == 0:
                    open_case = 'open'
                else:
                    open_case = 'closed'

                case = Case.objects.create(
                    patient=patient,
                    status=open_case,
                    initial_diagnosis={"symptoms": fake.sentence()},
                    treatment_plan={"medications": "paracetamol", "follow_up": fake.sentence()},
                    closure_info={"details": fake.text(max_nb_chars=100)} if open_case == 'closed' else None,
                    notes=fake.paragraph()
                )

                # Create treatments for the case
                for _ in range(random.randint(1, 3)):
                    treatment = Treatment.objects.create(
                        case=case,
                        treatment_type=fake.word(),
                        description={"details": fake.text()},
                        treatment_name=fake.word(),
                        doctor=random.choice(doctors)
                    )

                    # Create lab results for the treatment
                    for _ in range(random.randint(0, 2)):
                        LabResult.objects.create(
                            treatment=treatment,
                            test_name=fake.word(),
                            test_date=fake.date_this_year(),
                            result={"values": fake.random_int()},
                        )

                    # Create immunizations for the treatment
                    for _ in range(random.randint(0, 2)):
                        Immunization.objects.create(
                            treatment=treatment,
                            vaccine_name=fake.word(),
                            vaccine_date=fake.date_this_year(),
                            description={"notes": fake.sentence()},
                            doctor=random.choice(doctors)
                        )

                # Create checkups for the case
                for _ in range(random.randint(1, 5)):
                    CheckUp.objects.create(
                        case=case,
                        nurse=random.choice(nurses),
                        bp=f"{random.randint(90, 120)}/{random.randint(60, 80)}",
                        pr=f"{random.randint(60, 100)} bpm",
                        rr=f"{random.randint(12, 20)} breaths/min",
                        t=f"{random.uniform(36.5, 37.5):.1f} °C",
                        input=fake.paragraph(),
                        output=fake.paragraph(),
                        additional_information=fake.paragraph()
                    )

        # Create beds
        for room_number in range(1, 6):
            for bed_number in range(1, 4):
                Bed.objects.create(
                    room_number=room_number,
                    bed_number=bed_number,
                    status='available',
                )

        print("Fake data generated successfully!")

