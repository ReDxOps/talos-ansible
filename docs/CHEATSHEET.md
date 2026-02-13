# ⚡ CHEATSHEET OPÉRATIONNEL TALOS

![Status](https://img.shields.io/badge/Tools-Ready-orange?style=for-the-badge)

> [!TIP]
> Ce document regroupe les commandes vitales pour l'opérateur (Sentinel). Gardez-le à portée de main.

---

## 🛠️ GESTION ENVIRONNEMENT (VAGRANT)

| Action | Commande | Difficile à retenir ? |
| :--- | :--- | :--- |
| **Démarrer** | `vagrant up` | |
| **SSH** | `vagrant ssh` | Connecte au user `vagrant` par défaut |
| **Reload** | `vagrant reload` | Applique changement Vagrantfile |
| **Reset** | `vagrant destroy -f` | ⚠️ Supprime tout |

---

## 🔐 ANSIBLE VAULT (SECRETS)

> [!WARNING]
> Ne jamais commiter un secret en clair. Utilisez toujours `encrypt_string` pour les nouvelles variables.

```bash
# Éditer le fichier de secrets
ansible-vault edit group_vars/all/secrets.yml

# Chiffrer une variable 'inline' (Pour usage dans un playbook)
ansible-vault encrypt_string 'mon_password' --name 'db_password'

# Voir le contenu sans éditer
ansible-vault view group_vars/all/secrets.yml
```

---

## 🛡️ SÉCURITÉ (CROWDSEC)

Gestion de l'IPS collaboratif via le conteneur `crowdsec`.

```bash
# 📋 Lister les bannissements actifs
docker exec crowdsec cscli decisions list

# 🚫 Bannir une IP (Raison obligatoire)
docker exec crowdsec cscli decisions add --ip 1.2.3.4 --duration 24h --reason "Attaque manuelle"

# ✅ Débannir une IP (Faux positif)
docker exec crowdsec cscli decisions delete --ip 1.2.3.4
```

---

## 🚀 DÉPLOIEMENTS (PRODUCTION & DEV)

> [!IMPORTANT]
> Vérifiez toujours votre cible avec le flag `--limit`.
> *   Dev : `--limit dev`
> *   Prod : `--limit prod`

### 1. 🐣 Bootstrap (Premier Run / Day 0)
Configuration initiale (User, SSH Hardening). Nécessite surcharge car l'inventaire vise la cible finale.
```bash
# Dev (Vagrant)
ansible-playbook playbooks/bootstrap.yml --limit dev \
  -e "ansible_port=22" \
  -e "ansible_user=vagrant" \
  -e "ansible_ssh_private_key_file=.vagrant/machines/default/vmware_desktop/private_key"

# Prod (Première connexion root)
ansible-playbook playbooks/bootstrap.yml --limit prod \
  -e "ansible_port=22" \
  -e "ansible_user=root"
```

### 2. 🐳 Installation Docker (Day 1)
Une fois le bootstrap fait, tout est standard.
```bash
ansible-playbook playbooks/install_docker.yml --limit dev
```

### 2. Déploiement Applicatif (Chirurgical)
Ne touche que l'application ciblée.
```bash
# Exemple pour Nextcloud
ansible-playbook -i inventory.ini site.yml --tags "nextcloud" --limit prod
```

### 3. Test "Dry Run"
Simule l'exécution pour voir les changements (`--diff`).
```bash
ansible-playbook -i inventory.ini site.yml --tags "nextcloud" --limit prod --check --diff
```

---

## 🔍 VÉRIFICATIONS & MAINTENANCE

### Accès SSH Manuel
En cas de pépin, pour contourner l'automatisation.
```bash
ssh -p 8888 sentinel@192.168.x.x
```

### Vérifications Audit (SRE)
Commandes pour valider la conformité du serveur.
```bash
# 🕒 Vérifier synchro NTP (Critique pour CrowdSec/Logs)
timedatectl status

# 🪵 Vérifier Driver de Logs (Doit être 'json-file')
docker info --format '{{.LoggingDriver}}'
```

### Nettoyage (Maintenance)
> [!NOTE]
> Cette commande est automatisée par cron (Hebdo), mais utile en cas d'urgence disque.
```bash
# 🧹 Nettoyage TOTAL (Images, Conteneurs stop, Cache)
docker system prune -a -f --volumes
```

---

## 🔄 ROUTINE GITOPS STANDARD

1.  🛠️ **Fix/Feat** : `git checkout -b fix/ma-modif`
2.  🧪 **Test** : `vagrant provision` + Tests locaux.
    *   *Auto-Check* : Pre-commit hook valide les secrets.
3.  📦 **Commit** : `git commit -am "fix: description"`
4.  🚀 **Push & PR** : Merge sur `main` après review.
5.  🚢 **Deploy** : Ansible depuis le contrôleur.
