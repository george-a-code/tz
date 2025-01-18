# tz
Timezone CLI Application. Save favourite timezones and see a given time in all zones!


## Setup
These instructions assume you are using VSCode. This is not required, but you're on your own if you want to use a different editor :)

### Create python virtual environment
```
cd tz
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Optionally install recommended VSCode workspace extensions
Extensions can be found in `tz/.vscode/extensions.json`

## Run tests
```
cd tz
pytest
```