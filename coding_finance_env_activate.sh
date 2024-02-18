#!usr/bin/bash 

set -e

venv=${1:-coding_finance_env}

if [[ "$OSTYPE" == "msys" ]]; then
<<<<<<< HEAD
    source "C:/ProgramData/Python/virtualenvs/${venv}/Scripts/activate"
else
    source ~/virtualenvs/${venv}/bin/activate
=======
        source "C:/ProgramData/Python/virtualenvs/${venv}/Scripts/activate"
else
        source ~/virtualenvs/${venv}/bin/activate
>>>>>>> origin/main
fi
