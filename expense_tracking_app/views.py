from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.authtoken.models import Token


from .models import Expenses
from .models import RecurringExpenses
from .models import Categories
from .models import Budgets
from .serializers import ExpensesSerializer
from .serializers import SignupSerializer
from .serializers import LoginSerializer
from .serializers import ProfileSerializer
from .serializers import PasswordChangeSerializer
from .serializers import RecurringExpensesSerializer
from .serializers import CategoriesSerializer
from .serializers import BudgetsSerializer

# Create your views here.


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        token = Token.objects.create(user=user)

        return Response(
            { 
                'detail': 'User created successfully',
                'token': token.key
            },
            status=status.HTTP_201_CREATED
        )
    
class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key
        })
    
class LogoutView(APIView):
    def post(self, request):
        request.auth.delete()
        return Response({'detail': 'Logged out successfully'})
    
class ProfileView(APIView):
    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        # Verify current password
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {"current_password": "Incorrect password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(serializer.validated_data['new_password'])
        user.save()

        return Response({"detail": "Password updated successfully"})

class ExpensesViewSet(ModelViewSet):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expenses.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class RecurringExpensesViewSet(ModelViewSet):
    serializer_class = RecurringExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return expenses for the current user
        return RecurringExpenses.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically assign the logged-in user
        serializer.save(user=self.request.user)

class CategoriesViewSet(ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = [IsAuthenticated]

class BudgetsViewSet(ModelViewSet):
    serializer_class = BudgetsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budgets.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

