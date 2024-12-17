import React, { useState } from "react";
import "./ShoppingCart.css";

function ShoppingCart({ cart, setCart }) {
    const [showCheckoutBox, setShowCheckoutBox] = useState(false);
    const [showPaymentBox, setShowPaymentBox] = useState(false);

    const handleCheckout = () => {
        setShowCheckoutBox(true);
    };

    const handleProceedToPayment = () => {
        setShowCheckoutBox(false);
        setShowPaymentBox(true);
    };

    const closePaymentBox = () => {
        setShowPaymentBox(false);
    };

    const updateQuantity = (index, delta) => {
        const updatedCart = [...cart];
        updatedCart[index].quantity = Math.max(0, updatedCart[index].quantity + delta);
        setCart(updatedCart);
    };

    const total = cart.reduce((acc, item) => acc + item.price * item.quantity, 0);

    return (
        <div className="shopping-cart">
            <h2>Your Shopping Cart</h2>
            {cart.length === 0 ? (
                <p className="empty-cart-hint">Your cart is empty. Start adding items!</p>
            ) : (
                <>
                    <div className="cart-scroll-box">
                        <ul className="cart-items">
                            {cart.map((item, index) => (
                                <li key={index} className="cart-item">
                                    <img src={item.imageUrl} alt={item.name} className="item-image" />
                                    <div className="item-info">
                                        <h3>{item.name}</h3>
                                        <p>${item.price.toFixed(2)}</p>
                                        <p>Quantity: {item.quantity}</p>
                                    </div>
                                </li>
                            ))}
                        </ul>
                    </div>
                    <div className="cart-actions">
                        <button className="checkout-button" onClick={handleCheckout}>
                            Show All Cart
                        </button>
                    </div>
                </>
            )}

            {showCheckoutBox && (
                <div className="checkout-box">
                    <div className="checkout-box-content">
                        <h3>Shopping Cart Confirmation</h3>
                        <table
                            className="checkout-table"
                            style={{
                                border: "none",
                                borderCollapse: "collapse",
                                width: "100%",
                            }}
                        >
                            <thead>
                            <tr style={{ border: "none" }}>
                                <th style={{ border: "none", padding: "8px" }}>Item</th>
                                <th style={{ border: "none", padding: "8px" }}>Quantity</th>
                                <th style={{ border: "none", padding: "8px" }}>Price</th>
                                <th style={{ border: "none", padding: "8px" }}>Total</th>
                                <th style={{ border: "none", padding: "8px" }}>Actions</th>
                            </tr>
                            </thead>
                            <tbody>
                            {cart.map((item, index) => (
                                <tr
                                    key={index}
                                    style={{
                                        backgroundColor: item.quantity === 0 ? "lightgrey" : "white",
                                        border: "none",
                                    }}
                                >
                                    <td style={{ border: "none", padding: "8px" }}>{item.name}</td>
                                    <td style={{ border: "none", padding: "8px" }}>{item.quantity}</td>
                                    <td style={{ border: "none", padding: "8px" }}>${item.price.toFixed(2)}</td>
                                    <td style={{ border: "none", padding: "8px" }}>
                                        ${(item.price * item.quantity).toFixed(2)}
                                    </td>
                                    <td style={{ border: "none", padding: "8px" }}>
                                        <button className="addMinus" style={{marginRight: "5px"}}
                                            onClick={() => updateQuantity(index, -1)}
                                            disabled={item.quantity === 0}
                                        >
                                            -
                                        </button>
                                        <button  className="addMinus" onClick={() => updateQuantity(index, 1)}>+</button>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>

                        <div className="checkout-total">
                            <strong>Total: ${total.toFixed(2)}</strong>
                        </div>
                        <div className="checkout-buttons">
                            <button
                                className="proceed-to-checkout-button"
                                onClick={handleProceedToPayment}
                            >
                                Proceed to Checkout
                            </button>
                            <button
                                className="close-checkout-button"
                                onClick={() => setShowCheckoutBox(false)}
                            >
                                Close
                            </button>
                        </div>
                    </div>
                </div>
            )}


            {/* Payment Method Box */}
            {showPaymentBox && (
                <div className="payment-box">
                    <div className="payment-box-content">
                        <h3>Select a Payment Method</h3>
                        <div className="payment-methods">
                            <button className="payment-method-button">Credit Card</button>
                            <button className="payment-method-button">PayPal</button>
                            <button className="payment-method-button">Apple Pay</button>
                        </div>
                        <button className="close-payment-box-button" onClick={closePaymentBox}>
                            Close
                        </button>
                    </div>
                </div>
            )}
        </div>
    );
}

export default ShoppingCart;
