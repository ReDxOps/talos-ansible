#!/usr/bin/env python3
import getpass
import sys
import subprocess
import shutil

# Script pour générer un hash Bcrypt

def generate_bcrypt_hash(password):
    htpasswd_path = shutil.which("htpasswd")
    # Nom d'utilisateur factice pour tromper htpasswd
    dummy_user = "user"
    
    cmd = []
    if htpasswd_path:
        cmd = [htpasswd_path, "-nbB", dummy_user, password]
    else:
        if not shutil.which("docker"):
             raise Exception("Ni 'htpasswd' ni 'docker' ne sont trouvés dans le PATH.")
        
        cmd = [
            "docker", "run", "--rm", 
            "httpd:alpine", 
            "htpasswd", "-nbB", dummy_user, password
        ]
    
    try:
        process = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        full_output = process.stdout.strip()
        
        if ":" in full_output:
            return full_output.split(":", 1)[1]
        return full_output
        
    except subprocess.CalledProcessError as e:
        raise Exception(f"Erreur d'exécution : {e.stderr}")

def main():
    print("Générateur de Hash Bcrypt")
    print("-------------------------")
    
    try:
        password = getpass.getpass("Mot de passe à hasher : ")
        confirm = getpass.getpass("Confirmation          : ")
    except KeyboardInterrupt:
        sys.exit(0)

    if password != confirm:
        print("Les mots de passe ne correspondent pas.")
        sys.exit(1)

    try:
        print("")
        hash_result = generate_bcrypt_hash(password)
        print(hash_result)
        print("")
        
    except Exception as e:
        print(f"Erreur : {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
