import React, { useState } from "react";
import "./App.css";
import ShoppingCart from "./components/ShoppingCart";
import Chat from "./components/Chat";
import PopUp from "./components/PopUp";
import logo from "./assets/MealMate-logo.png";


function App() {
    const [cart, setCart] = useState([]); // Manage cart items
    const [showModal, setShowModal] = useState(true);
    const [userPreferences, setUserPreferences] = useState({});

    const handleModalSubmit = (preferences) => {
        setUserPreferences(preferences);
        setShowModal(false); // Close the modal
        console.log("User Preferences:", preferences);
    };

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
                        <Chat setCart={setCart} cart={cart} preferences={userPreferences} />
                    </div>
                    <div className="scart">
                        <ShoppingCart cart={cart} setCart={setCart} />
                    </div>
                </div>
            </main>
            {showModal && <PopUp onSubmit={handleModalSubmit} />}
        </div>
    );
}

export default App;
