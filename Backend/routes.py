from flask import request, jsonify, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app import app, db, login_manager
from models import User, Product, Order

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API endpoint for user login
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()  # Expects JSON: { "username": "value", "password": "value" }
    if not data or not data.get("username") or not data.get("password"):
        return jsonify({"error": "Username and password required"}), 400

    user = User.query.filter_by(username=data.get("username")).first()
    if user and user.check_password(data.get("password")):
        login_user(user)
        return jsonify({
            "message": "Login successful",
            "username": user.username,
            "role": user.role
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401

# API endpoint for user logout
@app.route('/api/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logged out successfully"}), 200

# API endpoint for role-based dashboard (Page 1)
@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard_api():
    if current_user.role == 'Admin':
        products = Product.query.all()
        orders = Order.query.all()
        users = User.query.all()
        return jsonify({
            "role": "Admin",
            "products": [
                {"id": p.id, "name": p.name, "stock": p.stock, "warehouse_location": p.warehouse_location}
                for p in products
            ],
            "orders": [
                {"id": o.id, "product_id": o.product_id, "quantity": o.quantity, "status": o.status}
                for o in orders
            ],
            "users": [
                {"id": u.id, "username": u.username, "role": u.role}
                for u in users
            ]
        }), 200

    elif current_user.role == 'Staff':
        products = Product.query.filter_by(warehouse_location="Warehouse A").all()
        orders = Order.query.filter_by(status="Pending").all()
        return jsonify({
            "role": "Staff",
            "products": [
                {"id": p.id, "name": p.name, "stock": p.stock, "warehouse_location": p.warehouse_location}
                for p in products
            ],
            "orders": [
                {"id": o.id, "product_id": o.product_id, "quantity": o.quantity, "status": o.status}
                for o in orders
            ]
        }), 200

    elif current_user.role == 'Supplier':
        orders = Order.query.filter_by(status="Pending").all()
        return jsonify({
            "role": "Supplier",
            "orders": [
                {"id": o.id, "product_id": o.product_id, "quantity": o.quantity, "status": o.status}
                for o in orders
            ]
        }), 200

    else:
        return jsonify({"error": "User role not recognized"}), 400

# GET /api/products: Retrieve a list of all products.
@app.route('/api/products', methods=['GET'])
@login_required
def get_products():
    products = Product.query.all()
    data = [
        {
            "id": p.id,
            "name": p.name,
            "stock": p.stock,
            "warehouse_location": p.warehouse_location
        }
        for p in products
    ]
    return jsonify(data), 200

# POST /api/products: Create a new product.
@app.route('/api/products', methods=['POST'])
@login_required
def create_product():
    # Only Admin can create products
    if current_user.role != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    # Check for required fields
    if not data or not all(key in data for key in ['name', 'stock', 'warehouse_location']):
        return jsonify({"error": "Missing product information"}), 400

    new_product = Product(
        name=data['name'],
        stock=data['stock'],
        warehouse_location=data['warehouse_location']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully", "product_id": new_product.id}), 201

# PUT /api/products/<product_id>: Update an existing product.
@app.route('/api/products/<int:product_id>', methods=['PUT'])
@login_required
def update_product(product_id):
    # Allow Admin and Staff to update products
    if current_user.role not in ['Admin', 'Staff']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    product = Product.query.get_or_404(product_id)
    
    # Update fields if provided
    product.name = data.get('name', product.name)
    product.stock = data.get('stock', product.stock)
    product.warehouse_location = data.get('warehouse_location', product.warehouse_location)
    
    db.session.commit()
    return jsonify({"message": "Product updated successfully"}), 200

# DELETE /api/products/<product_id>: Delete a product.
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
@login_required
def delete_product(product_id):
    # Only Admin can delete products
    if current_user.role != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"}), 200

# GET /api/orders: Retrieve a list of orders.
@app.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    # For now, return all orders. You can later filter based on current_user.role if needed.
    orders = Order.query.all()
    data = [
        {
            "id": o.id,
            "product_id": o.product_id,
            "quantity": o.quantity,
            "status": o.status
        }
        for o in orders
    ]
    return jsonify(data), 200

# POST /api/orders: Create a new order.
@app.route('/api/orders', methods=['POST'])
@login_required
def create_order():
    # Only Admin or Staff can create orders.
    if current_user.role not in ['Admin', 'Staff']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    # Ensure required fields are present.
    if not data or not data.get("product_id") or not data.get("quantity"):
        return jsonify({"error": "Product ID and quantity are required"}), 400

    new_order = Order(
        product_id=data["product_id"],
        quantity=data["quantity"],
        status=data.get("status", "Pending")
    )
    db.session.add(new_order)
    db.session.commit()
    return jsonify({"message": "Order created successfully", "order_id": new_order.id}), 201

# PUT /api/orders/<order_id>: Update an existing order.
@app.route('/api/orders/<int:order_id>', methods=['PUT'])
@login_required
def update_order(order_id):
    # Allow Admin and Staff to update orders.
    if current_user.role not in ['Admin', 'Staff']:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    order = Order.query.get_or_404(order_id)

    # Update fields if provided; if not, keep the existing values.
    order.quantity = data.get("quantity", order.quantity)
    order.status = data.get("status", order.status)
    
    db.session.commit()
    return jsonify({"message": "Order updated successfully"}), 200

# DELETE /api/orders/<order_id>: Delete an order.
@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
@login_required
def delete_order(order_id):
    # Only Admin can delete orders.
    if current_user.role != 'Admin':
        return jsonify({"error": "Unauthorized"}), 403

    order = Order.query.get_or_404(order_id)
    db.session.delete(order)
    db.session.commit()
    return jsonify({"message": "Order deleted successfully"}), 200