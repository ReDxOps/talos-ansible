# 🗺️ TALOS : Roadmap vers une CI/CD "Elite"

Ce document trace ton parcours pour transformer ta CI actuelle (Lint & Syntax) en un pipeline de déploiement industriel sécurisé.

## 🛡️ Étape 1 : Optimisation & Sécurité (Terminé ✅)
*L'objectif était de rendre ta CI actuelle plus rapide et plus "invisible".*

- [x] **Défi Caching** : Mise en cache des rôles Galaxy et des dépendances Pip avec `actions/cache`.
- [x] **Défi Auto-Cleanup** : Sécurisation "Zero-Trace" via l'approche "Elite" (secrets en mémoire uniquement via `ANSIBLE_VAULT_IDENTITY_LIST`).
- [x] **Défi Linting Strict** : Profil `production` activé dans `.ansible-lint` avec exclusion des dossiers externes.

## 🧪 Étape 2 : Simulation & Validation (Le "Debian Lab")
*L'objectif est de s'assurer que le changement est sûr avant de toucher au serveur.*

- [ ] **Défi Docker Lab** : Créer un job qui lance un conteneur `debian:stable-slim` pour servir de cible.
    *   *Question à creuser : Comment préparer l'image pour qu'elle soit "Ansible-ready" (Python) ?*
- [ ] **Défi Check Mode** : Exécuter `ansible-playbook site.yml --check` contre ce conteneur en utilisant `ansible_connection: docker`.
- [ ] **Défi Diff Check** : Cherche comment extraire uniquement les changements (`--diff`) et les afficher dans le résumé de ton run GitHub Actions.

## 🎡 Étape 3 : Déploiement Continu (Le Saint Graal)
*L'objectif est d'automatiser l'action de déploiement réel.*

- [ ] **Défi Environments** : Découvre comment configurer des "Environments" dans GitHub (Settings > Environments) pour l'approbation manuelle.
- [ ] **Défi Self-Hosted Runner** : Installer l'agent GitHub sur ton serveur pour un déploiement local sécurisé.
- [ ] **Défi Matrix Deployment** : Apprends à utiliser une `matrix` pour tester sur différentes versions d'OS.

## 📢 Étape 4 : Observabilité & Feedback
*L'objectif est de savoir ce qu'il se passe sans ouvrir GitHub.*

- [ ] **Défi Notification** : Envoyer le résultat vers Discord, Telegram ou Slack via Webhooks.
- [ ] **Défi Artifact Logging** : Sauvegarder les logs Ansible (`ansible.log`) comme un "Artifact GitHub" pour le débuggage.

---
> [!TIP]
> **Le secret de la réussite** : Ne tente pas de tout faire d'un coup. Réalise chaque défi l'un après l'autre. Chaque case cochée est une compétence SRE que tu acquiers à vie.
