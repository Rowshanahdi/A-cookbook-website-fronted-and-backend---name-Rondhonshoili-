let listProductHTML = document.querySelector('.listProduct');
let listCartHTML = document.querySelector('.listCart');
let iconCart = document.querySelector('.icon-cart');
let iconCartSpan = document.querySelector('.icon-cart span');
let body = document.querySelector('body');
let closeCart = document.querySelector('.close');
let products = [];
let cart = [];
console.log("app.js is loaded");

// Cart toggle
iconCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});
closeCart.addEventListener('click', () => {
    body.classList.toggle('showCart');
});

// Add products to HTML
const addDataToHTML = () => {
    if(products.length > 0) {
        products.forEach(product => {
            let newProduct = document.createElement('div');
            newProduct.dataset.id = product.id;
            newProduct.classList.add('item');
            newProduct.innerHTML = 
            `<img src="${product.image}" alt="">
            <h2>${product.name}</h2>
            <div class="price">${product.price}৳</div>
            <button class="addCart">Add To Cart</button>`;
            listProductHTML.appendChild(newProduct);
        });
    }
};

// Event for Add to Cart
listProductHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if(positionClick.classList.contains('addCart')){
        let id_product = positionClick.parentElement.dataset.id;
        addToCart(id_product);
    }
});

// Add item to cart
const addToCart = (product_id) => {
    let positionThisProductInCart = cart.findIndex((value) => value.product_id == product_id);
    if(cart.length <= 0){
        cart = [{
            product_id: product_id,
            quantity: 1
        }];
    } else if(positionThisProductInCart < 0){
        cart.push({
            product_id: product_id,
            quantity: 1
        });
    } else {
        cart[positionThisProductInCart].quantity += 1;
    }
    addCartToHTML();
    addCartToMemory();
    updateCartInDatabase(); // ✅ Update server cart
};

// Save cart to local storage
const addCartToMemory = () => {
    localStorage.setItem('cart', JSON.stringify(cart));
};

// Display cart in HTML
const addCartToHTML = () => {
    listCartHTML.innerHTML = '';
    let totalQuantity = 0;
    if(cart.length > 0){
        cart.forEach(item => {
            totalQuantity += item.quantity;
            let newItem = document.createElement('div');
            newItem.classList.add('item');
            newItem.dataset.id = item.product_id;

            let positionProduct = products.findIndex((value) => value.id == item.product_id);
            let info = products[positionProduct];
            newItem.innerHTML = `
                <div class="image">
                    <img src="${info.image}">
                </div>
                <div class="name">${info.name}</div>
                <div class="totalPrice">${info.price * item.quantity} ৳</div>
                <div class="quantity">
                    <span class="minus"><</span>
                    <span>${item.quantity}</span>
                    <span class="plus">></span>
                </div>
            `;
            listCartHTML.appendChild(newItem);
        });
    }
    iconCartSpan.innerText = totalQuantity;
    updateTotalAmount();
};

// Cart quantity change
listCartHTML.addEventListener('click', (event) => {
    let positionClick = event.target;
    if(positionClick.classList.contains('minus') || positionClick.classList.contains('plus')){
        let product_id = positionClick.parentElement.parentElement.dataset.id;
        let type = positionClick.classList.contains('plus') ? 'plus' : 'minus';
        changeQuantityCart(product_id, type);
    }
});

const changeQuantityCart = (product_id, type) => {
    let positionItemInCart = cart.findIndex((value) => value.product_id == product_id);
    if(positionItemInCart >= 0){
        if(type === 'plus'){
            cart[positionItemInCart].quantity += 1;
        } else {
            let newQty = cart[positionItemInCart].quantity - 1;
            if(newQty > 0){
                cart[positionItemInCart].quantity = newQty;
            } else {
                cart.splice(positionItemInCart, 1);
            }
        }
    }
    addCartToHTML();
    addCartToMemory();
    updateTotalAmount();
    updateCartInDatabase(); // ✅ Update server cart
};

// Load data and initialize
const initApp = () => {
    fetch(productsJsonUrl)
    .then(response => response.json())
    .then(data => {
        products = data;
        addDataToHTML();

        if(localStorage.getItem('cart')){
            cart = JSON.parse(localStorage.getItem('cart'));
            addCartToHTML();
        }
    });
};
initApp();

// CSRF Token Fetcher
function getCSRFToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        if (cookie.trim().startsWith('csrftoken=')) {
            return cookie.trim().substring('csrftoken='.length);
        }
    }
    return '';
}

// ✅ Sync cart to Django DB
const updateCartInDatabase = () => {
    fetch('/update-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ cart }),
        credentials: 'include'
    })
    .then(res => {
        if (!res.ok) throw new Error("Cart update failed");
        return res.json();
    })
    .then(data => {
        console.log("✅ Cart updated to server");
    })
    .catch(error => {
        console.error("❌ Error sending cart to server:", error);
    });
};

// Checkout button
document.querySelector('.checkOut').addEventListener('click', () => {
    fetch('/checkout-save-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({ cart }),
        credentials: 'include'
    })
    .then(res => res.json())
    .then(data => {
        if (data.status === 'success') {
            // Redirect with total price as query param
            window.location.href = `/payment/?total=${data.total.toFixed(2)}`;
        } else {
            alert("Failed to save cart.");
        }
    })
    .catch(err => {
        alert("Error: " + err);
    });
});


// Show total in cart
const updateTotalAmount = () => {
    let total = 0;
    cart.forEach(item => {
        let product = products.find(p => p.id == item.product_id);
        if (product) {
            total += product.price * item.quantity;
        }
    });

    let totalDisplay = document.querySelector('.totalAmountDisplay');
    if(!totalDisplay){
        totalDisplay = document.createElement('div');
        totalDisplay.classList.add('totalAmountDisplay');
        totalDisplay.style.fontWeight = 'bold';
        totalDisplay.style.fontSize = '18px';
        totalDisplay.style.marginTop = '10px';
        document.querySelector('.cartTab').appendChild(totalDisplay);
    }
    totalDisplay.textContent = `Total: ৳ ${total.toFixed(2)}`;
};
