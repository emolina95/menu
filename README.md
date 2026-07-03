# Restaurant Menu API
A REST API built with Django REST Framework to serve a restaurant menu with filtering, validation and test suite includes. Model:
 * categories
 * menu items
 * ingredients

## Tech Stack used
* Python 3.14
* Django + Django Rest Framework - API Layer
* Django Filter
* SQlite

### Setup
```bash
# 1. Clone and enter the project
git clone https://github.com/emolina95/menu.git
cd restaurant
 
# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
 
# 3. Install dependencies
pip install -r requirements.txt
 
# 4. Apply migrations
python manage.py migrate

# 5. Running the tests
python manage.py test
 
# 6. Run the development server
python manage.py runserver
```
The browsable API root is then available at http://127.0.0.1:8000/api/v1/.

### API endpoints
 
All endpoints are versioned under `/api/v1/`.
* `/api/v1/categories/`      
* `/api/v1/categories/{id}/`
* `/api/v1/menu-items/`
* `/api/v1/menu-items/{id}/`
* `/api/v1/ingredients/`
* `/api/v1/ingredients/{id}/`

### Filtering
 
Menu items support query-param filters:
 
- `?category={id}` — items in a category
- `?is_available=true` — available items only
- `?ingredients={id}` — items containing a given ingredient
Example: `/api/v1/menu-items/?ingredients=3&is_available=true`

## Data model
 
- A **Category** groups menu items (e.g. "Appetizers").
- A **MenuItem** belongs to one category and has many ingredients.
- An **Ingredient** can appear in many menu items.
The MenuItem↔Ingredient relationship is a **ManyToMany**, since a dish has
several ingredients and an ingredient is reused across dishes.