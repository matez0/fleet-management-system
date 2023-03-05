# Fleet management system

## Testing

```
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```
Install dependencies:
```
pip install -r requirements.txt
```

```
python manage.py makemigrations --settings=project.settings.fms
python manage.py migrate --settings=project.settings.fms
```

```
docker network create fms_net
```
