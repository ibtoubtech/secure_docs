from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Document, DocumentShare
from django.contrib import messages
from django.conf import settings
import base64
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()

# Définition des vues

@login_required
def upload_document(request):
    """Vue pour le téléversement d'un document"""
    if request.method == 'POST':
        title = request.POST.get('title')
        file = request.FILES.get('file')
        
        if file and title:
            # Création et chiffrement du document
            document = Document(
                user=request.user,
                title=title,
                original_filename=file.name,
                content_type=file.content_type
            )
            document.encrypt_file(file.read())
            document.save()
            messages.success(request, 'Document téléversé avec succès !')
            return redirect('documents:list')
        else:
            messages.error(request, 'Erreur lors du téléversement du document.')
        
    return render(request, 'documents/upload.html')

@login_required
def document_list(request):
    """Vue pour afficher la liste des documents de l'utilisateur"""
    documents = Document.objects.filter(user=request.user)
    return render(request, 'documents/list.html', {'documents': documents})

@login_required
def download_document(request, document_id):
    """Vue pour télécharger un document déchiffré"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    decrypted_content = document.decrypt_file()
    
    # Préparation de la réponse HTTP avec le fichier déchiffré
    response = HttpResponse(decrypted_content, content_type=document.content_type)
    response['Content-Disposition'] = f'attachment; filename="{document.original_filename}"'
    return response

@login_required
def delete_document(request, document_id):
    """Vue pour supprimer un document"""
    try:
        document = Document.objects.get(id=document_id, user=request.user)
        if request.method == 'POST':
            document.delete()
            messages.success(request, 'Document supprimé avec succès.')
            return redirect('documents:list')
        return render(request, 'documents/delete_confirm.html', {'document': document})
    except Document.DoesNotExist:
        messages.error(request, 'Document non trouvé.')
        return redirect('documents:list')

@login_required
def share_document(request, document_id):
    """Vue pour partager un document avec un autre utilisateur"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            # Vérifier si l'utilisateur existe
            try:
                target_user = User.objects.get(email=email)
                
                # Ne pas permettre le partage avec soi-même
                if target_user == request.user:
                    messages.error(request, 'Vous ne pouvez pas partager un document avec vous-même.', extra_tags='danger')
                    return redirect('documents:share', document_id=document_id)
                
                # Vérifier si le document est déjà partagé avec cet email
                share, created = DocumentShare.objects.get_or_create(
                    document=document,
                    shared_with_email=email,
                    defaults={'shared_by': request.user}
                )
                
                if created:
                    messages.success(request, f'Document partagé avec {email}')
                else:
                    messages.info(request, f'Le document est déjà partagé avec {email}')
                    
                return redirect('documents:list')
                
            except User.DoesNotExist:
                messages.error(request, f'Aucun utilisateur trouvé avec l\'adresse email {email}', extra_tags='danger')
                return redirect('documents:share', document_id=document_id)
        else:
            messages.error(request, 'Veuillez fournir une adresse email valide.', extra_tags='danger')
    
    return render(request, 'documents/share.html', {'document': document})

@login_required
def shared_with_me(request):
    """Vue pour afficher les documents partagés avec l'utilisateur"""
    shared_documents = Document.objects.filter(
        shares__shared_with_email=request.user.email,
        shares__is_active=True
    ).distinct()
    return render(request, 'documents/shared_with_me.html', {'documents': shared_documents})

@login_required
def download_shared_document(request, document_id):
    """Vue pour télécharger un document partagé"""
    document = get_object_or_404(
        Document,
        id=document_id,
        shares__shared_with_email=request.user.email,
        shares__is_active=True
    )
    decrypted_content = document.decrypt_file()
    
    response = HttpResponse(decrypted_content, content_type=document.content_type)
    response['Content-Disposition'] = f'attachment; filename="{document.original_filename}"'
    return response

@login_required
def manage_shares(request, document_id):
    """Vue pour gérer les partages d'un document"""
    document = get_object_or_404(Document, id=document_id, user=request.user)
    shares = document.shares.all()
    
    if request.method == 'POST':
        share_id = request.POST.get('share_id')
        action = request.POST.get('action')
        
        if share_id and action == 'revoke':
            share = get_object_or_404(DocumentShare, id=share_id, document=document)
            share.is_active = False
            share.save()
            messages.success(request, f'Partage révoqué pour {share.shared_with_email}')
        
    return render(request, 'documents/manage_shares.html', {
        'document': document,
        'shares': shares
    })
