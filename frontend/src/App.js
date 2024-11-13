import React from "react";
import "./App.css";
import ShoppingCart from "./components/ShoppingCart";
import Chat from "./components/Chat";
import logo from "./assets/name.png"

function App() {
    return (
        <div className="app">
            <header className="header">

                <img src={logo} alt="TJ Logo" className="logo" /> {/* Replace text with logo */}
                <nav>
                    <a href="#shop">Shop</a>
                    <a href="#about">About</a>
                    {/*<a href="#journal">Journal</a>*/}
                    <a href="#contact">Contact</a>
                    {/*<button className="icon-button">🔍</button>*/}
                    {/*<button className="icon-button">👤</button>*/}
                    {/*<button className="icon-button">📧</button>*/}
                </nav>
            </header>
            <main className="main">
                <div className="char">
                    <Chat />
                </div>
                <div className="scart">
                    <ShoppingCart />
                </div>

            </main>
        </div>
    );
}

export default App;
