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

## 🐣 BOOTSTRAP (DAY-0)
Opération à faire une seule fois par serveur nu.
```bash
# Pour le Lab Vagrant
ansible-playbook playbooks/00_bootstrap.yml -i inventories/bootstrap/hosts.yml --limit talos-dev

# Pour la Prod (si accès root encore actif sur port 22)
ansible-playbook playbooks/00_bootstrap.yml -i inventories/bootstrap/hosts.yml --limit prod --user root
```

---

## 🚀 DÉPLOIEMENT (SITE.YML)
La commande unique pour tout gérer.
```bash
# Déploiement complet (par défaut sur dev via ansible.cfg)
ansible-playbook site.yml

# Déploiement sur la Production
ansible-playbook site.yml -i inventories/prod/hosts.yml

# Cibler une phase ou un rôle précis (Recommandé)
ansible-playbook site.yml --tags traefik
ansible-playbook site.yml --tags common,docker
```

---

## 🔐 SECRETS & VAULT
```bash
# Éditer les secrets de DEV
ansible-vault edit inventories/dev/group_vars/all/secrets.yml --vault-id dev@.vault_pass_dev

# Éditer les secrets de PROD
ansible-vault edit inventories/prod/group_vars/all/secrets.yml --vault-id prod@.vault_pass_prod

# Vérifier qu'une variable chiffrée est accessible
ansible-inventory --list | grep vault_smtp_pass
```

---

## 🛠️ DIAGNOSTIC & MAINTENANCE
```bash
# Vérifier la syntaxe globale de l'infra
ansible-playbook site.yml --syntax-check

# Lister tous les hôtes et leurs variables
ansible-inventory --list -y

# Tester la connectivité (Ping Pong)
ansible all -m ping
```

---

## 🧹 NETTOYAGE & RÉINITIALISATION
```bash
# Supprimer tout Docker sur la VM (Prudence !)
ansible all -m shell -a "docker system prune -af --volumes"

# Détruire et recréer le Lab
vagrant destroy -f && vagrant up
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
