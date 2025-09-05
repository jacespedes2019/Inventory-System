from typing import Dict

def _auth_header(token: str) -> Dict[str, str]:
    return {"Authorization": f"Bearer {token}"}

def test_products_crud_with_admin(client, admin_token):
    # Create
    p = {
        "name": "Shampoo",
        "description": "Hair care",
        "price": 12.50,
        "quantity": 5,
        "image_url": "http://img/shampoo.png",
    }
    r = client.post("/products/", headers=_auth_header(admin_token), json=p)
    assert r.status_code == 201, r.text
    created = r.json()
    assert created["name"] == "Shampoo"
    pid = created["id"]

    # Get
    r = client.get(f"/products/{pid}", headers=_auth_header(admin_token))
    assert r.status_code == 200
    got = r.json()
    assert got["id"] == pid

    # Update
    r = client.put(f"/products/{pid}", headers=_auth_header(admin_token), json={"quantity": 9})
    assert r.status_code == 200
    updated = r.json()
    assert updated["quantity"] == 9

    # Delete
    r = client.delete(f"/products/{pid}", headers=_auth_header(admin_token))
    assert r.status_code == 204

def test_products_list_search_filter_sort(client, admin_token):
    # Seed multiple products
    items = [
        {"name": "Apple",  "description": "", "price": 3.0,  "quantity": 50, "image_url": ""},
        {"name": "Banana", "description": "", "price": 2.0,  "quantity": 30, "image_url": ""},
        {"name": "Mango",  "description": "", "price": 5.5,  "quantity": 10, "image_url": "http://img/m.png"},
        {"name": "Avocado","description": "", "price": 7.1,  "quantity": 5,  "image_url": None},
    ]
    for it in items:
        r = client.post("/products/", headers=_auth_header(admin_token), json=it)
        assert r.status_code == 201

    # Search 'an' -> Banana, Mango
    r = client.get("/products?q=an", headers=_auth_header(admin_token))
    assert r.status_code == 200
    names = [p["name"] for p in r.json()]
    assert set(names) >= {"Banana", "Mango"}

    # Filter min_price=5 -> Mango, Avocado
    r = client.get("/products?min_price=5", headers=_auth_header(admin_token))
    assert r.status_code == 200
    names = [p["name"] for p in r.json()]
    assert set(names) >= {"Mango", "Avocado"}

    # Filter has_image=true -> only Mango (image_url non-empty)
    r = client.get("/products?has_image=true", headers=_auth_header(admin_token))
    assert r.status_code == 200
    names = [p["name"] for p in r.json()]
    assert "Mango" in names
    assert "Apple" not in names  # empty string counts as no image

    # Sort by price desc -> first should have highest price (≈ Avocado 7.1)
    r = client.get("/products?sort_by=price&sort_dir=desc", headers=_auth_header(admin_token))
    assert r.status_code == 200
    data = r.json()
    assert data[0]["name"] in {"Avocado", "Mango"}  # Avocado(7.1) or Mango(5.5); 7.1 should be first
    assert data[0]["price"] >= data[-1]["price"]

def test_products_permissions_user_cannot_write(client, user_token):
    # user can read
    r = client.get("/products", headers=_auth_header(user_token))
    assert r.status_code == 200

    # user cannot create
    r = client.post("/products/", headers=_auth_header(user_token), json={
        "name": "X", "description": "", "price": 1.0, "quantity": 1, "image_url": ""})
    assert r.status_code == 403  # blocked by require_roles("admin")

    # user cannot update
    r = client.put("/products/9999", headers=_auth_header(user_token), json={"name": "Y"})
    assert r.status_code == 403

    # user cannot delete
    r = client.delete("/products/9999", headers=_auth_header(user_token))
    assert r.status_code == 403