import React from "react";
import "./ShoppingCart.css";

function ShoppingCart() {
    const items = [
        {
            name: "French Press",
            price: 30,
            description: "Matte black",
            quantity: 1,
            imageUrl: "/images/FrenchPress.jpg", // Replace with actual image URL
        },
        {
            name: "Espresso Blend",
            price: 15,
            description: "12oz",
            quantity: 1,
            imageUrl: "/images/Espresso Blend.jpeg", // Replace with actual image URL
        },
        {
            name: "Coffee Filters",
            price: 6,
            description: "30 pack",
            quantity: 1,
            imageUrl: "/images/Coffee Filter.jpg", // Replace with actual image URL
        },
    ];
    const total = items.reduce((acc, item) => acc + item.price * item.quantity, 0);

    return (
        <div className="shopping-cart">
            <h2>Your bag ({items.length})</h2>
            <ul className="cart-items">
                {items.map((item, index) => (
                    <li key={index} className="cart-item">
                        <img src={item.imageUrl} alt={item.name} className="item-image" />
                        <div className="item-info">
                            <h3>{item.name}</h3>
                            <p>${item.price}</p>
                            <p className="item-description">{item.description}</p>
                        </div>
                        <div className="item-quantity">
                            <button>-</button>
                            <span>{item.quantity}</span>
                            <button>+</button>
                        </div>
                    </li>
                ))}
            </ul>
            <div className="total-section">
                <div className="subtotal-row">
                    <span>Subtotal</span>
                    <span>${total.toFixed(2)}</span>
                </div>
                <div className="total-row">
                    <span>Total</span>
                    <span>${total.toFixed(2)}</span>
                </div>
                <button className="checkout-button">Checkout</button>
                <button className="continue-shopping-button">Continue shopping</button>
            </div>
        </div>
    );
}

export default ShoppingCart;
