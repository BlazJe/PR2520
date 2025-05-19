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

# Git
```
pip install --upgrade nbstripout
nbstripout --install
```
```
pip install --upgrade nbdime
nbdime config-git --enable
```
```
nbdime mergetool
```
