import React, { useState } from "react";
import "./Chat.css";
import assistantLogo from "../assets/trader-joes-logo.png";
import customerAvatar from "../assets/customer.jpg";

function Chat({ setCart }) {
    const [messages, setMessages] = useState([
        { sender: "assistant", text: "Hello! I'm your virtual assistant. How can I help you today?" },
    ]);
    const [inputValue, setInputValue] = useState("");
    const [showCheckoutBox, setShowCheckoutBox] = useState(false);

    // Ingredients with recommended and current quantities
    const [ingredients, setIngredients] = useState([]);
    const [recipeSuggestions, setRecipeSuggestions] = useState([]);

    const predefinedIngredients = [
        {
            name: "Pasta",
            price: 2.5,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "200g",
            imageUrl: "/images/pasta/pasta.png"
        },
        {
            name: "Olive oil",
            price: 1.2,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "2 tbsp",
            imageUrl: "/images/pasta/Olive Oil.png"
        },
        {
            name: "Garlic",
            price: 0.5,
            recommended: 3,
            quantity: 3,
            selected: true,
            unit: "2-3 cloves",
            imageUrl: "/images/pasta/garlic.png"
        },
        {
            name: "Small onion",
            price: 0.8,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "1",
            imageUrl: "/images/pasta/onion.png"
        },
        {
            name: "Canned tomatoes",
            price: 1.5,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "400g",
            imageUrl: "/images/pasta/canned tomato.png"
        },
        {
            name: "Sugar",
            price: 0.2,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "1 tsp",
            imageUrl: "/images/pasta/sugar.png"
        },
        {
            name: "Salt and pepper",
            price: 0.3,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "",
            imageUrl: "/images/pasta/saltandpepper.png"
        },
        {
            name: "Fresh basil leaves",
            price: 0.7,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "",
            imageUrl: "/images/pasta/leaves.png"
        },
        {
            name: "Grated Parmesan cheese",
            price: 1.0,
            recommended: 1,
            quantity: 1,
            selected: true,
            unit: "",
            imageUrl: "/images/pasta/cheese.png"
        },
    ];

    // const handleSend = () => {
    //     if (inputValue.trim() !== "") {
    //         setMessages([...messages, { sender: "customer", text: inputValue }]);
    //
    //         // Check if user requests a pasta recipe
    //         if (inputValue.toLowerCase().includes("pasta with tomato sauce")) {
    //             setIngredients(predefinedIngredients);
    //             setShowCheckoutBox(true); // Show the message box for confirmation
    //             setMessages((prevMessages) => [
    //                 ...prevMessages,
    //                 { sender: "assistant", text: "Please confirm the items in the message box." },
    //             ]);
    //             // // Combine ingredients into one message
    //             // const ingredientList = predefinedIngredients
    //             //     .map((item) =>
    //             //         `${item.name}${item.unit ? ` - ${item.unit}` : ""} - $${item.price.toFixed(2)}`
    //             //     )
    //             //     .join("\n");
    //             //
    //             // setMessages((prevMessages) => [
    //             //     ...prevMessages,
    //             //     {
    //             //         sender: "assistant",
    //             //         text: `Here is your recipe and the ingredients:\n\n${ingredientList}`,
    //             //     },
    //             // ]);
    //         } else if (inputValue.toLowerCase() === "add to cart") {
    //             setShowCheckoutBox(true); // Show the message box for confirmation
    //             setMessages((prevMessages) => [
    //                 ...prevMessages,
    //                 { sender: "assistant", text: "Please confirm the items in the message box." },
    //             ]);
    //         } else {
    //             setMessages((prevMessages) => [
    //                 ...prevMessages,
    //                 { sender: "assistant", text: "How can I assist you further?" },
    //             ]);
    //         }
    //         setInputValue("");
    //     }
    // };

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

            try {
                const response = await fetch('http://127.0.0.1:5000/api/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ message: inputValue }),
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
            }

            setInputValue(""); // Clear input field
        }
    };

    return (
        <div className="chat">
            <h2>Chat with us</h2>
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div key={index} className="chat-message-container">
                        {message.sender === "assistant" && (
                            <img src={assistantLogo} alt="Assistant Logo" className="chat-logo" />
                        )}
                        <div
                            className={`chat-bubble ${message.sender === "customer" ? "customer-bubble" : ""}`}
                        >
                            {message.text &&
                                message.text} {/* Display regular text messages */}
                            {message.recipes && (
                                <div className="recipe-cards">
                                    {message.recipes.map((recipe, idx) => (
                                        <div key={idx} className="recipe-card">
                                            <h4>{recipe.title}</h4>
                                            <p><strong>Ingredients:</strong> {recipe.ingredients}</p>
                                            <button
                                                className="select-recipe-button"
                                                onClick={() => console.log(`Selected Recipe: ${recipe.title}`)}
                                            >
                                                Select Recipe
                                            </button>
                                        </div>
                                    ))}
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
                <input
                    type="text"
                    value={inputValue}
                    onChange={(e) => setInputValue(e.target.value)}
                    placeholder="Type your request, e.g., 'I want a pasta with tomato sauce'"
                />
                <button className="send-button" onClick={handleTestSend}>
                    Send
                </button>
            </div>
        </div>
    );
}

export default Chat;
