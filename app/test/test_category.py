import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.modules.auth.schema import TokenProvider
from app.test.test_database import get_test_db, init_db
from app.core.dependencies import get_db
from app.core.security import get_current_user
from app.modules.category.schema import CreateCategory, CategoryResponse

client = TestClient(app)

#Pour chaque test, l'ajout de token dans mon payload ne fonctionnant pas, commenter current_user pour les endpoitns

#To run the test depuis la racine du projet pytest app/test/test_category.py -v
# Surcharge des dépendances FastAPI pour utiliser la base de test et un utilisateur fictif
app.dependency_overrides[get_db] = get_test_db
print(f"dependceis work {app.dependency_overrides[get_db]}")

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    init_db()


def test_api_running():
    response = client.get("/")
    print(f"Réponse brute : {response.text}")  # Debug

    assert response.status_code in [200, 404]

    if "application/json" in response.headers.get("content-type", ""):
        print(response.json())  # Vérifier si c'est bien du JSON


# Test de récupération de toutes les catégories (vide au début)
def test_get_all_categories_empty():
    response = client.get("/api/category/all")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == []  # Vérifier que la base est vide


# Test de création d'une catégorie
def test_create_category():
    category_data = {"name": "Electronics"}
    response = client.post("/api/category/create-category", json=category_data)

    assert response.status_code == 200

    # Valider avec Pydantic
    category_response = CategoryResponse.model_validate(response.json())
    print(category_response)
    assert "Category" in category_response.message


# Test de récupération d'une catégorie existante
def test_get_category_by_id():
    category_data = {"name": "Books"}
    create_response = client.post("/api/category/create-category", json=category_data)

    # 🛠 Vérifier si la réponse contient un ID au bon format
    print(f"⚠️ Réponse de création : {create_response.json()}")  # DEBUG

    category_id = create_response.json().get("id")  # ✅ Extraire l'ID directement
    assert category_id is not None, "L'ID n'a pas été retourné correctement"

    response = client.get(f"/api/category/{category_id}")
    print(response.json())

    assert response.status_code == 200
    assert response.json()["name"] == "Books"


# Test de suppression d'une catégorie
def test_delete_category():
    category_data = {"name": "Toys"}
    create_response = client.post("/api/category/create-category", json=category_data)
    category_id = create_response.json()["message"].split(": ")[1][:-16]

    delete_response = client.delete(f"/api/category/delete-category/{category_id}")
    print(delete_response.json())

    assert delete_response.status_code == 200
    assert "a été supprimé" in delete_response.json()["message"]

    # Vérifier que la catégorie n'existe plus
    get_response = client.get(f"/api/category/{category_id}")
    assert get_response.status_code == 404
