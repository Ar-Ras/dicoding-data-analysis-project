# Setup .venv
There are two ways to setup the env. Choose whichever is most comfortable and available:

#### First way
```
python -m venv prod-venv

# if on UNIX bash shell, run:
prod-venv/Scripts/activate

# if on Windows PowerShell, run:
prod-venv/Scripts/activate.ps1

pip install -r requirements.txt
```

#### Second way (requires Conda)
```
conda create --name prod-venv python=3.10.5 pip
conda activate prod-venv

pip install -r requirements.txt
```

# Run Streamlit app
```
streamlit run app.py
```