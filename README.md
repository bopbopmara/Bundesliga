Bundesliga
=========

Optional environment settings
---------------------------------------------------
```bash
export ALLOWED_LEAGUES='bl1 bl2 bl3'  # If you need to restrict the default ones
```


Instructions for running in development
---------------------------------------

```bash
git clone
cd bundesliga
mkvirtualenv bundesliga
vim WORKON_HOME/bundesliga/bin/postactivate # Set allowed leagues if necessary
workon bundesliga
pip install -r requirements/dev.txt
export FLASK_APP='bundesliga/app.py'
flask run --host=127.0.0.1
```

Running Tests
-------------
```bash
py.test tests
```

