from rest_framework import serializers
from .models import Expenses
from django.contrib.auth import authenticate
from .models import CustomUser
from .models import RecurringExpenses
from .models import Categories
from .models import Budgets

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        # fields = [
        #     'id',
        #     'user',
        #     'category',
        #     'amount',
        #     'currency',
        #     'description',
        #     'expense_date',
        #     'created_at',
        #     'updated_at',
        # ]
        exclude = ['user']
        # read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)

    def validate(self, data):
        user = authenticate(
            email=data['email'],
            password=data['password']
        )

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        if not user.is_active:
            raise serializers.ValidationError('User account is disabled')

        data['user'] = user
        return data
    
class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            'username',
            'email',
            'preferred_currency',
            'password',
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')

        user = CustomUser.objects.create_user(
            password=password,
            **validated_data
        )
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'preferred_currency',
            'created_at',
            'updated_at',
        ]

class PasswordChangeSerializer(serializers.Serializer):
    current_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

class RecurringExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecurringExpenses
        # user will be set automatically, category is allowed from input
        fields = (
            'id',
            'user',
            'category',
            'amount',
            'currency',
            'description',
            'next_pay_date',
            'frequency',
            'created_at',
            'updated_at'
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')
    
    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value

    def validate_next_pay_date(self, value):
        if value < datetime.date.today():
            raise serializers.ValidationError("Next pay date cannot be in the past")
        return value
    
class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = (
            'id',
            'name',
            'description',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'created_at', 'updated_at')

class BudgetsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budgets
        fields = (
            'id',
            'user',
            'category',
            'amount',
            'currency',
            'start_date',
            'end_date',
            'created_at',
            'updated_at',
        )
        read_only_fields = ('id', 'user', 'created_at', 'updated_at')

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Budget amount must be positive")
        return value

    def validate(self, attrs):
        start_date = attrs.get('start_date')
        end_date = attrs.get('end_date')

        if start_date and end_date and start_date > end_date:
            raise serializers.ValidationError(
                "Start date must be before end date"
            )

        return attrs