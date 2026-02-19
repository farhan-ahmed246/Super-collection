const products = [
    { name: "Red Dress", price: "Rs 1000", image: "images/product1.jpg" },
    { name: "Blue Top", price: "Rs 1200", image: "images/product2.jpg" },
    { name: "Green Shirt", price: "Rs 1500", image: "images/product3.jpg" }
];

const container = document.getElementById("product-container");

products.forEach(product => {
    const div = document.createElement("div");
    div.className = "product";
    div.innerHTML = `
        <img src="${product.image}" alt="${product.name}">
        <h3>${product.name}</h3>
        <p>${product.price}</p>
        <button onclick="alert('${product.name} added to cart!')">Add to Cart</button>
    `;
    container.appendChild(div);
});
