import React, { useState, useEffect, useRef } from "react";
import "./Chat.css";
import assistantLogo from "../assets/MealMate-chat-logo.png";
import customerAvatar from "../assets/customer.jpg";

function Chat({ setCart, preferences }) {
    // console.log("User Preferences in Chat:", preferences);

    const [messages, setMessages] = useState([
        { sender: "assistant", text: "Hello! I'm your virtual assistant. How can I help you today?" },
    ]);
    const [inputValue, setInputValue] = useState("");
    const [showCheckoutBox, setShowCheckoutBox] = useState(false);

    // Ingredients with recommended and current quantities
    const [ingredients, setIngredients] = useState([]);
    const [shopName, setShopName] = useState([]);
    const [recipe, setRecipe] = useState([]);
    const [recipeSuggestions, setRecipeSuggestions] = useState([]);
    const [loading, setLoading] = useState(false); // Loading state

    // Ref to scroll the chat container
    const chatContainerRef = useRef(null);

    // Automatically scroll to the bottom when messages change
    useEffect(() => {
        if (chatContainerRef.current) {
            chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
        }
    }, [messages]);

    const updateQuantity = (index, delta) => {
        const updatedIngredients = [...ingredients];
        updatedIngredients[index].quantity = Math.max(0, updatedIngredients[index].quantity + delta);
        setIngredients(updatedIngredients);
    };

    const toggleSelect = (index) => {
        const updatedIngredients = [...ingredients];
        const item = updatedIngredients[index];
        if (item.selected) {
            // Drop action: Set current quantity to 0
            item.quantity = 0;
        } else {
            // Pick action: Reset to recommended quantity
            item.quantity = item.recommended;
        }
        item.selected = !item.selected;
        setIngredients(updatedIngredients);
    };

    const handleAddToCart = () => {
        const selectedItems = ingredients.filter((item) => item.selected && item.quantity > 0);
        setCart((prevCart) => [...prevCart, ...selectedItems]); // Add selected items to cart
        setShowCheckoutBox(false);

        // Notify user in chat
        setMessages((prevMessages) => [
            ...prevMessages,
            { sender: "assistant", text: "Ingredients have been added to your cart!" },
        ]);
    };

    const handleTestSend = async () => {
        if (inputValue.trim() !== "") {
            setMessages((prevMessages) => [
                ...prevMessages,
                { sender: "customer", text: inputValue },
            ]);
            setLoading(true); // Show loading overlay

            try {
                const response = await fetch('http://127.0.0.1:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ 
                        message: inputValue,
                        preferences: preferences, // Pass user preferences
                    }),
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! Status: ${response.status}`);
                }

                const data = await response.json();
                console.log("Response from backend:", data);
                if (data.type === "recipe") {
                    // Add recipe cards to the chat
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { sender: "assistant", text: "Here are some recipes you might like:" },
                        {
                            sender: "assistant",
                            recipes: data.recipe, // Pass recipes as part of the message
                        },
                    ]);
                } else if (data.type === "general") {
                    setMessages((prevMessages) => [
                        ...prevMessages,
                        { sender: "assistant", text: data.message },
                    ]);
                }
            } catch (error) {
                console.error("Error:", error);
                setMessages((prevMessages) => [
                    ...prevMessages,
                    { sender: "assistant", text: "Sorry, I couldn't process your request. Please try again." },
                ]);
            } finally {
                setLoading(false); // Show loading overlay
            }

            setInputValue(""); // Clear input field
        }
    };

    return (
        <div className="chat">
            {/*<h2>Chat with us</h2>*/}
            <div className="chat-messages"
                 ref={chatContainerRef}
                 style={{ overflowY: "auto"}}>
                {messages.map((message, index) => (
                    <div key={index} className="chat-message-container">
                        {message.sender === "assistant" && (
                            <img src={assistantLogo} alt="Assistant Logo" className="chat-logo" />
                        )}
                        <div
                            className={`chat-bubble ${message.sender === "customer" ? "customer-bubble" : ""}`}
                        >
                            {message.text && message.text}


                            {message.recipes && (
                                <div className="recipe-cards">
                                    {message.recipes.map((recipe, idx) => (
                                        <div key={idx} className="recipe-card">
                                            <h4>{recipe.title}</h4>
                                            <p><strong>Ingredients:</strong> {recipe.ingredients}</p>
                                            <button
                                                className="select-recipe-button"
                                                onClick={async () => {
                                                    try {
                                                        const selectedRecipe = {
                                                            recipe: {
                                                                title: recipe.title,
                                                                ingredients: Array.isArray(recipe.ingredients) ? recipe.ingredients : recipe.ingredients.split(";"),
                                                            },
                                                            preferences: preferences, // Add user preference to the payload

                                                        };

                                                        console.log("Sending payload to backend:", selectedRecipe);

                                                        setLoading(true); // Show loading overlay
                                                        const response = await fetch('http://127.0.0.1:5000/api/line-cook', {
                                                            method: 'POST',
                                                            headers: {
                                                                'Content-Type': 'application/json',
                                                            },
                                                            body: JSON.stringify(selectedRecipe),
                                                        });

                                                        if (!response.ok) {
                                                            const errorData = await response.json();
                                                            throw new Error(`HTTP error! Status: ${response.status}, Message: ${errorData.error}`);
                                                        }

                                                        const data = await response.json();
                                                        console.log("Backend response:", data);

                                                        let predefinedIngredients = data.formatted_output

                                                        setIngredients(predefinedIngredients);
                                                        setShopName(data.store);
                                                        setRecipe(Object.keys(data.recipe)[0])


                                                        setLoading(false); // Show loading overlay
                                                        if (data.type === "ingredients") {
                                                            // Add recipe cards to the chat
                                                            setMessages((prevMessages) => [
                                                                ...prevMessages,
                                                                {
                                                                    sender: "assistant",
                                                                    ingredients: data.best_matches, // Pass ingreds as part of the message
                                                                },
                                                            ]);
                                                        }
                                                        else if (data.type === "unavailable_message") {
                                                            // Display only the unavailable message text
                                                            setMessages((prevMessages) => [
                                                                ...prevMessages,
                                                                { sender: "assistant", text: data.unavailable_message },
                                                            ]);
                                                        }
                                                    } catch (error) {
                                                        console.error("Error sending recipe to backend:", error);
                                                        setMessages((prevMessages) => [
                                                            ...prevMessages,
                                                            {
                                                                sender: "assistant",
                                                                text: `Sorry, there was an issue saving your recipe. Error: ${error.message}`,
                                                            },
                                                        ]);
                                                    }
                                                }}
                                            >
                                                Select Recipe
                                            </button>
                                        </div>
                                    ))}
                                </div>
                            )}
                                {message.ingredients && (
                                    
                                    <div className="ingredients-list">
                                        <p>Here are the ingredients needed for {recipe}: </p>
                                        <table style={{ borderCollapse: "collapse", width: "100%", marginBottom: "10px" }}>
                                            <thead>
                                                <tr>
                                                    <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Ingredient</th>
                                                    <th style={{ border: "1px solid #ddd", padding: "8px", textAlign: "left" }}>Found in {shopName}:</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {Object.entries(message.ingredients).map(([ingredient, match], idx) => (
                                                    <tr key={idx}>
                                                        <td style={{ border: "1px solid #ddd", padding: "8px" }}>{ingredient}</td>
                                                        <td style={{ border: "1px solid #ddd", padding: "8px" }}>{match}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </table>
                                        <button className="review-ingredient-button" onClick={() => setShowCheckoutBox(true)}>
                                            <span className="text">Check Ingredients</span>
                                        </button>
                                    </div>
                                )}
                    </div>
                    {message.sender === "customer" && (
                        <img src={customerAvatar} alt="Customer Avatar" className="chat-logo-customer" />
                    )}
                </div>
                ))}
            </div>
            <div className="chat-input-container">
                <input style={{
                    backgroundColor: "#f4f4f4",
                    color: "black",
                }}
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === "Enter") {
                            handleTestSend(); // Trigger the Send button logic
                        }
                    }}
                    placeholder="Type your request, e.g., 'I want pasta with tomato sauce'"
                />
                <button className="send-button" onClick={handleTestSend}>
                {/*<button className="send-button" onClick={handleSend}>*/}
                    Send
                </button>
            </div>


            {/* Message Box for Confirmation */}
            {showCheckoutBox && (
                <div className="checkout-box">
                    <div className="checkout-box-content">
                        {/* Dish Name Heading */}
                        <h3>Review Ingredients</h3>
                        <p>For <u style={{color: "darkorange"}}>{recipe}</u></p>
                        <p>Recommended store: {shopName}</p>
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
                                <th style={{ border: "none", padding: "8px" }}>Image</th>
                                <th style={{ border: "none", padding: "8px" }}>Item</th>
                                <th style={{ border: "none", padding: "8px" }}>Suggested</th>
                                <th style={{ border: "none", padding: "8px" }}>Quantity</th>
                                <th style={{ border: "none", padding: "8px" }}>Price</th>
                                <th style={{ border: "none", padding: "8px" }}>Pick/Drop</th>
                            </tr>
                            </thead>
                            <tbody>
                            {ingredients.map((item, index) => (
                                <tr
                                    key={index}
                                    style={{
                                        backgroundColor: item.quantity > 0 ? "white" : "lightgray",
                                        color: item.quantity > 0 ? "black" : "white",
                                        border: "none",
                                    }}
                                >
                                    <td style={{ border: "none", padding: "8px" }}>
                                        <img
                                            src={item.imageUrl}
                                            alt={item.name}
                                            style={{
                                                width: "50px",
                                                height: "50px",
                                                objectFit: "cover",
                                                borderRadius: "5px",
                                            }}
                                        />
                                    </td>
                                    <td style={{ border: "none", padding: "8px" }}>{item.name}</td>
                                    <td style={{ border: "none", padding: "8px" }}>{item.recommended}</td>
                                    <td style={{ border: "none", padding: "8px" }}>
                                        <button
                                            className="addMinus"
                                            onClick={() => updateQuantity(index, -1)}
                                        >
                                            -
                                        </button>
                                        <span style={{ fontSize: "18px", margin: "0 5px 0 5px" }}>
            {item.quantity}
          </span>
                                        <button
                                            className="addMinus"
                                            onClick={() => updateQuantity(index, 1)}
                                        >
                                            +
                                        </button>
                                    </td>
                                    <td style={{ border: "none", padding: "8px" }}>
                                        ${item.price.toFixed(2)}
                                    </td>
                                    <td style={{ border: "none", padding: "8px" }}>
                                        <button className="dropButton" onClick={() => toggleSelect(index)}>
                                            {item.quantity > 0 ? "Drop" : "Pick"}
                                        </button>
                                    </td>
                                </tr>
                            ))}
                            </tbody>
                        </table>

                        {/* Price Summary */}
                        <div className="price-summary">
                            <strong>Total:</strong> ${ingredients
                            .filter((item) => item.selected && item.quantity > 0)
                            .reduce((total, item) => total + item.price * item.quantity, 0)
                            .toFixed(2)}
                        </div>
                        <button className="add-to-cart-button" onClick={handleAddToCart}>
                            Add to Cart
                        </button>
                        <button className="add-to-cart-button" onClick={()=>setShowCheckoutBox(false)}>
                            Cancel
                        </button>
                    </div>
                </div>
            )}
            {/* Loading Overlay */}
            {loading && (
                <div className="loading-overlay">
                    <div className="loading-content">Loading...</div>
                </div>
            )}
        </div>
    );
}

export default Chat;
