#! /bin/bash

echo "Installation de CryptImage en cours ...."
echo "Note : CryptImage nécessite python 3 et un environnement Linux."
echo
echo "Installation des modules ..."
python3 -m pip install -r ../requirement.txt
echo
echo "Définition de l'environnement"
export PYTHONPATH=$(which python3)
cd ..
export PYTHONPATH="$PYTHONPATH:$(pwd)"
cd cryptimage
export PYTHONPATH="$PYTHONPATH:$(pwd)"

echo "Execution de 'sudo apt-get install ffmpeg libsm6 libxext6  -y' : "
sudo apt-get install ffmpeg libsm6 libxext6  -y

echo
echo "Installation réussie"
echo "CryptImage est pret à être exécuté"
