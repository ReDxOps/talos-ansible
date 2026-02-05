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

> [!IMPORTANT]
> Ne lancez aucune commande admin sans avoir consulté les procédures correspondantes.

<div align="center">

| 🏛️ ARCHITECTURE | 📅 MIGRATION | ⚡ CHEATSHEET | 🕵️‍♂️ AUDIT |
| :---: | :---: | :---: | :---: |
| [Accéder à l'Architecture](docs/ARCHITECTURE.md) | [Voir le Plan](docs/MIGRATION_PLAN.md) | [Commandes Vitales](docs/CHEATSHEET.md) | [Rapport de Sécurité](docs/AUDIT_REPORT.md) |
| *Network, Security, Stack* | *Zero-to-Hero Guide* | *Ops, Clean, Logs* | *Risques & Fixes* |

</div>

---

## ⚡ DÉMARRAGE RAPIDE (DEV)

### Pré-requis
*   Vagrant + VMware (ou VirtualBox).
*   Ansible Core.

### 1. Initialiser l'environnement
```bash
git clone git@github.com:user/talos.git
cd talos
vagrant up
```

### 2. Déployer le Socle (Dev)
```bash
# Le mot de passe Vault vous sera demandé (ou via .vault_pass)
ansible-playbook -i inventory.ini site.yml --tags "base" --limit dev
```

### 3. Accès SSH (Post-Provisioning)
```bash
# Port 8888, Utilisateur 'sentinel'
ssh -p 8888 sentinel@192.168.x.x
```

---

## 📂 STRUCTURE DU PROJET

```text
talos/
├── docs/               # 📘 Le Codex (Source de Vérité)
├── group_vars/         # 🔐 Variables globales (Secrets chiffrés)
├── inventory.ini       # 🌍 Inventaire (Dev/Prod)
├── roles/
│   ├── common/         # 🧱 Socle système (Docker, UFW, CrowdSec, Users)
│   ├── monitoring/     # 👁️ Stack LGT (Loki, Grafana, Promtail)
│   └── [apps]/         # 📦 1 App = 1 Rôle (Nextcloud, Traefik, etc.)
├── site.yml            # 🚀 Playbook Maître
└── Vagrantfile         # 🛠️ Lab local
```

---

<div align="center">
  <b>Mainteneur :</b> ReDxOps • <b>Licence :</b> MIT
</div>