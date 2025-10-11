create-prism-mockserver service-auth-client     http://127.0.0.1:8000/openapi.json --force --port 8000
create-prism-mockserver service-token-validator http://127.0.0.1:8001/openapi.json --force --port 8001
create-prism-mockserver service-user            http://127.0.0.1:8002/openapi.json --force --port 8002
