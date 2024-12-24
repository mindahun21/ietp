from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from .permissions import IsNurse


# Create your views here.

class CustomLoginView(APIView):
    permission_classes = [AllowAny] 
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print('username', username, 'password', password)

        
        user = authenticate(request,username=username, password=password)

        if user is None:
          return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        
        if user.role != 'nurse':
          return Response({"detail": "Access denied. User is not a nurse."}, status=status.HTTP_403_FORBIDDEN)
       
        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key,"detail":"Authenticated Successfuly"}, status=status.HTTP_200_OK)
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get the token associated with the current user
        try:
            token = Token.objects.get(user=request.user)
            token.delete()  # Delete the token to log the user out
            return Response({"detail": "Logged out successfully."}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"detail": "No active session found for the user."}, status=status.HTTP_400_BAD_REQUEST)


from patients.models import Patient
from .serializers import PatientSerializer
class PatientListView(APIView):
    permission_classes = [IsAuthenticated, IsNurse]

    def get(self, request):
        patients = request.user.patients.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data)
    


from .serializers import CaseDetailSerializer
from core.models import Case
class CaseDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            patient = Patient.objects.get(id=id)
            case = patient.cases.filter(status='open').first()
            serializer = CaseDetailSerializer(case)
            return Response(serializer.data)
        except Case.DoesNotExist:
            return Response({"detail": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
        


from .serializers import CheckUpSerializer
class CheckupsView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, id):
        try:
            case = Case.objects.get(id=id)
            checkups = case.checkups.all().order_by('-date','-time')
            serializer = CheckUpSerializer(checkups, many=True)
            return Response(serializer.data)
        except Case.DoesNotExist:
            return Response({"detail": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
        


from .serializers import AddCheckUpSerializer
class AddCheckUpView(APIView):
    def post(self, request, id):
        try:
            case = Case.objects.get(id=id)
        except Case.DoesNotExist:
            return Response({"error": "Case not found"}, status=status.HTTP_404_NOT_FOUND)
        
        data = request.data.copy()
        data['case'] = case.id
        data['nurse'] = request.user.id
        
        serializer = AddCheckUpSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'checkup':serializer.data, 'detail': 'checkup added successfuly'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

















