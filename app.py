from flask import Flask, render_template, request, redirect, url_for, jsonify
import sweet_shop_manager

app = Flask(__name__)

# ------------------------
# Home page: List + Search + Sort
# ------------------------
@app.route('/')
def home():
    search_query = request.args.get('search', '').lower()
    sort_by = request.args.get('sort_by', '')

    items = sweet_shop_manager.get_all_items()

    # Filter by search query
    if search_query:
        items = [
            i for i in items
            if search_query in i['name'].lower()
            or search_query in i['category'].lower()
        ]

    # Sort results
    if sort_by == 'name':
        items = sorted(items, key=lambda x: x['name'].lower())
    elif sort_by == 'price':
        items = sorted(items, key=lambda x: x['price'])
    elif sort_by == 'category':
        items = sorted(items, key=lambda x: x['category'].lower())

    return render_template('index.html', items=items)

# ------------------------
# Add new sweet
# ------------------------
@app.route('/add', methods=['POST'])
def add_item():
    name = request.form['name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])
    category = request.form['category']

    sweet_shop_manager.add_item(name, quantity, price, category)
    return redirect(url_for('home'))

# ------------------------
# Delete sweet
# ------------------------
@app.route('/delete/<int:sweet_id>', methods=['POST'])
def delete_sweet(sweet_id):
    sweet_shop_manager.delete_item(sweet_id)
    return redirect(url_for('home'))

# ------------------------
# Edit sweet
# ------------------------
@app.route('/edit/<int:sweet_id>', methods=['GET', 'POST'])
def edit_sweet(sweet_id):
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        category = request.form['category']

        sweet_shop_manager.update_item(sweet_id, name, quantity, price, category)
        return redirect(url_for('home'))

    items = sweet_shop_manager.get_all_items()
    sweet = next((i for i in items if i['id'] == sweet_id), None)
    return render_template('edit.html', sweet=sweet)

# ------------------------
# Optional: API endpoint
# ------------------------
@app.route('/api/items')
def api_items():
    return jsonify(sweet_shop_manager.get_all_items())

# ------------------------
# Run Flask app
# ------------------------
if __name__ == '__main__':
    app.run(debug=True)
