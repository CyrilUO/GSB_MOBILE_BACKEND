from app.core.exceptions import HarmFullEnum
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse

from app.api.routes import global_router
from app.db import init_db
from app.db.database import test_db_connection
from app.utils.token_blacklist import load_blacklisted_tokens

app = FastAPI(title="My API", description="API for my project", version="1.0")

# Gérer les permissions CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(title="GSB Mobile API", version="1.0")
app.include_router(global_router)

html_content = """
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>GSB Mobile API</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f4;
            padding: 50px;
        }
        .container {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
            max-width: 600px;
            margin: auto;
        }
        h1 {
            color: #007bff;
        }
        p {
            font-size: 18px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Bienvenue sur l'API GSB Mobile</h1>
        <p>Cette API vous permet d'accéder aux ressources de l'application GSB Mobile.</p>
        <p>Consultez la <a href="/docs">documentation interactive</a> pour plus d'informations.</p>
    </div>
</body>
</html>
"""


# Route de test
@app.get("/", response_class=HTMLResponse)
def read_root():
    return HTMLResponse(content=html_content)


# Point d’entrée
if __name__ == "__main__":
    test_db_connection()
    print(HarmFullEnum.banned_words())
    import importlib.metadata

    init_db()

    print(importlib.metadata.version("bcrypt"))

    load_blacklisted_tokens()


    import uvicorn

    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)
