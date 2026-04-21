# CoDrive - Ride-Sharing DevSecOps System 🚗

Ce projet démontre une architecture logicielle moderne intégrant les principes du **Développement**, de la **Sécurité** et des **Opérations** (DevSecOps).

## 🌟 Points Forts du Projet
- **Logique Métier Robuste** : Système de quota de trajets (anti-abus) validé par tests unitaires.
- **Sécurité Native** : Scan de vulnérabilités automatisé à chaque build.
- **Infrastructure Immutable** : Déploiement Cloud automatisé via Terraform.

## 🏗 Architecture


- **Backend** : FastAPI (Python)
- **Database** : PostgreSQL
- **Containerization** : Docker / Docker-Compose
- **IA/ML Ready** : Structure prête pour l'intégration d'algorithmes d'optimisation de trajets.

## 🚀 Pipeline CI/CD (GitHub Actions)
Le pipeline exécute automatiquement :
1. **Backend Quality** : Tests unitaires avec `pytest`.
2. **Container Security** : Analyse d'image avec `Trivy`.
3. **IaC Validation** : Vérification de la configuration `Terraform`.