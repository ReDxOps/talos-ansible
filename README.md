<div align="center">

<img src="docs/assets/talos_logo.png" alt="Talos Logo" width="240"/>

# 🛡️ TALOS INFRASTRUCTURE

### Immutable SRE Infrastructure

<img src="https://img.shields.io/badge/-TALOS_INFRASTRUCTURE-cd7f32?style=for-the-badge&logo=fortinet&logoColor=white" alt="Talos INFRASTRUCTURE" />
<img src="https://img.shields.io/badge/-Debian-a81d33?style=for-the-badge&logo=debian&logoColor=white" alt="Debian" />
<img src="https://img.shields.io/badge/-Docker-2496ed?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/-Ansible-000000?style=for-the-badge&logo=ansible&logoColor=white" alt="Ansible" />
<img src="https://img.shields.io/badge/-CrowdSec-d0a41d?style=for-the-badge&logo=crowdsec&logoColor=white" alt="CrowdSec" />
<img src="https://img.shields.io/badge/-License-blue?style=for-the-badge" alt="License" />

<br/>

**TALOS** est une infrastructure **Self-Hosted**, **Sécurisée** et **Automatisée**, conçue selon les standards SRE les plus stricts ("Security First", Idempotence, GitOps) pour protéger vos services critiques.

[Philosophie](#-philosophie) • [Documentation](#-le-codex-documentation) • [Démarrage Rapide](#-démarrage-rapide-dev) • [Structure](#-structure-du-projet)

</div>

---

## 🏗️ PHILOSOPHIE

Ce projet n'est pas "juste un serveur". C'est une plateforme d'ingénierie qui respecte les standards **Enterprise / SRE**.

| Pilier | Description Technique |
| :--- | :--- |
| **🔒 Security First** | Port SSH `8888`, Auth Key-Only, **CrowdSec IPS**, Socket Proxy, Root disable. |
| **👁️ Observabilité** | Stack **LGT** (Loki-Grafana-Tempo) pour centraliser logs & métriques sans SSH. |
| **🧘 Idempotence** | Tout est code (IaC). Reset total et reconstruction en **< 30 min**. |
| **🤖 GitOps** | Modifications via Git uniquement. Déploiement piloté par **Ansible**. |

---

## 📚 LE CODEX (DOCUMENTATION)

La documentation est la source de vérité absolue.

<div align="center">

| 🏛️ ARCHITECTURE | ⚡ CHEATSHEET | 🔐 SECRETS | 🕵️‍♂️ AUDIT |
| :---: | :---: | :---: | :---: |
| [L'Architecture](docs/ARCHITECTURE.md) | [Les Commandes](docs/CHEATSHEET.md) | [Gestion Vault](docs/VAULT.md) | [Rapport](docs/AUDIT_REPORT.md) |
| *Network, Security, Playbooks* | *Ops, site.yml, tags* | *ID Dev vs Prod* | *Risques & Fixes* |

</div>

---

## 🛠️ PRÉ-REQUIS & INSTALLATION

### 1. La Stack Logicielle
| Outil | Rôle | Version Min |
| :--- | :--- | :--- |
| **Ansible** | Moteur d'automatisation. | `2.15+` |
| **Python** | Runtime Ansible. | `3.10+` |
| **Vagrant** | Hyperviseur de Lab. | `2.3+` |

### 2. Initialisation du Control Node
```bash
# 1. Cloner le dépôt
git clone git@github.com:ReDxOps/talos.git && cd talos

# 2. Installer les collections & rôles (Galaxy)
ansible-galaxy role install -r requirements.yml
ansible-galaxy collection install -r requirements.yml
```

---

## ⚡ DÉMARRAGE RAPIDE (LAB DEV)

### 1. Monter l'infrastructure de test
```bash
vagrant up
```

### 2. 🐣 PHASE 0 : Bootstrap (Day-0)
Opération à usage unique pour transformer une VM nue en cible TALOS sécurisée (Port 22 -> 8888).
```bash
ansible-playbook playbooks/00_bootstrap.yml \
  -i inventories/bootstrap/hosts.yml \
  --limit talos-dev
```

### 3. 🚀 PHASE 1-4 : Déploiement Global (Day-1+)
Une fois le bootstrap fini, on utilise le Master Playbook qui orchestre toutes les couches.
```bash
# Déploiement complet sur le lab de dév
ansible-playbook site.yml
```

---

## 🔐 GESTION DES SECRETS (VAULT IDs)

TALOS utilise une isolation stricte des secrets via des **Vault IDs**. Les mots de passe ne sont jamais partagés entre le développement et la production.

*   **Dev** : Chiffré avec `.vault_pass_dev` (`--vault-id dev`)
*   **Prod** : Chiffré avec `.vault_pass_prod` (`--vault-id prod`)

> [!TIP]
> `ansible.cfg` est configuré pour détecter automatiquement vos clés locales. Vous n'avez pas besoin de passer les flags manuellement !

---

## 📂 STRUCTURE DU PROJET (V2)

```text
talos/
├── inventories/             # 🌍 Environnements (Bootstrap, Dev, Prod)
│   ├── bootstrap/           # Day-0 : Accès initial
│   ├── dev/                 # Lab Local (Vagrant)
│   └── prod/                # Serveur de Production
├── group_vars/              # 🔐 Variables & Secrets (AES-256)
├── playbooks/               # 🚀 Séquençage (00_ à 04_)
├── roles/                   # 🧱 Briques logiques (Traefik, Apps, etc.)
├── ansible.cfg              # ⚙️ Pilotage Cloud-Ready
├── requirements.yml         # 📦 Dépendances Galaxy
└── site.yml                 # 🏛️ MASTER ORCHESTRATOR
```

---

<div align="center">
  <b>Mainteneur :</b> ReDxOps • <b>Licence :</b> MIT
</div>