from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.views import LoginView

class CustomLoginView(LoginView):
    """Vue personnalisée pour la page de connexion"""
    template_name = 'registration/login.html'
    
    def get_context_data(self, **kwargs):
        """Ajoute des données supplémentaires au contexte de la vue"""
        context = super().get_context_data(**kwargs)
        context['is_login_page'] = True
        return context

def register(request):
    """Vue pour l'inscription des nouveaux utilisateurs"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Spécification du backend d'authentification
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, 'Inscription réussie !')
            return redirect('documents:list')
        else:
            # Affichage des erreurs de validation du formulaire
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def disconnect(request):
    """Vue pour la déconnexion des utilisateurs"""
    logout(request)
    messages.success(request, 'Vous avez été déconnecté avec succès.')
    return redirect('login')
