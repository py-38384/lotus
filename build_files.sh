# pip install -r requirements.txt
# python3.9 manage.py collectstatic

#!/usr/bin/env bash
# exit on error
set -o errexit

poetry install

python manage.py collectstatic --no-input
python manage.py migrate