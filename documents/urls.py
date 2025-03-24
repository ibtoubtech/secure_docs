from django.urls import path
from . import views
from . import auth_views

# Configuration des URLs de l'application documents
app_name = 'documents'

# Définition des chemins d'URL
urlpatterns = [
    # Gestion des documents
    path('upload/', views.upload_document, name='upload'),          # Téléversement
    path('list/', views.document_list, name='list'),               # Liste des documents
    path('download/<int:document_id>/', views.download_document, name='download'),  # Téléchargement
    path('delete/<int:document_id>/', views.delete_document, name='delete'),       # Suppression
    
    # Partage de documents
    path('share/<int:document_id>/', views.share_document, name='share'),          # Partager
    path('shared-with-me/', views.shared_with_me, name='shared_with_me'),         # Documents partagés
    path('download-shared/<int:document_id>/', views.download_shared_document, name='download_shared'),  # Télécharger partagé
    path('manage-shares/<int:document_id>/', views.manage_shares, name='manage_shares'),  # Gérer partages
    
    # Authentification
    path('disconnect/', auth_views.disconnect, name='disconnect'),  # Déconnexion
]
