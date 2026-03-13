from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "grocery_secret"

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    conn = get_db_connection()
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return render_template("products.html", products=products)


@app.route("/add_to_cart/<int:product_id>")
def add_to_cart(product_id):
    if "cart" not in session:
        session["cart"] = []

    cart = session["cart"]
    cart.append(product_id)
    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    if "cart" not in session:
        return render_template("cart.html", cart_items=[], total=0)

    cart = session["cart"]

    conn = get_db_connection()
    cart_items = []
    total = 0

    for product_id in cart:
        product = conn.execute(
            "SELECT * FROM products WHERE id=?", (product_id,)
        ).fetchone()
        cart_items.append(product)
        total += product["price"]

    conn.close()

    return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/remove/<int:index>")
def remove(index):
    cart = session.get("cart", [])
    if index < len(cart):
        cart.pop(index)
        session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        address = request.form["address"]

        session["customer"] = {
            "name": name,
            "phone": phone,
            "address": address,
        }

        return redirect(url_for("payment"))

    return render_template("checkout.html")


@app.route("/payment", methods=["GET", "POST"])
def payment():
    if request.method == "POST":
        payment_method = request.form["payment"]

        session.pop("cart", None)

        return render_template("success.html", payment_method=payment_method)

    return render_template("payment.html")


if __name__ == "__main__":
    app.run(debug=True)