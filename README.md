# Workout App Backend

## Development

### Setup
1. create a venv:
```ps
python -m venv .\.venv
```
2. activate the venv:
```ps
.\.venv\Scripts\Activate.ps1
```
3. install the required packages:
```ps
pip install -r requirements.txt
```
4. install hatch:
```
pip install hatch
```
5. set up the .env file by running ```cp .env.example .env``` and inserting your information

### Debugging

- Start a local FastAPI test server using:
```ps
hatch run backend
```

- Server is reachable under http://localhost:7000

- Reset the database and optionally create a test user:
```ps
hatch run backend-cli reset-db --create-default-user
```
- Default user has username **admin** and password **password**

- Insert base exercises into the database:
```ps
hatch run backend-cli import-exercises Exercises.csv
```

### Testing

- Run API and Unit tests: 
    - Press **CTRL+SHIFT+P**
    - Select Tasks: Run Task
    - Select either: Run API Tests, Run Unit Tests, Run all Tests (both)

- Run Integration Tests:
    - ensure the backend is reachable locally under http://localhost:7000
    - run ```hatch run backend-integration-tests```