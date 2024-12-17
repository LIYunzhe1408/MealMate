import React, { useState, useEffect } from "react";
import "./App.css";
import ShoppingCart from "./components/ShoppingCart";
import Chat from "./components/Chat";
import BudgetModal from "./components/BudgetModal";
import logo from "./assets/MealMate-logo.png";

function App() {
    const [budgetPreference, setBudgetPreference] = useState(null); // Budget preference state
    const [showModal, setShowModal] = useState(false); // Modal visibility state
    const [cart, setCart] = useState([]); // Manage cart items

    useEffect(() => {
        // Check if a budget preference is already saved in localStorage
        const savedBudget = localStorage.getItem("budgetPreference");
        if (savedBudget) {
            setBudgetPreference(parseInt(savedBudget));
            setShowModal(false); // Close the modal if budget is already set
        }
    }, []);

    const handleSetBudgetPreference = (budget) => {
        console.log(`Budget Sensitivity Selected: ${budget}`); // Log the budget sensitivity
        setBudgetPreference(budget); // Save budget preference to state
        localStorage.setItem("budgetPreference", budget); // Save to localStorage for persistence
        setShowModal(false); // Close the modal
    };

    return (
        <div className="app">
            {/* Show Budget Modal */}
            {showModal && (
                <BudgetModal setBudgetPreference={handleSetBudgetPreference} />
            )}

            {/* App content when modal is closed */}
            {!showModal && (
                <>
                    <header className="header">
                        <img src={logo} alt="MealMate Logo" className="logo" />
                        {/* Uncomment the nav section if needed */}
                        {/*<nav>
                            <a href="#shop">Shop</a>
                            <a href="#about">About</a>
                            <a href="#contact">Contact</a>
                        </nav>*/}
                    </header>
                    <main className="main">
                        <div className="content-container">
                            <div className="char">
                                <Chat
                                    setCart={setCart}
                                    cart={cart}
                                    budgetPreference={budgetPreference} // Pass budget to Chat
                                />
                            </div>
                            <div className="scart">
                                <ShoppingCart
                                    cart={cart}
                                    setCart={setCart}
                                />
                            </div>
                        </div>
                        <button
                            className="reset-button"
                            onClick={() => {
                                localStorage.removeItem("budgetPreference");
                                setBudgetPreference(null);
                                setShowModal(true);
                            }}
                        >
                            Reset Budget Preference
                        </button>
                    </main>
                </>
            )}
        </div>
    );
}

export default App;
