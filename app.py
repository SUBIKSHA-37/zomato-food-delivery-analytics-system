from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector

app = Flask(__name__)
CORS(app)

# =========================
# MYSQL CONNECTION
# =========================

try:
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="yourpassword",
        database="zomatoapp"
    )

    cursor = conn.cursor(dictionary=True)

    print("✅ Connected to MySQL")

except Exception as e:
    print("❌ Database Connection Error")
    print(e)

# =========================
# HOME ROUTE
# =========================

@app.route("/")
def home():
    return jsonify({
        "message": "Zomato Backend Running"
    })

# =========================
# GET ALL FOODS
# =========================

@app.route("/foods", methods=["GET"])
def get_foods():

    try:

        cursor.execute("""
            SELECT
                food_id,
                food_name,
                category,
                price,
                rating,
                restaurant_name
            FROM foods
        """)

        foods = cursor.fetchall()

        return jsonify(foods)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# PLACE ORDER
# =========================
@app.route("/add-order", methods=["POST"])
def add_order():

    try:

        data = request.get_json()

        print("\n========== ORDER RECEIVED ==========")
        print(data)
        print("====================================\n")

        if not data:
            return jsonify({
                "success": False,
                "error": "No JSON data received"
            }), 400

        # --------------------------
        # CUSTOMER
        # --------------------------

        customer_query = """
        INSERT INTO customers(name, email, mobile)
        VALUES(%s, %s, %s)
        """

        cursor.execute(
            customer_query,
            (
                data["name"],
                data["email"],
                data["mobile"]
            )
        )

        customer_id = cursor.lastrowid

        print("Customer inserted:", customer_id)

        # --------------------------
        # ORDER
        # --------------------------

        order_query = """
        INSERT INTO orders(customer_id, total_amount)
        VALUES(%s, %s)
        """

        cursor.execute(
            order_query,
            (
                customer_id,
                data["total"]
            )
        )

        order_id = cursor.lastrowid

        print("Order inserted:", order_id)

        # --------------------------
        # ORDER ITEMS
        # --------------------------

        items = data.get("items", [])

        print("Items received:", items)

        for item in items:

            print("Inserting item:", item)

            item_query = """
            INSERT INTO order_items
            (order_id, food_id, quantity, price)
            VALUES(%s, %s, %s, %s)
            """

            cursor.execute(
                item_query,
                (
                    order_id,
                    item["id"],
                    item["qty"],
                    item["price"]
                )
            )

            print("Item inserted successfully")

        # --------------------------
        # DELIVERY DETAILS
        # --------------------------

        delivery_query = """
        INSERT INTO delivery_details
        (order_id, address, delivery_status)
        VALUES(%s, %s, %s)
        """

        cursor.execute(
            delivery_query,
            (
                order_id,
                data["address"],
                "Pending"
            )
        )

        print("Delivery details inserted")

        # --------------------------
        # COMMIT
        # --------------------------

        conn.commit()

        print("Transaction committed")

        return jsonify({
            "success": True,
            "message": "Order placed successfully",
            "order_id": order_id
        })

    except Exception as e:

        conn.rollback()

        print("\n❌ ERROR OCCURRED")
        print(str(e))
        print("Rollback completed\n")

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
        # --------------------------
        # ORDER ITEMS
        # --------------------------

        for item in data["items"]:

            item_query = """
            INSERT INTO order_items
            (order_id, food_id, quantity, price)
            VALUES(%s,%s,%s,%s)
            """

            cursor.execute(
                item_query,
                (
                    order_id,
                    item["id"],
                    item["qty"],
                    item["price"]
                )
            )

        # --------------------------
        # DELIVERY DETAILS
        # --------------------------

        delivery_query = """
        INSERT INTO delivery_details
        (order_id, address, delivery_status)
        VALUES(%s,%s,%s)
        """

        cursor.execute(
            delivery_query,
            (
                order_id,
                data["address"],
                "Pending"
            )
        )

        conn.commit()

        return jsonify({
            "success": True,
            "message": "Order Placed Successfully",
            "order_id": order_id
        })

    except Exception as e:

        conn.rollback()

        print("❌ ERROR:")
        print(e)

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# GET CUSTOMERS
# =========================

@app.route("/customers", methods=["GET"])
def get_customers():

    try:

        cursor.execute("""
            SELECT *
            FROM customers
            ORDER BY customer_id DESC
        """)

        customers = cursor.fetchall()

        return jsonify(customers)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# GET ORDERS
# =========================

@app.route("/orders", methods=["GET"])
def get_orders():

    try:

        cursor.execute("""
            SELECT *
            FROM orders
            ORDER BY order_id DESC
        """)

        orders = cursor.fetchall()

        return jsonify(orders)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# GET ORDER ITEMS
# =========================

@app.route("/order-items", methods=["GET"])
def get_order_items():

    try:

        cursor.execute("""
            SELECT *
            FROM order_items
            ORDER BY order_item_id DESC
        """)

        items = cursor.fetchall()

        return jsonify(items)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# GET DELIVERY DETAILS
# =========================

@app.route("/delivery-details", methods=["GET"])
def get_delivery_details():

    try:

        cursor.execute("""
            SELECT *
            FROM delivery_details
            ORDER BY delivery_id DESC
        """)

        delivery = cursor.fetchall()

        return jsonify(delivery)

    except Exception as e:

        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )