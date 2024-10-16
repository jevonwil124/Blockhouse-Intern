from django.urls import path
from .views import backtest

urlpatterns = [
    path('api/backtest/', backtest, name='backtest'),
]

urlpatterns += [
    path('api/predict/', predict, name='predict'),
]

urlpatterns += [
    path('api/report/<str:symbol>/', report, name='generate_report'),
]

