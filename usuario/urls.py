from django.urls import path
from usuario import views

urlpatterns = [
    path('usuarios/', views.UsuarioList.as_view()),
    path('usuarios/<int:pk>/creditar/', views.UsuarioCredito.as_view()),
    path('usuarios/<int:pk>/debitar/', views.UsuarioDebito.as_view()),
    path('usuarios/<int:pk>/', views.UsuarioDetail.as_view()),
    path('usuarios/<int:pk>/extrato/', views.UsuarioExtrato.as_view()),
]
