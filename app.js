// ===== FOOD DATA (also fetched from API) =====
const FOODS = [
  { id:1, name:"Margherita Pizza", category:"Pizza", price:299, rating:4.5, restaurant:"Pizza Palace", emoji:"🍕" },
  { id:2, name:"Pepperoni Pizza", category:"Pizza", price:349, rating:4.7, restaurant:"Pizza Palace", emoji:"🍕" },
  { id:3, name:"Classic Burger", category:"Burger", price:199, rating:4.3, restaurant:"Burger Barn", emoji:"🍔" },
  { id:4, name:"Cheese Burger", category:"Burger", price:249, rating:4.6, restaurant:"Burger Barn", emoji:"🍔" },
  { id:5, name:"Chicken Biryani", category:"Biryani", price:279, rating:4.8, restaurant:"Biryani House", emoji:"🍛" },
  { id:6, name:"Veg Biryani", category:"Biryani", price:229, rating:4.5, restaurant:"Biryani House", emoji:"🍛" },
  { id:7, name:"Spaghetti Carbonara", category:"Pasta", price:319, rating:4.4, restaurant:"La Pasta", emoji:"🍝" },
  { id:8, name:"Penne Arrabbiata", category:"Pasta", price:289, rating:4.2, restaurant:"La Pasta", emoji:"🍝" },
  { id:9, name:"Chocolate Lava Cake", category:"Dessert", price:149, rating:4.9, restaurant:"Sweet Spot", emoji:"🍰" },
  { id:10, name:"Tiramisu", category:"Dessert", price:179, rating:4.7, restaurant:"Sweet Spot", emoji:"🍰" },
  { id:11, name:"Mango Lassi", category:"Drinks", price:99, rating:4.6, restaurant:"Refresh Hub", emoji:"🥤" },
  { id:12, name:"Cold Coffee", category:"Drinks", price:129, rating:4.4, restaurant:"Refresh Hub", emoji:"🥤" },
  { id:13, name:"Caesar Salad", category:"Salad", price:219, rating:4.3, restaurant:"Green Leaf", emoji:"🥗" },
  { id:14, name:"Greek Salad", category:"Salad", price:239, rating:4.5, restaurant:"Green Leaf", emoji:"🥗" },
  { id:15, name:"Paneer Tikka Pizza", category:"Pizza", price:369, rating:4.6, restaurant:"Fusion Bites", emoji:"🍕" },
  { id:16, name:"Double Patty Burger", category:"Burger", price:299, rating:4.8, restaurant:"Burger Barn", emoji:"🍔" },
];

// ===== STATE =====
let cart = JSON.parse(localStorage.getItem('zomato_cart') || '[]');
let currentPage = 'home';
let filteredFoods = [...FOODS];

// ===== PAGE NAVIGATION =====
function showPage(page) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.getElementById('page-' + page).classList.add('active');
  currentPage = page;
  window.scrollTo(0, 0);

  if (page === 'home') renderPopular();
  if (page === 'menu') renderMenu();
  if (page === 'cart') renderCart();
  if (page === 'checkout') renderCheckout();
}

// ===== RENDER FOOD CARD =====
function createFoodCard(food) {
  const inCart = cart.find(i => i.id === food.id);
  return `
    <div class="food-card">
      <div class="food-img">${food.emoji}</div>
      <div class="food-info">
        <div class="food-name">${food.name}</div>
        <div class="food-meta">
          <span class="food-cat">${food.category}</span>
          <span class="food-rating">★ ${food.rating}</span>
        </div>
        <div class="food-restaurant">🏪 ${food.restaurant}</div>
        <div class="food-footer">
          <span class="food-price">₹${food.price}</span>
          <button class="add-btn" onclick="addToCart(${food.id})" id="btn-${food.id}">
            ${inCart ? `✓ Added (${inCart.qty})` : 'Add to Cart'}
          </button>
        </div>
      </div>
    </div>`;
}

// ===== POPULAR FOODS (home) =====
function renderPopular() {
  const popular = [...FOODS].sort((a,b) => b.rating - a.rating).slice(0, 8);
  document.getElementById('popularGrid').innerHTML = popular.map(createFoodCard).join('');
}

// ===== MENU =====
function renderMenu() {
  document.getElementById('menuGrid').innerHTML = filteredFoods.map(createFoodCard).join('');
}

function filterFoods() {
  const search = document.getElementById('searchInput')?.value.toLowerCase() || '';
  const cat = document.getElementById('categoryFilter')?.value || '';
  const sort = document.getElementById('sortFilter')?.value || '';

  filteredFoods = FOODS.filter(f => {
    const matchSearch = f.name.toLowerCase().includes(search) || f.category.toLowerCase().includes(search);
    const matchCat = !cat || f.category === cat;
    return matchSearch && matchCat;
  });

  if (sort === 'price-asc') filteredFoods.sort((a,b) => a.price - b.price);
  else if (sort === 'price-desc') filteredFoods.sort((a,b) => b.price - a.price);
  else if (sort === 'rating') filteredFoods.sort((a,b) => b.rating - a.rating);

  renderMenu();
}

function filterByCategory(cat) {
  showPage('menu');
  setTimeout(() => {
    const sel = document.getElementById('categoryFilter');
    if (sel) sel.value = cat;
    filterFoods();
  }, 50);
}

// ===== CART LOGIC =====
function addToCart(foodId) {
  const food = FOODS.find(f => f.id === foodId);
  if (!food) return;

  const existing = cart.find(i => i.id === foodId);
  if (existing) {
    existing.qty += 1;
  } else {
    cart.push({ ...food, qty: 1 });
  }
  saveCart();
  updateCartBadge();
  showAddedFeedback(foodId);

  // Update current page if menu
  if (currentPage === 'menu') renderMenu();
  if (currentPage === 'home') renderPopular();
}

function showAddedFeedback(foodId) {
  const btn = document.getElementById('btn-' + foodId);
  if (!btn) return;
  const item = cart.find(i => i.id === foodId);
  if (item) btn.textContent = `✓ Added (${item.qty})`;
}

function changeQty(foodId, delta) {
  const idx = cart.findIndex(i => i.id === foodId);
  if (idx === -1) return;
  cart[idx].qty += delta;
  if (cart[idx].qty <= 0) cart.splice(idx, 1);
  saveCart();
  updateCartBadge();
  renderCart();
}

function removeFromCart(foodId) {
  cart = cart.filter(i => i.id !== foodId);
  saveCart();
  updateCartBadge();
  renderCart();
}

function saveCart() {
  localStorage.setItem('zomato_cart', JSON.stringify(cart));
}

function updateCartBadge() {
  const total = cart.reduce((s, i) => s + i.qty, 0);
  document.getElementById('cartBadge').textContent = total;
}

// ===== RENDER CART =====
function renderCart() {
  const container = document.getElementById('cartItems');
  const summary = document.getElementById('cartSummary');

  if (cart.length === 0) {
    container.innerHTML = `
      <div class="empty-cart">
        <div class="icon">🛒</div>
        <h3>Your cart is empty</h3>
        <p>Add some delicious food to get started!</p>
        <button class="add-btn" style="margin-top:16px" onclick="showPage('menu')">Browse Menu</button>
      </div>`;
    summary.innerHTML = '';
    return;
  }

  container.innerHTML = cart.map(item => `
    <div class="cart-item">
      <div class="cart-item-emoji">${item.emoji}</div>
      <div class="cart-item-info">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-price">₹${item.price} × ${item.qty} = ₹${item.price * item.qty}</div>
      </div>
      <div class="qty-controls">
        <button class="qty-btn" onclick="changeQty(${item.id}, -1)">−</button>
        <span class="qty-num">${item.qty}</span>
        <button class="qty-btn" onclick="changeQty(${item.id}, 1)">+</button>
        <button class="remove-btn" onclick="removeFromCart(${item.id})">🗑️</button>
      </div>
    </div>`).join('');

  const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const delivery = 40;
  const tax = Math.round(subtotal * 0.05);
  const total = subtotal + delivery + tax;

  summary.innerHTML = `
    <h3>Order Summary</h3>
    <div class="summary-row"><span>Subtotal</span><span>₹${subtotal}</span></div>
    <div class="summary-row"><span>Delivery Fee</span><span>₹${delivery}</span></div>
    <div class="summary-row"><span>GST (5%)</span><span>₹${tax}</span></div>
    <div class="summary-row total"><span>Total</span><span>₹${total}</span></div>
    <button class="checkout-btn" onclick="showPage('checkout')">Proceed to Checkout →</button>`;
}

// ===== RENDER CHECKOUT =====
function renderCheckout() {
  const summary = document.getElementById('orderSummary');
  const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const delivery = 40, tax = Math.round(subtotal * 0.05), total = subtotal + delivery + tax;

  if (cart.length === 0) {
    summary.innerHTML = '<p style="color:var(--gray-600)">No items in cart.</p>';
    return;
  }

  summary.innerHTML = `
    <h3>Order Summary</h3>
    ${cart.map(i => `
      <div class="order-item-row">
        <span>${i.emoji} ${i.name} × ${i.qty}</span>
        <span>₹${i.price * i.qty}</span>
      </div>`).join('')}
    <hr style="margin:16px 0; border-color: var(--gray-100)">
    <div class="order-item-row"><span>Delivery</span><span>₹${delivery}</span></div>
    <div class="order-item-row"><span>GST</span><span>₹${tax}</span></div>
    <div class="order-item-row" style="font-weight:800;color:var(--red);font-size:1.1rem">
      <span>Total</span><span>₹${total}</span>
    </div>`;
}

// ===== PLACE ORDER =====
function placeOrder() {
  const name = document.getElementById('custName').value.trim();
  const mobile = document.getElementById('custMobile').value.trim();
  const email = document.getElementById('custEmail').value.trim();
  const address = document.getElementById('custAddress').value.trim();

  if (!name || !mobile || !email || !address) {
    alert('Please fill in all delivery details!');
    return;
  }
  if (cart.length === 0) {
    alert('Your cart is empty!');
    return;
  }

  const orderId = 'ZMT' + Date.now().toString().slice(-6);
  const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const total = subtotal + 40 + Math.round(subtotal * 0.05);

  // Build order object (would POST to /add-order in real app)
  const order = {
    order_id: orderId,
    customer: { name, mobile, email, address },
    items: cart,
    total,
    status: 'Placed',
    created_at: new Date().toISOString(),
  };

  // Save to localStorage (simulate)
  const orders = JSON.parse(localStorage.getItem('zomato_orders') || '[]');
  orders.push(order);
  localStorage.setItem('zomato_orders', JSON.stringify(orders));

  // Clear cart
  cart = [];
  saveCart();
  updateCartBadge();

  // Show success
  document.getElementById('orderIdDisplay').textContent = `Order ID: ${orderId}`;
  document.getElementById('successModal').style.display = 'flex';

  /* In a real app, you'd call:
  fetch('http://localhost:5000/add-order', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(order)
  }).then(r => r.json()).then(data => console.log(data));
  */
}

function closeModal() {
  document.getElementById('successModal').style.display = 'none';
  showPage('home');
}

// ===== INIT =====
document.addEventListener('DOMContentLoaded', () => {
  updateCartBadge();
  renderPopular();

})
async function placeOrder() {

  const name = document.getElementById('custName').value.trim();
  const mobile = document.getElementById('custMobile').value.trim();
  const email = document.getElementById('custEmail').value.trim();
  const address = document.getElementById('custAddress').value.trim();

  if (!name || !mobile || !email || !address) {
      alert("Fill all fields");
      return;
  }

  const subtotal = cart.reduce((s, i) => s + i.price * i.qty, 0);
  const total = subtotal + 40 + Math.round(subtotal * 0.05);

  const order = {
      name,
      mobile,
      email,
      address,
      total,
      items: cart
      
  }

  try {

      const response = await fetch(
          "http://127.0.0.1:5000/add-order",
          {
              method: "POST",
              headers: {
                  "Content-Type": "application/json"
              },
              body: JSON.stringify(order)
          }
      );

      const result = await response.json();

      console.log(result);

      alert("Order Placed Successfully");

  } catch(error) {

      console.error(error);

      alert("Backend Connection Failed");

  };
}