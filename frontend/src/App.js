import React, { useState } from "react";
import "./App.css";
import ShoppingCart from "./components/ShoppingCart";
import Chat from "./components/Chat";
import logo from "./assets/MealMate-logo.png";

function App() {
    const [cart, setCart] = useState([]); // Manage cart items

    return (
        <div className="app">
            <header className="header">
                <img src={logo} alt="TJ Logo" className="logo" />
                {/*<nav>*/}
                {/*    <a href="#shop">Shop</a>*/}
                {/*    <a href="#about">About</a>*/}
                {/*    <a href="#contact">Contact</a>*/}
                {/*</nav>*/}
            </header>
            <main className="main">
                <div className="content-container">
                    <div className="char">
                        <Chat setCart={setCart} cart={cart} />
                    </div>
                    <div className="scart">
                        <ShoppingCart cart={cart} setCart={setCart} />
                    </div>
                </div>
            </main>
        </div>
    );
}

export default App;
