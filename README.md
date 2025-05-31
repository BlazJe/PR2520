# Linux
```
python -m venv PR2520
source PR2520/bin/activate
pip install -r requirements.txt
```

# Windows
Če Powershell blokira aktivacijo skripte:
```
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

```
python -m venv PR2520
PR2520\Scripts\activate
pip install -r requirements.txt
```
# Modeli

Modeli niso objavljeni v repozitoriju zaradi njihove velikosti.  
Če želite generirati modele, poženite datoteko `model.ipynb`.  
Modeli se bodo shranili v vnaprej določene direktorije:

- `models_NaiveBayas`
- `models_Random_Forest`