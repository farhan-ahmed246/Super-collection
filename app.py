from datetime import datetime, timedelta, date
from flask import Flask, render_template_string, request, redirect, session, url_for 
from werkzeug.utils import secure_filename
import os
import json
import smtplib
from email.mime.text import MIMEText



# ================= APP CONFIG =================
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "default_secret_key")



ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "fmukhtar420@gmail.com")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "blueberry@420")
ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "fmukhtar420@gmail.com")
GMAIL_USER = os.environ.get("GMAIL_USER", "fmukhtar420@gmail.com")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "bnap lyde xsxm twql")

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

PRODUCTS_FILE = "products.json"
order_history = []

# ---------------- PRODUCTS DATA ----------------
if os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, "r") as f:
        products = json.load(f)
else:
    products = [
        {"id": i, "title": f"Super Product {i}", "price": 2850,
         "description": "Premium Quality Product", "image": "", "images": [], "ratings": []}
        for i in range(1, 31)
    ]
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

def save_products():
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

# ---------------- EMAIL FUNCTION ----------------
def send_email(subject, body):
    try:
        msg = MIMEText(body)
        msg["Subject"] = subject
        msg["From"] = GMAIL_USER
        msg["To"] = ADMIN_EMAIL
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.login(GMAIL_USER, GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
    except Exception as e:
        print("Email Error:", e)


# ================= HOME =================
# ================= HOME =================
# ================= HOME =================
from flask import render_template_string, request, session
from datetime import datetime
@app.route("/", methods=["GET"])
def home():
    search = request.args.get("search","").lower()
    filtered = [p for p in products if search in p["title"].lower()]

    banner_path = "static/banner.jpg" if os.path.exists("static/banner.jpg") else "https://static.vecteezy.com/system/resources/previews/021/962/217/non_2x/ramadan-sale-banner-vector.jpg"

    html = """
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:black;color:white;font-family:sans-serif;}
.logo-box{text-align:center;margin-bottom:20px;}
.logo-sc{font-size:90px;font-weight:900;letter-spacing:5px;background:linear-gradient(45deg,#00c6ff,#ff00cc,#ff6600);-webkit-background-clip:text;-webkit-text-fill-color:transparent;position:relative;display:inline-block;}
.logo-sc:after{content:"⚡";position:absolute;left:50%;transform:translateX(-50%);top:-10px;font-size:100px;color:#ffcc00;text-shadow:0 0 20px #ffcc00;}
.logo-text{font-size:32px;font-weight:700;margin-top:-10px;letter-spacing:3px;}
.card{border:none;border-radius:15px;transition:0.3s;background:#111;color:white;}
.card:hover{transform:scale(1.05);box-shadow:0 10px 25px rgba(255,255,255,0.2);}
.btn-cart{background:#ff6600;border:none;color:white;padding:10px 20px;font-size:16px;margin-top:10px;border-radius:10px;cursor:pointer;}
.icon{width:45px;margin:0 10px;filter:invert(1);}
.product-img{width:100%;height:350px;object-fit:contain;background:#000;border-radius:10px;}
.search-bar{max-width:400px;margin:0 auto 20px;display:block;}
.size-btn{border-radius:50%;background:#222;color:white;width:50px;height:50px;margin:5px;border:none;cursor:pointer;}
a{text-decoration:none;color:white;}
</style>
</head>
<body>
<div class="container mt-4">

<!-- ADMIN LOGIN -->
<div class="d-flex justify-content-end mb-2">
<a href="/admin" class="btn btn-warning btn-sm">Admin Login</a>
</div>

<!-- SC LOGO -->
<div class="logo-box">
<div class="logo-sc">SC</div>
<div class="logo-text">SUPER COLLECTION</div>
</div>

<div class="mb-3 text-center">

<a href="https://www.instagram.com/supercollection6547/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" class="icon">
</a>

<a href="https://www.facebook.com/profile.php?id=61587780675415" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" class="icon">
</a>

<a href="https://www.tiktok.com/@superr.collection?lang=en" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/512/3046/3046120.png" class="icon">
</a>

<a href="https://wa.me/923363016943" target="_blank">
<img src="https://upload.wikimedia.org/wikipedia/commons/6/6b/WhatsApp.svg" class="icon">
</a>

</div>

<!-- SEARCH -->
<form method="get" class="mt-3">
<input type="text" name="search" placeholder="🔍 Search Products" class="form-control search-bar">
</form>

<!-- BANNER -->
<img src="{{ banner_url }}?v={{ timestamp }}" class="d-block mx-auto mb-4" style="width:100%;height:auto;border-radius:20px;">

{% if not filtered %}
<h3 class="mt-4 text-center">Not Available ❌</h3>
{% endif %}

<div class="row mt-4">
{% for p in filtered %}
<div class="col-md-4 mb-4">
<div class="card p-3 text-center">
<a href="/product/{{p.id}}">
<img src="{{p.images[0] if p.images else p.image}}" class="product-img mb-2">
</a>
<h5><a href="/product/{{p.id}}">{{p.title}}</a></h5>
<p>{{p.description}}</p>
<h6 class="text-danger">PKR {{p.price}}</h6>

<form action="/add_to_cart/{{p.id}}" method="post">
<input type="hidden" name="quantity" value="1">
<input type="hidden" name="size" value="N/A">
<button class="btn-cart w-100">Add To Cart</button>
</form>

</div>
</div>
{% endfor %}
</div>
</div>
</body>
</html>
"""
    return render_template_string(
        html,
        filtered=filtered,
        banner_url=banner_path,
        timestamp=datetime.now().timestamp()
    )


# ================= SIMPLE CHECKOUT =================
@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if "cart" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        address = request.form.get("address")
        desc = request.form.get("desc")
        phone = request.form.get("phone")
        selected_size = request.form.get("size", "N/A")

        # Product from cart
        product = next((p for p in products if p["id"] == session["cart"]["pid"]), None)
        if not product:
            return "<h2>Product not found ❌</h2><a href='/'>Back</a>"

        quantity = session["cart"].get("quantity", 1)
        total_price = quantity * product["price"]
        delivery = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        # Add order to history
        order_history.append({
            "name": name,
            "product": product["title"],
            "quantity": quantity,
            "size": selected_size,
            "total": total_price,
            "delivery": delivery
        })

        # Send email notification (optional)
        send_email(
            "New Order - Super Collection",
            f"""
Full Name: {name}
Age: {age}
Gender: {gender}
Address: {address}
Phone: {phone}
Email: {session.get("user", {}).get("email","N/A")}
Product: {product['title']}
Quantity: {quantity}
Size: {selected_size}
Total: PKR {total_price}
Delivery: {delivery}
"""
        )

        # Confirmation page
        return f"""
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{{background:black;color:white;font-family:sans-serif;display:flex;justify-content:center;align-items:center;height:100vh;}}
.confirm-box{{background:#111;padding:30px;border-radius:15px;text-align:center;max-width:400px;box-shadow:0 10px 25px rgba(255,255,255,0.2);}}
h2{{color:#00c6ff;}}
.btn-continue{{margin-top:15px;padding:10px 20px;border:none;border-radius:8px;background:#007bff;color:white;font-weight:bold;text-decoration:none;}}
</style>
</head>
<body>
<div class="confirm-box">
<h2>Order Confirmed ✅</h2>
<p><strong>Product:</strong> {product['title']}</p>
<p><strong>Quantity:</strong> {quantity}</p>
<p><strong>Size:</strong> {selected_size}</p>
<p><strong>Total:</strong> PKR {total_price}</p>
<p><strong>Delivery:</strong> {delivery}</p>
<a href="/" class="btn-continue">Continue Shopping</a>
</div>
</body>
</html>
"""

    # GET method → return checkout form
    return """
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:black;color:white;font-family:sans-serif;}
.box{max-width:700px;margin:auto;margin-top:30px;padding:30px;border-radius:15px;background:#111;}
.form-label{font-size:18px;font-weight:bold;}
.form-control, select, textarea{font-size:16px;padding:10px;background:#222;color:white;border:none;border-radius:5px;}
.btn-confirm{background:#007bff;border:none;font-size:18px;font-weight:bold;color:white;padding:10px 0;border-radius:10px;margin-top:10px;width:100%;}
.size-btn{border-radius:50%;background:#222;color:white;width:50px;height:50px;margin:5px;border:none;cursor:pointer;}
.size-btn.selected{background:#007bff;}
</style>
<script>
function selectSize(btn){
    let buttons=document.getElementsByClassName('size-btn');
    for(let b of buttons){b.classList.remove('selected');}
    btn.classList.add('selected');
    document.getElementById('size_input').value=btn.innerText;
}
</script>
</head>
<body>
<div class="box">
<h2 class="text-center mb-3">Checkout</h2>
<form method="post">
    <label class="form-label">Full Name</label>
    <input name="name" class="form-control mb-2" required>

    <label class="form-label">Age</label>
    <input name="age" type="number" class="form-control mb-2" required>

    <label class="form-label">Gender</label>
    <select name="gender" class="form-control mb-2">
        <option>Male</option>
        <option>Female</option>
    </select>

    <label class="form-label">Address</label>
    <textarea name="address" class="form-control mb-2" required></textarea>

    <label class="form-label">Phone Number</label>
    <input name="phone" class="form-control mb-2" required>

    <label class="form-label">Order Description</label>
    <textarea name="desc" class="form-control mb-2"></textarea>

    <label class="form-label">Select Size</label><br>
    <button type="button" class="size-btn" onclick="selectSize(this)">S</button>
    <button type="button" class="size-btn" onclick="selectSize(this)">M</button>
    <button type="button" class="size-btn" onclick="selectSize(this)">L</button>
    <button type="button" class="size-btn" onclick="selectSize(this)">XL</button>
    <button type="button" class="size-btn" onclick="selectSize(this)">XXL</button>
    <input type="hidden" id="size_input" name="size" value="">

    <button class="btn-confirm">Confirm Order</button>
</form>
<br><a href="/" class="btn btn-dark w-100">⬅ Continue Shopping</a>
</div>
</body>
</html>
"""

# ================= ADMIN LOGIN =================
@app.route("/admin", methods=["GET","POST"])
def admin():
    error = ""
    if request.method == "POST":
        if request.form.get("admin_user") == ADMIN_USERNAME and \
           request.form.get("admin_pass") == ADMIN_PASSWORD:

            session["admin"] = True

            #send_email(
                #"Admin Login Alert - Super Collection",
                #f"Admin logged in at {datetime.now()}"
            #)

            return redirect("/admin_dashboard")
        else:
            error = "Invalid Credentials ❌"

    return f"""
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body {{
    margin:0;
    height:100vh;
    display:flex;
    justify-content:center;
    align-items:center;
    background:linear-gradient(-45deg,#ff0000,#007bff,#00c6ff,#ff6600);
    background-size:400% 400%;
    animation:gradient 8s ease infinite;
}}
@keyframes gradient {{
    0% {{background-position:0% 50%;}}
    50% {{background-position:100% 50%;}}
    100% {{background-position:0% 50%;}}
}}
.box {{
    background:white;
    padding:50px;
    border-radius:20px;
    text-align:center;
    box-shadow:0 20px 50px rgba(0,0,0,0.3);
    width:350px;
}}
.title {{
    font-size:45px;
    font-weight:900;
    color:green;
}}
</style>
</head>
<body>
<div class="box">
<div class="title">ADMIN LOGIN</div>

<form method="post" style="margin-top:20px;" autocomplete="off">

    <!-- Hidden fake inputs to block autofill -->
    <input type="text" style="display:none">
    <input type="password" style="display:none">

    <input type="text"
           name="admin_user"
           placeholder="Username"
           class="form-control mb-3"
           autocomplete="off"
           required>

    <input type="password"
           name="admin_pass"
           placeholder="Password"
           class="form-control mb-3"
           autocomplete="new-password"
           required>

    <button class="btn btn-success w-100">Login</button>
</form>

<p style="color:red;">{error}</p>
</div>
</body>
</html>
"""

# ================= ADMIN DASHBOARD =================
# ================= ADMIN DASHBOARD =================
@app.route("/admin_dashboard", methods=["GET","POST"])
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    # Handle uploads
    if request.method == "POST":
        # Homepage banner
        if "banner" in request.files:
            file = request.files["banner"]
            if file.filename:
                path = os.path.join("static", "banner.jpg")
                file.save(path)
        # Ramadan badge
        if "ramadan_badge" in request.files:
            file = request.files["ramadan_badge"]
            if file.filename:
                path = os.path.join("static", "ramadan_badge.png")
                file.save(path)

    # Check if files exist
    banner_exists = os.path.exists("static/banner.jpg")
    ramadan_exists = os.path.exists("static/ramadan_badge.png")

    html = """
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:#f8f9fa;}
.card{border:none;border-radius:15px;transition:0.3s;}
.card:hover{transform:scale(1.05);box-shadow:0 10px 25px rgba(0,0,0,0.2);}
.btn-edit{background:linear-gradient(45deg,#ff6600,#ff0000);border:none;color:white;font-weight:bold;}
.position-relative{position:relative;}
.banner-upload{margin-bottom:20px;padding:15px;background:#222;color:white;border-radius:10px;}
.circle-banner{border-radius:50%;width:80px;height:80px;object-fit:cover;margin:5px;}
.delete-btn{position:absolute;top:-5px;right:-5px;background:red;color:white;border-radius:50%;padding:3px 6px;text-decoration:none;font-weight:bold;}
</style>
</head>
<body>
<div class="container mt-4">
<h2>Admin Dashboard</h2>
<a href="/" class="btn btn-dark mb-3">Home</a>
<a href="/add_product" class="btn btn-success mb-3">➕ Add Product</a>

<!-- Banner Upload Form -->
<div class="banner-upload">
<h5>Upload Homepage Banner</h5>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="banner" class="form-control mb-2" required>
    <button class="btn btn-primary w-100">Upload Banner</button>
</form>
{% if banner_exists %}
<div style="position:relative;display:inline-block;margin-top:10px;">
    <img src="{{ url_for('static', filename='banner.jpg') }}" class="circle-banner">
    <a href="/delete_banner" class="delete-btn">❌</a>
</div>
{% endif %}

<h5 class="mt-3">Upload Ramadan Badge</h5>
<form method="post" enctype="multipart/form-data">
    <input type="file" name="ramadan_badge" class="form-control mb-2" required>
    <button class="btn btn-primary w-100">Upload Badge</button>
</form>
{% if ramadan_exists %}
<div style="position:relative;display:inline-block;margin-top:10px;">
    <img src="{{ url_for('static', filename='ramadan_badge.png') }}" class="circle-banner">
    <a href="/delete_ramadan_badge" class="delete-btn">❌</a>
</div>
{% endif %}
</div>

<div class="row mt-4">
{% for p in products %}
<div class='col-md-4 mb-4'>
<div class='card p-3 text-center position-relative'>
<a href='/delete_product/{{p.id}}' class='delete-btn'>✖</a>
{% if p.image %}<img src='{{p.image}}' style='width:100%;height:150px;object-fit:cover;border-radius:10px;'>{% endif %}
<h5>{{p.title}}</h5>
<p>{{p.description}}</p>
<h6>PKR {{p.price}}</h6>
<a href='/edit/{{p.id}}' class='btn btn-edit mt-2 w-100'>⚙️ Edit Product</a>
</div>
</div>
{% endfor %}
</div>
</div>
</body>
</html>
"""
    return render_template_string(html, banner_exists=banner_exists, ramadan_exists=ramadan_exists, products=products)

# ---------------- Delete Banner ----------------
@app.route("/delete_banner")
def delete_banner():
    if not session.get("admin"):
        return redirect("/admin")
    path = "static/banner.jpg"
    if os.path.exists(path):
        os.remove(path)
    return redirect("/admin_dashboard")

# ---------------- Delete Ramadan Badge ----------------
@app.route("/delete_ramadan_badge")
def delete_ramadan_badge():
    if not session.get("admin"):
        return redirect("/admin")
    path = "static/ramadan_badge.png"
    if os.path.exists(path):
        os.remove(path)
    return redirect("/admin_dashboard")
# ================= ORDER HISTORY =================
@app.route("/order_history")
def order_history_page():
    html = """
    <html>
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{background:linear-gradient(45deg,#007bff,#ff0000);}
        .table{background:white;}
    </style>
    </head>
    <body>
    <div class="container mt-5">
    <h2 class="text-white">Order History</h2>
    <table class="table table-bordered mt-3">
    <tr>
        <th>Name</th>
        <th>Product</th>
        <th>Quantity</th>
        <th>Total</th>
        <th>Delivery</th>
    </tr>
    """

    for o in order_history:
        html += f"""
        <tr>
            <td>{o['name']}</td>
            <td>{o['product']}</td>
            <td>{o['quantity']}</td>
            <td>PKR {o['total']}</td>
            <td>{o['delivery']}</td>
        </tr>
        """

    html += """
    </table>
    <a href="/" class="btn btn-dark">Back</a>
    </div>
    </body>
    </html>
    """
    return html

# ================= ADD PRODUCT =================
@app.route("/add_product", methods=["GET","POST"])
def add_product():
    if not session.get("admin"):
        return redirect("/admin")

    if request.method == "POST":
        new_id = max([p["id"] for p in products]) + 1 if products else 1
        title = request.form["title"]
        price = int(request.form["price"])
        desc = request.form["description"]

        image_list = []

        if "images" in request.files:
            files = request.files.getlist("images")
            for img in files[:5]:   # max 5 images
                if img and img.filename:
                    filename = secure_filename(img.filename)
                    path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                    img.save(path)
                    image_list.append(url_for('static', filename='uploads/' + filename))

        products.append({
            "id": new_id,
            "title": title,
            "price": price,
            "description": desc,
            "images": image_list,
            "ratings": []
        })

        save_products()
        return redirect("/admin_dashboard")

    return """
    <html>
    <body class="container mt-5">
    <h2>Add Product (Max 5 Images)</h2>
    <form method="post" enctype="multipart/form-data">
        <input name="title" class="form-control mb-2" placeholder="Title" required>
        <input name="price" type="number" class="form-control mb-2" placeholder="Price" required>
        <textarea name="description" class="form-control mb-2" placeholder="Description" required></textarea>

        <label>Select 1 to 5 Images</label>
        <input type="file" name="images" multiple class="form-control mb-3">

        <button class="btn btn-success w-100">Add Product</button>
    </form>
    </body>
    </html>
"""

# ================= EDIT PRODUCT =================
@app.route("/edit/<int:pid>", methods=["GET","POST"])
def edit_product(pid):
    if not session.get("admin"):
        return redirect("/admin")

    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return "Product not found ❌"

    if "images" not in product:
        product["images"] = []

    if request.method == "POST":
        product["title"] = request.form["title"]
        product["description"] = request.form["description"]

        # Add new images (max total 5)
        files = request.files.getlist("images")
        for img in files:
            if img and img.filename and len(product["images"]) < 5:
                filename = secure_filename(img.filename)
                path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                img.save(path)
                product["images"].append(
                    url_for('static', filename='uploads/' + filename)
                )

        save_products()
        return redirect("/edit/" + str(pid))

    # Image preview section with delete button
    image_html = ""
    for img in product["images"]:
        image_html += f"""
        <div style="position:relative;display:inline-block;margin:10px;">
            <img src="{img}" width="150" height="150"
                 style="object-fit:cover;border-radius:10px;">
            <a href="/delete_image/{pid}?img={img}"
               style="position:absolute;top:-8px;right:-8px;
                      background:red;color:white;
                      border-radius:50%;padding:4px 8px;
                      text-decoration:none;font-weight:bold;">
               ✖
            </a>
        </div>
        """

    return f"""
    <html>
    <body class="container mt-5">
    <h2>Edit Product (Max 5 Images)</h2>

    <form method="post" enctype="multipart/form-data">
        <input name="title" value="{product['title']}" class="form-control mb-2">

        <textarea name="description" class="form-control mb-3">{product['description']}</textarea>

        <label>Add Images (Max 5 total)</label>
        <input type="file" name="images" multiple class="form-control mb-3">

        <button class="btn btn-warning w-100">Update</button>
    </form>

    <hr>
    <h4>Uploaded Images</h4>
    {image_html}

    <br><br>
    <a href="/admin_dashboard" class="btn btn-dark">Back</a>
    </body>
    </html>
"""


#================== DELETE IMAGE =================
@app.route("/delete_image/<int:pid>")
def delete_image(pid):
    if not session.get("admin"):
        return redirect("/admin")

    img = request.args.get("img")

    product = next((p for p in products if p["id"] == pid), None)
    if product and img in product["images"]:
        product["images"].remove(img)
        save_products()

    return redirect("/edit/" + str(pid))
# ================= ADD TO CART =================
@app.route("/add_to_cart/<int:pid>", methods=["GET","POST"])
def add_to_cart(pid):
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return "<h2>Product not found ❌</h2><a href='/'>Back</a>"

    # Quantity and size from GET parameters
    quantity = int(request.args.get("quantity", 1))
    size = request.args.get("size", "N/A")

    # Store in session cart
    session["cart"] = {
        "pid": pid,
        "quantity": quantity,
        "size": size
    }

    return redirect("/checkout")
# Product Detail Route
@app.route("/product/<int:pid>", methods=["GET","POST"])
def product_detail(pid):
    product = next((p for p in products if p["id"] == pid), None)
    if not product:
        return "<h2>Product not found ❌</h2><a href='/'>Back</a>"

    # Ramadan badge path
    ramadan_badge_path = "static/ramadan_badge.png" if os.path.exists("static/ramadan_badge.png") else None

    return render_template_string("""
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body{background:black;color:white;font-family:sans-serif;}
.container{max-width:900px;margin:auto;padding:20px;}
.product-img{width:100%;height:400px;object-fit:contain;background:#000;border-radius:10px;position:relative;}
.btn-cart{background:#ff6600;border:none;color:white;padding:10px 20px;font-size:16px;margin-top:10px;border-radius:10px;cursor:pointer;}
.badge-ramadan{
    width:60px;
    height:60px;
    border-radius:50%;
    position:absolute;
    top:10px;
    left:10px;
    z-index:10;
    border:2px solid #fff;
    background:#fff;
    object-fit:cover;
}
</style>
</head>
<body>
<div class="container">
<h2>{{product['title']}}</h2>
<div style="position:relative;">
    <img src="{{product.images[0] if product.images else product.image}}" class="product-img">
    {% if ramadan_badge_path %}
        <img src="{{ url_for('static', filename='ramadan_badge.png') }}" class="badge-ramadan">
    {% endif %}
</div>
<p>{{product['description']}}</p>
<h4>PKR {{product['price']}}</h4>
<form action="/add_to_cart/{{product['id']}}" method="get">
<input type="number" name="quantity" value="1" min="1" class="form-control mb-2" style="max-width:100px;">
<button class="btn-cart">Add To Cart</button>
</form>
<a href="/" class="btn btn-dark mt-3">⬅ Back</a>
</div>
</body>
</html>
""", product=product, ramadan_badge_path=ramadan_badge_path)




# ================= APP RUN =================
if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
