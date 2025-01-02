from rest_framework import serializers
from patients.models import Patient

class PatientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'

from core.models import Case
class CaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = '__all__'


from rest_framework import serializers
from core.models import Case, Treatment, LabResult, Immunization


class LabResultSerializer(serializers.ModelSerializer):
    treatment_name = serializers.CharField(source='treatment.treatment_name', read_only=True)

    class Meta:
        model = LabResult
        fields = ['id', 'test_name', 'test_date', 'result', 'treatment_name']

class ImmunizationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)

    class Meta:
        model = Immunization
        fields = ['id', 'vaccine_name', 'vaccine_date', 'description', 'doctor_name']



class TreatmentSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.username', read_only=True)
    patient_name = serializers.CharField(source='case.patient.full_name', read_only=True)
    lab_results = LabResultSerializer(many=True, read_only=True)
    immunizations = ImmunizationSerializer(many=True, read_only=True)


    class Meta:
        model = Treatment
        fields = ['id', 'treatment_type', 'description', 'treatment_name', 'treatment_date', 'doctor_name', 'patient_name','lab_results',
            'immunizations',]


class CaseDetailSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.full_name', read_only=True)
    treatments = TreatmentSerializer(many=True, read_only=True)

    class Meta:
        model = Case
        fields = [
            'id',
            'patient_name',
            'status',
            'initial_diagnosis',
            'treatment_plan',
            'closure_info',
            'notes',
            'start_date',
            'end_date',
            'treatments',
        ]

from core.models import CheckUp
class CheckUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckUp
        fields = ['id', 'case', 'nurse','date', 'time', 'bp', 'pr', 'rr', 't', 'input', 'output', 'additional_information']
        read_only_fields = ['date', 'time']

class AddCheckUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckUp
        fields = ['case', 'nurse', 'bp', 'pr', 'rr', 't', 'input', 'output', 'additional_information']
        read_only_fields = ['date', 'time']

from patients.models import Bed
class BedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bed
        fields = ['id', 'bed_number', 'room_number']


class PatientDetailSerializer(serializers.ModelSerializer):
  bed = BedSerializer(read_only=True)

  class Meta:
      model= Patient
      fields = ['id', 'full_name', 'address', 'email', 'phone_number', 'marital_status', 'gender', 'age','date_of_birth','emergency_contact', 'is_active', 'bed' ]
