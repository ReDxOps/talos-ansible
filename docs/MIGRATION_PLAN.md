# 📅 PLAN DE MIGRATION TALOS

![Status](https://img.shields.io/badge/Plan-Actif-blue?style=for-the-badge)

> [!TIP]
> Ce plan est un guide "Zero-to-Hero". Il couvre le cycle de vie complet, de l'effacement total à la maintenance long terme.

---

## 🛑 PRÉ-REQUIS PILOTAGE

*   [x] **Machine** : Workstation avec Vagrant + VMware/VirtualBox.
*   [x] **Code** : VS Code + Ansible Core + Git.
*   [x] **Mentalité** : "Cattle not Pets" (On ne s'attache pas au serveur).

---

## ☢️ PHASE 0 : LE GRAND RESET
**Situation :** Serveur compromis ou instable. Besoin de repartir de zéro.

> [!CAUTION]
> **RISQUE DE PERTE DE DONNÉES TOTALE.** Exécutez cette phase uniquement si vous êtes sûr de vos backups.

1.  **Freeze** : `docker stop $(docker ps -a -q)`
2.  **Backup Ultime** :
    *   Snapshot Kopia manuel (Tag: `PRE_WIPE`).
    *   Exfiltration `/var/lib/docker/volumes` via SCP.
3.  **Drill de Survie** : ⚠️ Tenter une restauration sur VM locale. **Si échec : ANNULER.**
4.  **WIPE** : Réinstallation Debian 12 (Netinstall).

---

## 🚀 PHASE 1 : INITIALISATION (JOUR 1)
**Objectif :** Fondations saines GitOps.

*   [ ] **GitHub** : Création Repo + Protection branche `main`.
*   [ ] **Git Security** : `.gitignore` (exclure `.vault_pass`) + **Pre-commit hooks**.
*   [ ] **Vault** : Init `secrets.yml` (AES-256).
*   [ ] **Vagrant** : Validation de l'environnement de dev local.

---

## 🐣 PHASE 1.5 : LE BOOTSTRAP
**Objectif** : Transition du serveur nu (Port 22/Root) vers cible TALOS (Port 8888/Sentinel).

1.  **Inventaire Temp** : `bootstrap_inventory.ini` (Port 22, User Root).
2.  **Playbook Bootstrap** : Exécution tags `setup_users,ssh_hardening`.
3.  **Validation** : Connexion SSH port 8888 OK ? -> Bascule sur `inventory.ini` standard.

---

## 🛡️ PHASE 2 : LE SOCLE SÉCURISÉ
**Objectif** : Transformer le serveur en forteresse.

*   [ ] **Réseau** : UFW (Allow 8888/80/443) + Sysctl Hardening.
*   [ ] **Temps** : NTP (`chrony`) actif.
*   [ ] **Docker** : Install + Config Daemon (Log Rotate `json-file`).
*   [ ] **CrowdSec** : Install + Enrôlement console.
*   [ ] **Utilisateurs** : Création `sentinel` (Sudo) + `docker user`.

> [!IMPORTANT]
> À la fin de cette phase, le **SSH Root** doit être totalement désactivé.

---

## 🔄 PHASE 3 : MIGRATION DES STACKS
**Règle d'Or** : *"Ne jamais migrer plus de 2 stacks par jour."*

### Boucle de Migration (Par Service)
1.  🕵️‍♂️ **AUDIT** : Analyse volumes/ports/env actuels.
2.  💻 **CODE** : Création Rôle Ansible (Templates J2).
3.  🧪 **TEST** : Déploiement sur Vagrant -> Validation.
4.  💾 **BACKUP** : Dump SQL Production.
5.  🛑 **CUTOVER** : Arrêt ancien service -> Deploy Ansible Prod -> Check.

---

## 👁️ PHASE 4 : OBSERVABILITÉ AVANCÉE
**Objectif** : Voir ce qui se passe sans se connecter.

*   [ ] **Stack LGT** : Loki (Logs), Promtail (Agent), Grafana.
*   [ ] **Sécurité** : Socket Proxy (Limit access) + RAM Limits.
*   [ ] **Métriques** : Node Exporter + cAdvisor.

---

## 🤖 PHASE 5 : MAINTENANCE AUTOMATISÉE (DAY-2)
**Objectif** : Dormir tranquille.

| Tâche | Fréquence | Outil |
| :--- | :--- | :--- |
| **Docker Prune** | Hebdo | Cron / Ansible |
| **Backup Verify** | Hebdo | Kopia Verify |
| **DRILL RESTORE** | **Mensuel** | **Script CI/CD (Auto-VM + Checksum)** |
| **Updates Code** | Continue | Renovate Bot |

### 🧠 Stratégie Renovate (Smart Updates)
Pour éviter la fatigue opérationnelle ("Alert Fatigue"), Renovate est configuré en mode **"Silence"** :
*   **Schedule** : PRs ouvertes uniquement le **Week-end**.
*   **Grouping** : Toutes les images Docker (`docker_image`) sont groupées dans une seule PR hebdomadaire `chore(deps): update docker images`.
*   **Automerge** : Activé pour les `patch` minors sur Dev, désactivé sur Prod.

---

## 🔮 PHASE 6 : ROADMAP CI/CD
**Futur** : Runners Self-Hosted.

1.  **Runner** : Conteneur GitHub Actions isolé sur le serveur.
2.  **Pipeline** : `.github/workflows/deploy.yml` pilote Ansible en local.
