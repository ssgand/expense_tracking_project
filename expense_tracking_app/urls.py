from rest_framework.routers import DefaultRouter
from .views import (
    ExpensesViewSet,
    SignupView,
    LoginView,
    ProfileView,
    LogoutView,
    ChangePasswordView,
    RecurringExpensesViewSet,
    CategoriesViewSet,
    BudgetsViewSet,
)

from django.urls import path

router = DefaultRouter()
router.register(r'expenses', ExpensesViewSet, basename='expenses')
router.register(r'recurring-expenses', RecurringExpensesViewSet, basename='recurring-expenses')
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'budgets', BudgetsViewSet, basename='budgets')


urlpatterns = router.urls

urlpatterns += [
    path('auth/register/', SignupView.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('auth/user/', ProfileView.as_view()),
    path('auth/logout/', LogoutView.as_view()),
    path('auth/change-password/', ChangePasswordView.as_view())
]
