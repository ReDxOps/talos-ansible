#!/usr/bin/env python3
import getpass
import sys
import subprocess
import os

# Script pour générer un hash de mot de passe compatible Ansible (SHA-512)
# Usage: ./scripts/hash_password.py

def generate_hash_local(password):
    import crypt
    return crypt.crypt(password, crypt.mksalt(crypt.METHOD_SHA512))

def generate_hash_docker(password):
    print("🐳 Module 'crypt' introuvable en local. Utilisation de Docker (python:3.9-alpine)...")
    cmd = [
        "docker", "run", "--rm", "-i", 
        "python:3.9-alpine", 
        "python3", "-c", 
        "import crypt,sys; print(crypt.crypt(sys.stdin.read().strip(), crypt.mksalt(crypt.METHOD_SHA512)))"
    ]
    
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stdout, stderr = process.communicate(input=password)
    
    if process.returncode != 0:
        raise Exception(f"Erreur Docker: {stderr}")
    
    return stdout.strip()

def main():
    print("🔐 Générateur de Hash TALOS (SHA-512)")
    print("-------------------------------------")
    
    try:
        password = getpass.getpass("Entrez le mot de passe à hasher : ")
        confirm = getpass.getpass("Confirmez le mot de passe       : ")
    except KeyboardInterrupt:
        print("\nAnnulé.")
        sys.exit(0)

    if password != confirm:
        print("\n❌ Erreur : Les mots de passe ne correspondent pas.")
        sys.exit(1)

    try:
        try:
            # Tentative 1: Local (Python macOS/Linux)
            pwd_hash = generate_hash_local(password)
        except (ImportError, AttributeError):
            # Tentative 2: Docker fallback
            pwd_hash = generate_hash_docker(password)
            
        print("\n✅ Hash généré avec succès :\n")
        print(pwd_hash)
        print("\n👉 Copiez ce hash dans votre fichier secrets.yml")
        
    except Exception as e:
        print(f"\n❌ Erreur fatale : {e}")
        print("💡 Vérifiez que Docker est lancé ou que vous utilisez un Python standard.")
        sys.exit(1)

if __name__ == "__main__":
    main()
