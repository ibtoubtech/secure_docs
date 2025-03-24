from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import base64
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

# Création des modèles

class DocumentShare(models.Model):
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='shares')
    shared_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_documents')
    shared_with_email = models.EmailField()
    shared_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['document', 'shared_with_email']
        
    def __str__(self):
        return f"{self.document.title} partagé avec {self.shared_with_email}"


class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    file = models.BinaryField()  # Stockage du contenu du fichier chiffré
    iv = models.BinaryField(null=True)  # Stockage du vecteur d'initialisation
    salt = models.BinaryField(null=True)  # Stockage du sel pour la dérivation de clé
    original_filename = models.CharField(max_length=255)
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def _derive_key(self, salt):
        """Dérivation de la clé de chiffrement en utilisant PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 32 octets = 256 bits
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        # Décodage de la clé de chiffrement encodée en base64
        key_bytes = base64.b64decode(settings.ENCRYPTION_KEY)
        return kdf.derive(key_bytes)
    
    def encrypt_file(self, file_data):
        # Génération d'un sel et d'un IV aléatoires
        salt = os.urandom(16)
        iv = os.urandom(16)
        
        # Dérivation de la clé
        key = self._derive_key(salt)
        
        # Création de l'encrypteur
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Ajout du padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()
        
        # Chiffrement des données
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Stockage des données chiffrées, de l'IV et du sel
        self.file = encrypted_data
        self.iv = iv
        self.salt = salt
        
    def decrypt_file(self):
        if not all([self.file, self.iv, self.salt]):
            raise ValueError("Paramètres de chiffrement manquants")
            
        # Dérivation de la clé
        key = self._derive_key(self.salt)
        
        # Création du déchiffreur
        cipher = Cipher(
            algorithms.AES(key),
            modes.CBC(self.iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Déchiffrement des données
        padded_data = decryptor.update(self.file) + decryptor.finalize()
        
        # Suppression du padding
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(padded_data) + unpadder.finalize()
    
    def __str__(self):
        return f"{self.title} - {self.user.username}"
