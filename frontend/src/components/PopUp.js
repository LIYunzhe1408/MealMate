import React, { useState } from "react";
import "./PopUp.css";

function PopUp({ onSubmit }) {
    const [pricePreference, setPricePreference] = useState(3); // Default budget preference: 3
    const [allergies, setAllergies] = useState("");

    const handleSubmit = (e) => {
        e.preventDefault();
        onSubmit({ pricePreference, allergies });
    };

    return (
        <div className="modal-overlay">
            <div className="modal">
                <h2>Set Your Preferences</h2>
                <form onSubmit={handleSubmit}>
                    <label>
                        <strong>Price Preference ($):</strong>
                        <p className="price-explanation">
                            1 = Least budget sensitive, 5 = Most budget sensitive
                        </p>
                        <div className="budget-options">
                            {[1, 2, 3, 4, 5].map((num) => (
                                <button
                                    key={num}
                                    type="button"
                                    className={`budget-button ${
                                        num === pricePreference ? "selected" : ""
                                    }`}
                                    onClick={() => setPricePreference(num)}
                                >
                                    {num}
                                </button>
                            ))}
                        </div>
                    </label>
                    <br />
                    <label>
                        <strong>Allergies:</strong>
                        <input
                            type="text"
                            value={allergies}
                            onChange={(e) => setAllergies(e.target.value)}
                            placeholder="Enter allergies (e.g., nuts, gluten)"
                            className="allergies-input" // Add a class for wider input
                        />
                    </label>
                    <br />
                    <button type="submit" className="submit-button">
                        Submit
                    </button>
                </form>
            </div>
        </div>
    );
}

export default PopUp;