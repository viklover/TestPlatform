Test Platform
===============
Each user has the ability to create and pass other peoples tests.

[Preview presentation](Презентация.pdf)

Technology stack:
* Python 3.6
* Django 4.0+
* SQLite 3.22+

Project setup instruction:
1. Download in ZIP or clone this repository
2. Install required Python libraries:
    ```bash
    pip install -r requirements.txt
    ```
3. Create unique app key
    ```bash
   python manage.py shell -c "from django.core.management.utils import get_random_secret_key; get_random_secret_key()"
   ```
5. Synchronize database structure with models: 
    ```bash
    python manage.py migrate
    ```
6. Launch the site using the command:
   ```bash
    python manage.py runserver 8000
    ```
