# 🏛️ ARCHITECTURE DU SYSTÈME TALOS

![Status](https://img.shields.io/badge/Architecture-Validée-success?style=for-the-badge)

> [!NOTE]
> Ce document constitue la **Source of Truth** technique. Toute déviation en production par rapport à ce document est considérée comme une anomalie (Drift).

---

## 1. VUE D'ENSEMBLE (GITOPS FLUX)

```text
+-----------------------+              +-----------------------------+
| ZONE DE CONTRÔLE      |              | CI/CD & AUTOMATISATION      |
| (Local)               |   Push       |                             |
| [💻 Dev] --Vagrant--> [🛠️ VM] ------>| [📦 GitHub Repo] <-> [🔍 CI] |
|                       |              |       ^                     |
+-----------------------+              |       | (PR)                |
                                       | [🤖 Renovate]               |
                                       +-------+---------------------+
                                               |
                                               | Merge
                                               v
+-----------------------+              +-----------------------------+
| DÉPLOIEMENT           |              | INFRASTRUCTURE              |
| (Mode Push)           |   Ansible    |                             |
| [👤 Admin] ------------------------->| [🚀 PROD]                   |
|    | (site.yml)       |              |                             |
|    +-------------------------------->| [🛠️ VM (Vagrant)]           |
+-----------------------+              +-----------------------------+
```

---

## 2. LE SOCLE SYSTÈME (`common`)

Configuration immuable appliquée à tous les nœuds.

### 🛡️ Sécurité & Réseau
| Composant | Configuration | Rôle |
| :--- | :--- | :--- |
| **Firewall (UFW)** | Allow: `8888`(SSH), `80`, `443` | Filtrage entrée strict |
| **CrowdSec** | **IPS Collaboratif** | Ban d'IPs malveillantes (Couche iptables) |
| **SSH** | Port **8888**, Key-Only, No-Root | Obscurité & Durcissement |
| **Kernel** | Sysctl Hardened | Anti-Spoofing, No Redirects |
| **NTP** | `systemd-timesyncd` | Synchro temps stricte (Logs/TOTP) |

### 🐳 Container Runtime (Docker)
*   **Log Driver** : `json-file` (Max 10MB x 3 fichiers) -> *Évite saturation disque*.
*   **Socket Proxy** : Tecnativa Proxy -> *Expose socket en Read-Only uniquement*.

### 👥 Gestion des Utilisateurs
*   `sentinel` : Admin opérationnel (Sudoers).
*   `root` : **Verrouillé** (SSH Login Disabled).
*   Users applicatifs : UID/GID fixes par service.

---

## 3. STANDARDISATION DES APPLICATIONS

> [!TIP]
> **Une Application = Un Rôle Ansible.** Pas d'exceptions.

### Structure Type `roles/<app>/`
*   📂 `tasks/main.yml` : Orchestration (Dirs, Templates, Compose Up).
*   📄 `templates/docker-compose.yml.j2` : Services définis en Jinja2.
*   🔐 `templates/.env.j2` : Secrets injectés via Vault.

### Règles d'Or
1.  **Isolation Réseau** : Backend isolé, seul le Proxy Front expose 80/443.
2.  **Immuabilité** : Pas de modif manuelle (`vi`) sur le serveur.
3.  **Santé** : Healthchecks obligatoires (Support `autoheal`).

---

## 4. GESTION DES DONNÉES

| Type | Stratégie | Path |
| :--- | :--- | :--- |
| **Config** | Bind Mount | `/opt/<app>/config` |
| **Data (DB)** | Docker Volume | `volume: db_data` |
| **User Data** | Bind Mount | `/mnt/data/<app>` |

---

## 5. ORCHESTRATION & PLAYBOOKS

TALOS utilise un séquençage strict en 5 phases (00 à 04) piloté par le **Master Playbook** (`site.yml`).

### 📦 Séquençage des Phases
| Phase | Playbook | Cible | Rôle |
| :--- | :--- | :--- | :--- |
| **00** | `00_bootstrap.yml` | `bootstrap_nodes` | Initialisation Day-0 (Root) |
| **01** | `01_common.yml` | `all` | Hardening, SSH, Firewall |
| **02** | `02_docker.yml` | `all` | Container Runtime |
| **03** | `03_service_infra.yml`| `all` | Traefik, Backup, Monitoring |
| **04** | `04_applications.yml` | `all` | Stacks Applicatives (WordPress, Wiki, etc.) |

---

## 6. SEGMENTATION DES INVENTAIRES

La sécurité de TALOS repose sur une séparation physique des contextes d'exécution.

*   **`inventories/bootstrap/`** : Utilisé uniquement pour la "Phase Zéro". Accès via port 22 et utilisateur par défaut.
*   **`inventories/dev/`** : Inventaire par défaut (Vagrant). Accès via port 8888 et utilisateur `sentinel`.
*   **`inventories/prod/`** : Cible réelle. Isolation totale des variables et des secrets.

---

## 7. GESTION DES SECRETS (VAULT IDs)

## 6. OBSERVABILITÉ & CONTINUITÉ

### 💾 Sauvegardes (Disaster Recovery)
*   **Moteur** : Kopia / Restic.
*   **Cible** : S3 Chiffré (Off-site).
*   **Drill** : **Automatisé Mensuellement** (Restore VM + Checksum).

### 👁️ Stack LGT (Logs-Grafana-Tempo)
Stack "Watchdog" isolée pour debugger sans SSH.
*   **Promtail** : Agent de collecte (Socket RO).
*   **Loki** : Agrégation (RAM Limitée < 1GB).
*   **Grafana** : Dashboards unifiés.
*   **Alerting** : Webhook Discord/Telegram.

---

## 7. ROADMAP CI/CD

> [!NOTE]
> Transition "Human Gate" vers "Automated Runners".

*   **Self-Hosted Runners** : Déploiement d'un agent GitHub Actions dans conteneur isolé.
*   **Flux** : Le Runner exécute Ansible en `localhost` après validation PR.
*   **Gain** : Aucune clé SSH ne sort du serveur.

---

## 8. GOUVERNANCE DE MAINTENANCE (CI-DRIVEN)

> [!IMPORTANT]
> Pour garantir l'immuabilité et la traçabilité, la maintenance "Day-2" est déportée sur GitHub Actions.

*   **Vecteur** : Workflow Ansible planifié (`schedule: cron`).
*   **Périomètre** :
    *   Nettoyage Docker (`system prune`).
    *   Mises à jour applicatives (via Tags Ansible).
    *   Vérification d'intégrité des backups Kopia.
*   **Exception Sécurité** : Les patchs de sécurité OS restent locaux (`unattended-upgrades`) pour une réactivité maximale hors-ligne.
