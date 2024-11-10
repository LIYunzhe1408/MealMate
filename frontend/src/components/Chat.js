import React, { useState } from "react";
import "./Chat.css";
import assistantLogo from "../assets/trader-joes-logo.png"; // Adjust path to your assistant logo
import customerAvatar from "../assets/customer.jpg"; // Adjust path to your customer avatar

function Chat() {
    const [messages, setMessages] = useState([
        { sender: "assistant", text: "Hello! I'm your virtual assistant. How can I help you today?" }
    ]);
    const [inputValue, setInputValue] = useState("");

    const handleSend = () => {
        if (inputValue.trim() !== "") {
            // Add customer message
            setMessages([...messages, { sender: "customer", text: inputValue }]);
            setInputValue("");

            // Add a response from the assistant (optional: replace with actual logic or AI response)
            setTimeout(() => {
                setMessages(prevMessages => [
                    ...prevMessages,
                    { sender: "assistant", text: "Thank you for reaching out! How can I assist you further?" }
                ]);
            }, 1000);
        }
    };

    return (
        <div className="chat">
            <h2>Chat with us</h2>
            <div className="chat-messages">
                {messages.map((message, index) => (
                    <div key={index} className="chat-message-container" style={{ display: "flex" }}>
                        {message.sender === "assistant" && (
                            <img src={assistantLogo} alt="Assistant Logo" className="chat-logo" />
                        )}
                        <div
                            className={`chat-bubble ${message.sender === "customer" ? "customer-bubble" : ""}`}
                        >
                            <div className="chat-message">{message.text}</div>
                        </div>
                        {message.sender === "customer" && (
                            <img src={customerAvatar} alt="Customer Avatar" className="chat-logo-customer" />
                        )}
                    </div>
                ))}
            </div>
            <input
                type="text"
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                placeholder="Ask a question or type a keyword"
            />
            <button className="send-button" onClick={handleSend}>Send</button>
        </div>
    );
}

export default Chat;
