from app.repositories.product_repo import ProductRepository
from app.models.product import Product

def _seed(db):
    data = [
        Product(name="Pen", description="", price=1.5, quantity=100, image_url=""),
        Product(name="Notebook", description="", price=3.2, quantity=20, image_url=None),
        Product(name="Lamp", description="", price=9.9, quantity=5, image_url="http://img/l.png"),
        Product(name="Pencil", description="", price=0.8, quantity=200, image_url=""),
    ]
    for d in data:
        db.add(d)
    db.commit()

def test_repo_list_search_filter_sort(db_session):
    _seed(db_session)
    repo = ProductRepository(db_session)

    # Search by substring 'Pen' -> Pen, Pencil
    items = repo.list(q="Pen")
    names = [i.name for i in items]
    assert set(names) == {"Pen", "Pencil"}

    # min_price filter -> >= 3.0 should include Notebook (3.2) and Lamp (9.9)
    items = repo.list(min_price=3.0)
    names = [i.name for i in items]
    assert set(names) == {"Notebook", "Lamp"}

    # has_image true -> only Lamp
    items = repo.list(has_image=True)
    names = [i.name for i in items]
    assert names == ["Lamp"]

    # Sort by price desc -> first is Lamp (9.9)
    items = repo.list(sort_by="price", sort_dir="desc")
    assert items[0].name == "Lamp"
    assert items[0].price >= items[-1].price