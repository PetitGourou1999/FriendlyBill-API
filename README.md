# Friendly Bill App

## How To Setup

```
python3 -v venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

## How to run tests

```
python -m pytest
```

## How to run app

```
flask run
```

## TODO

- If not the creator of BillItem -> cannot delete
- If owner of the Bill -> cannot delete BillUser associated to owner
- Route for transfering ownership before being able to delete owner BillUser
