from flask import Flask, render_template_string, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import os
import json
import smtplib
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from google_auth_oauthlib.flow import Flow
import requests
app = Flask(__name__)
app.secret_key = "super_secure_secret_key_420"

# ================= CONFIG =================
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.email",
          "https://www.googleapis.com/auth/userinfo.profile"]

app = Flask(__name__)
app.secret_key = "super_secure_secret_key_420"

ADMIN_USERNAME = "fmukhtar420@gmail.com"
ADMIN_PASSWORD = "blueberry@420"
ADMIN_EMAIL = "fmukhtar420@gmail.com"
GMAIL_USER = "fmukhtar420@gmail.com"
GMAIL_APP_PASSWORD = "bnap lyde xsxm twql"

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'webp'}

from werkzeug.utils import secure_filename
import os

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
PRODUCTS_FILE = "products.json"

# ---------------- PRODUCTS ----------------
if os.path.exists(PRODUCTS_FILE):
    with open(PRODUCTS_FILE, "r") as f:
        products = json.load(f)
else:
    products = [
        {"id": i, "title": f"Super Product {i}", "price": 2850,
         "description": "Premium Quality Product", "image": "", "ratings": []}
        for i in range(1, 31)
    ]
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

order_history = []

def save_products():
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f)

# ---------------- EMAIL ----------------
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

# ---------------- GOOGLE LOGIN ----------------
@app.route("/login")
def login():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('login_callback', _external=True)
    )
    auth_url, state = flow.authorization_url()
    session['state'] = state
    return redirect(auth_url)

@app.route("/login/callback")
def login_callback():
    flow = Flow.from_client_secrets_file(
        CLIENT_SECRETS_FILE,
        scopes=SCOPES,
        redirect_uri=url_for('login_callback', _external=True)
    )
    flow.fetch_token(authorization_response=request.url)
    credentials = flow.credentials
    id_info = requests.get(
        f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={credentials.token}"
    ).json()
    session['user'] = id_info
    return redirect("/")


# ================= HOME =================
# ================= HOME =================
@app.route("/", methods=["GET"])
def home():
    search = request.args.get("search","").lower()
    filtered = [p for p in products if search in p["title"].lower()]

    html = """
    <html>
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{background:#f8f9fa;}
        .brand{
            font-size:48px;
            font-weight:900;
            background:linear-gradient(45deg,#ff0000,#ff6600);
            -webkit-background-clip:text;
            -webkit-text-fill-color:transparent;
        }
        .card{border:none;border-radius:15px;transition:0.3s;}
        .card:hover{transform:scale(1.05);box-shadow:0 10px 25px rgba(0,0,0,0.2);}
        .btn-cart{
            background:linear-gradient(45deg,#007bff,#00c6ff);
            border:none;
            font-size:18px;
            font-weight:bold;
        }
        .icon{width:45px;margin-left:10px;}

        /* 🔥 IMAGE FIX HERE */
        .product-img{
            width:100%;
            height:350px;
            object-fit:contain;
            background:#f8f9fa;
            border-radius:10px;
        }

        .search-bar{max-width:400px;margin-bottom:20px;}
        a{text-decoration:none;color:black;}
    </style>
    </head>
    <body>
    <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center">
        <div class="brand">🛍 SUPER COLLECTION</div>
        <div>
            <a href="https://www.instagram.com/supercollection6547/" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/2111/2111463.png" class="icon">
            </a>
            <a href="https://www.facebook.com/profile.php?id=61587780675415" target="_blank">
                <img src="https://cdn-icons-png.flaticon.com/512/733/733547.png" class="icon">
            </a>
            <a href="/admin" class="btn btn-dark">Admin Login</a>
            <a href="/order_history" class="btn btn-warning">Orders</a>
        </div>
    </div>

    <form method="get" class="mt-3">
        <input type="text" name="search" placeholder="Search Products" class="form-control search-bar">
        <button class="btn btn-primary mt-2 mb-4">Search</button>
    </form>

    <div class="row mt-4">
    {% for p in filtered %}
        <div class="col-md-4 mb-4">
            <div class="card p-3 text-center">

                {% if p.images %}
                    <a href="/product/{{p.id}}">
                        <img src="{{p.images[0]}}" class="product-img mb-2">
                    </a>
                {% elif p.image %}
                    <a href="/product/{{p.id}}">
                        <img src="{{p.image}}" class="product-img mb-2">
                    </a>
                {% endif %}

                <h5>
                    <a href="/product/{{p.id}}">{{p.title}}</a>
                </h5>
                <p>{{p.description}}</p>
                <h6 class="text-danger">PKR {{p.price}}</h6>
                <form action="/add_to_cart/{{p.id}}" method="post">
                    <input type="number" name="quantity" min="1" value="1" class="form-control mb-2">
                    <button class="btn btn-cart w-100">Add To Cart</button>
                </form>
            </div>
        </div>
    {% endfor %}
    </div>
    </div>
    </body>
    </html>
    """
    return render_template_string(html, filtered=filtered)

# ================= ADD TO CART =================
@app.route("/add_to_cart/<int:pid>", methods=["POST"])
def add_to_cart(pid):
    session["cart"] = {
        "pid": pid,
        "quantity": int(request.form["quantity"])
    }
    return redirect("/checkout")


# ================= CHECKOUT =================
@app.route("/checkout", methods=["GET","POST"])
def checkout():
    if "cart" not in session:
        return redirect("/")

    if request.method == "POST":
        # User input
        name = request.form.get("name")
        age = request.form.get("age")
        gender = request.form.get("gender")
        address = request.form.get("address")
        desc = request.form.get("desc")
        phone = request.form.get("phone")

        # Product lookup safe
        product = next((p for p in products if p["id"] == session["cart"]["pid"]), None)
        if not product:
            return "<h2>Product not found ❌</h2><a href='/'>Back</a>"

        quantity = session["cart"].get("quantity", 1)
        total_price = quantity * product["price"]
        delivery = (datetime.now() + timedelta(days=2)).strftime("%Y-%m-%d")

        # Save order
        order_history.append({
            "name": name,
            "product": product["title"],
            "quantity": quantity,
            "total": total_price,
            "delivery": delivery
        })

        # Send email
        send_email(
            "New Order - Super Collection",
            f"""
Full Name: {name}
Age: {age}
Gender: {gender}
Address: {address}
Order Description: {desc}
phone Number: {phone}
Email: {session.get("user", {}).get("email", "N/A")}

Product: {product['title']}
Quantity: {quantity}
Total: PKR {total_price}
Delivery: {delivery}
"""
        )

        # Animated order confirmation
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
    background: linear-gradient(-45deg,#ff4b2b,#1e90ff,#ffeb3b,#00c6ff,#ff66c4);
    background-size: 400% 400%;
    animation: gradientBG 10s ease infinite;
    font-family: Arial, sans-serif;
}}
@keyframes gradientBG {{
    0% {{background-position:0% 50%;}}
    50% {{background-position:100% 50%;}}
    100% {{background-position:0% 50%;}}
}}
.confirm-box {{
    background:white;
    padding:25px 30px;
    border-radius:15px;
    box-shadow:0 15px 30px rgba(0,0,0,0.3);
    max-width:350px;
    text-align:center;
    animation: fadeIn 1s ease forwards;
    opacity:0;
}}
@keyframes fadeIn {{
    to {{opacity:1;}}
}}
.confirm-box h2 {{
    font-size:26px;
    color:green;
    margin-bottom:12px;
}}
.confirm-box p {{
    font-size:16px;
    margin:4px 0;
}}
.btn-continue {{
    margin-top:12px;
    background:linear-gradient(45deg,#007bff,#00c6ff);
    border:none;
    color:white;
    font-weight:bold;
    font-size:16px;
    padding:8px 16px;
    border-radius:8px;
    text-decoration:none;
}}
</style>
</head>
<body>
<div class="confirm-box">
<h2>Order Confirmed ✅</h2>
<p><strong>Product:</strong> {product['title']}</p>
<p><strong>Quantity:</strong> {quantity}</p>
<p><strong>Total:</strong> PKR {total_price}</p>
<p><strong>Delivery:</strong> {delivery}</p>
<a href="/" class="btn-continue">Continue Shopping</a>
</div>
</body>
</html>
"""

    # GET method → always return checkout form
    return """
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
    body{background:linear-gradient(45deg,#ff4b2b,#1e90ff);}
    .box{max-width:700px;margin:auto;margin-top:50px;padding:40px;border-radius:20px;background:white;}
    .form-label{font-size:22px;font-weight:bold;color:#ff0000;}
    .form-control,select,textarea{font-size:20px;padding:12px;}
    .btn-confirm{background:linear-gradient(45deg,#ff0000,#007bff);border:none;font-size:22px;font-weight:bold;}
</style>
</head>
<body>
<div class="text-center mt-3">
    <a href="/" class="btn btn-dark btn-lg">⬅ Continue Shopping</a>
</div>
<div class="box shadow">
<h2 class="text-center mb-4" style="font-size:35px;color:#007bff;font-weight:bold;">Checkout Details</h2>
<form method="post">
    <label class="form-label">Full Name</label>
    <input name="name" class="form-control mb-3" required>

    <label class="form-label">Age</label>
    <input name="age" type="number" class="form-control mb-3" required>

    <label class="form-label">Gender</label>
    <select name="gender" class="form-control mb-3">
        <option>Female</option>

    </select>

    <label class="form-label">Address</label>
    <textarea name="address" class="form-control mb-3" required></textarea>

    <label class="form-label">Phone Number</label>
        <input name="phone" class="form-control mb-3" required>

    <label class="form-label">Email</label>
    <input name="email" type="email" class="form-control mb-3" required>    

    <label class="form-label">Order Description</label>
    <textarea name="desc" class="form-control mb-4" rows="4"></textarea>


    <button class="btn btn-confirm w-100">Confirm Order</button>
</form>
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

            send_email(
                "Admin Login Alert - Super Collection",
                f"Admin logged in at {datetime.now()}"
            )

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
@app.route("/admin_dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin")

    html = """
    <html>
    <head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body{background:#f8f9fa;}
        .card{border:none;border-radius:15px;transition:0.3s;}
        .card:hover{transform:scale(1.05);box-shadow:0 10px 25px rgba(0,0,0,0.2);}
        .btn-edit{background:linear-gradient(45deg,#ff6600,#ff0000);border:none;color:white;font-weight:bold;}
    </style>
    </head>
    <body>
    <div class="container mt-4">
    <h2>Admin Dashboard</h2>
    <a href="/" class="btn btn-dark mb-3">Home</a>
    <a href="/add_product" class="btn btn-success mb-3">➕ Add Product</a>
    <div class="row">
    """

    for p in products:
        img_tag = f"<img src='{p['image']}' style='width:100%;height:150px;object-fit:cover;border-radius:10px;'/>" if p["image"] else ""
        html += f"""
        <div class='col-md-4 mb-4'>
        <div class='card p-3 text-center'>
            {img_tag}
            <h5>{p['title']}</h5>
            <p>{p['description']}</p>
            <h6>PKR {p['price']}</h6>
            <a href='/edit/{p['id']}' class='btn btn-edit mt-2 w-100'>⚙️ Edit Product</a>
        </div>
        </div>
        """

    html += """
    </div>
    </div>
    </body>
    </html>
    """
    return html

#
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

#==================product detail=================
@app.route("/product/<pid>")
def product_detail(pid):
    try:
        pid = int(pid)
    except:
        return "<h2>Invalid Product ID ❌</h2><a href='/'>Back</a>"

    product = next((p for p in products if int(p.get("id", 0)) == pid), None)
    if not product:
        return "<h2>Product not found ❌</h2><a href='/'>Back</a>"

    # Ab images ka slider
    images = product.get("images")
    if not images:
        if product.get("image"):
            images = [product["image"]]
        else:
            images = ["https://via.placeholder.com/800x1200?text=No+Image"]

    images_js = str(images)

    return f"""
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<style>
body, html {{
    margin:0;
    padding:0;
    height:100%;
    overflow:hidden;
    background:black;
    display:flex;
    justify-content:center;
    align-items:center;
}}
.slider {{
    position:relative;
    width:100%;
    height:100%;
}}
.slider img {{
    width:100%;
    height:100%;
    object-fit:contain;
    background:black;
}}
.arrow {{
    position:absolute;
    top:50%;
    transform:translateY(-50%);
    font-size:60px;
    background:rgba(0,0,0,0.5);
    color:white;
    border:none;
    padding:10px 25px;
    cursor:pointer;
    z-index:10;
    border-radius:8px;
}}
.left {{left:20px;}}
.right {{right:20px;}}
.back-btn {{
    position:absolute;
    top:20px;
    left:20px;
    font-size:20px;
    padding:8px 15px;
    background:rgba(255,255,255,0.8);
    text-decoration:none;
    color:black;
    border-radius:8px;
    z-index:10;
}}
</style>
</head>
<body>

<a href="/" class="back-btn">⬅ Back</a>

<div class="slider">
    <button class="arrow left" onclick="prev()">&#10094;</button>
    <img id="sliderImg" src="{images[0]}">
    <button class="arrow right" onclick="next()">&#10095;</button>
</div>

<script>
let images = {images_js};
let index = 0;

function show() {{
    document.getElementById("sliderImg").src = images[index];
}}

function next() {{
    index = (index + 1) % images.length;
    show();
}}

function prev() {{
    index = (index - 1 + images.length) % images.length;
    show();
}}
</script>

</body>
</html>
"""




if __name__ == "__main__":
    app.run(debug=True)
