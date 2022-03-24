#! /bin/bash

echo "Installation de CryptImage en cours ...."
echo "Note : CryptImage nécessite python 3 et un environnement Linux."
echo
echo "Installation des modules ..."
pip install -r ../requirement.txt
echo
echo "Définition de l'environnement"
export PYTHONPATH=$(which python3)
cd ..
export PYTHONPATH="$PYTHONPATH:$(pwd)"
cd cryptimage
export PYTHONPATH="$PYTHONPATH:$(pwd)"
echo
echo "Installation réussie"
echo "CryptImage est pret à être exécuté"
