# Role: ai-cli-tools

Rôle Ansible pour provisionner et administrer les outils CLI d'agents d'intelligence artificielle :
- **Claude Code CLI** (`@anthropic-ai/claude-code`)
- **Antigravity CLI** (`agy`)
- **OpenAI Codex CLI** (`@openai/codex`)

## Fonctionnalités

- Installation conditionnelle et modulaire de chaque outil CLI via des bascules booléennes.
- Détection et provisionnement automatique de **Node.js LTS** (via le dépôt officiel NodeSource) si au moins un outil basé sur npm est activé.
- Installation globale dans `/usr/local/bin` accessible immédiatement par tous les utilisateurs (notamment le runner `multica-runner`).

## Variables du Rôle

| Variable | Défaut | Description |
|---|---|---|
| `ai_cli_tools_install_claude` | `true` | Installer Claude Code CLI via npm |
| `ai_cli_tools_install_agy` | `true` | Installer Google Antigravity CLI |
| `ai_cli_tools_install_codex` | `true` | Installer OpenAI Codex CLI via npm |
| `ai_cli_tools_install_nodejs` | `true` | Provisionner Node.js & npm si nécessaire |
| `ai_cli_tools_nodejs_version` | `"20"` | Version majeure de NodeSource (ex: 20 ou 22) |
| `ai_cli_tools_target_user` | `"multica-runner"` | Utilisateur système cible principal |
| `ai_cli_tools_bin_dir` | `"/usr/local/bin"` | Répertoire de destination des exécutables |

## Utilisation

Ajoutez le rôle dans votre playbook d'infrastructure ou d'applications :

```yaml
- hosts: all
  become: true
  roles:
    - role: ai-cli-tools
      tags: ai-tools
```
