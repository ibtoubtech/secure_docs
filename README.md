# Secure Docs

## Description

Secure Docs est une application web développée avec Django permettant la gestion et la sécurisation de documents. Elle offre des fonctionnalités telles que l'authentification des utilisateurs, le téléversement et la gestion de fichiers, ainsi que des outils d'administration pour superviser les utilisateurs et les documents.

## Fonctionnalités

- **Authentification des utilisateurs** : Inscription, connexion et gestion des comptes utilisateurs.
- **Gestion des documents** : Téléversement, téléchargement et suppression de fichiers.
- **Interface d'administration** : Supervision des utilisateurs et des documents via l'interface d'administration Django.

## Prérequis

- **Python 3.x** : Assurez-vous que Python est installé sur votre système.
- **Django** : Le framework web utilisé pour développer l'application.
- **Bibliothèques supplémentaires** : Les dépendances sont listées dans le fichier `requirements.txt`.

## Installation

1. **Cloner le dépôt**
   ```sh
   git clone https://github.com/ibtoubtech/secure_docs.git
   cd secure_docs
   ```

2. **Créer et activer un environnement virtuel**
   ```sh
   python -m venv venv
   source venv/bin/activate  # Sur Windows : venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```sh
   pip install -r requirements.txt
   ```

4. **Appliquer les migrations de la base de données**
   ```sh
   python manage.py migrate
   ```

5. **Créer un superutilisateur pour l'administration**
   ```sh
   python manage.py createsuperuser
   ```

   Suivez les instructions pour définir le nom d'utilisateur, l'adresse e-mail et le mot de passe.

6. **Collecter les fichiers statiques**
   ```sh
   python manage.py collectstatic
   ```

7. **Lancer le serveur de développement**
   ```sh
   python manage.py runserver
   ```

   L'application sera accessible à l'adresse `http://127.0.0.1:8000/`.

## Utilisation

- **Page d'accueil** : Présente une liste des documents disponibles.
- **Téléversement de documents** : Les utilisateurs peuvent téléverser de nouveaux fichiers via l'interface web.
- **Gestion des utilisateurs et des documents** : Accessible via l'interface d'administration Django à `http://127.0.0.1:8000/admin/`.

## Structure du projet

- **documents/** : Contient les fichiers téléversés par les utilisateurs.
- **secure_docs_project/** : Répertoire principal de l'application Django.
- **staticfiles/** : Contient les fichiers statiques collectés.
- **templates/** : Contient les modèles HTML utilisés par l'application.
- **manage.py** : Script de gestion pour interagir avec l'application Django.

## Sécurité

- **Gestion des utilisateurs** : L'application utilise le système d'authentification intégré de Django pour sécuriser l'accès aux fonctionnalités.
- **Protection des documents** : Assurez-vous que les permissions sur le répertoire `documents/` sont correctement configurées pour protéger les fichiers téléversés.

## Déploiement

Pour déployer l'application en production, envisagez d'utiliser un serveur web comme **Gunicorn** couplé à un serveur proxy tel que **Nginx**. Assurez-vous également de configurer correctement les paramètres de sécurité et de base de données dans le fichier `settings.py`.

## Auteur

- **BAH Ibrahima Toubbou** - [GitHub](https://github.com/ibtoubtech)
- **Alpha KANE**
- **Adama DIOP**
- **Mouhamadou Bamba FALL**
- **Oumaima El OUALID**
- **Elhadj A. BALDÉ**

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

