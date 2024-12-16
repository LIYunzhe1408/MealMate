import React, { useState } from "react";

const BudgetModal = ({ setBudgetPreference }) => {
    const [budget, setBudget] = useState(3); // Default is 3 (moderate sensitivity)
    const [isSaving, setIsSaving] = useState(false); // Track saving state
    const [error, setError] = useState(null); // Handle errors

    const handleSave = async () => {
        setIsSaving(true);
        setError(null);

        try {
            const response = await fetch("http://127.0.0.1:5000/api/set-budget", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ budgetPreference: budget }),
            });

            if (!response.ok) {
                throw new Error(`Failed to save budget preference. Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("Budget Preference Saved:", data); // Debugging log
            setBudgetPreference(budget); // Pass budget to parent component
        } catch (err) {
            console.error("Error saving budget preference:", err);
            setError("Failed to save budget preference. Please try again.");
        } finally {
            setIsSaving(false); // Reset saving state
        }
    };

    return (
        <div style={styles.modalOverlay}>
            <div style={styles.modal}>
                <h2>Set Your Budget Sensitivity</h2>
                <p>Choose a number from 1 (no price sensitivity) to 5 (high price sensitivity):</p>
                <div style={styles.options}>
                    {[1, 2, 3, 4, 5].map((num) => (
                        <button
                            key={num}
                            style={{
                                ...styles.optionButton,
                                backgroundColor: num === budget ? "#007bff" : "#f4f4f4",
                                color: num === budget ? "white" : "black",
                            }}
                            onClick={() => setBudget(num)}
                            disabled={isSaving} // Disable while saving
                        >
                            {num}
                        </button>
                    ))}
                </div>
                <button
                    style={{
                        ...styles.saveButton,
                        opacity: isSaving ? 0.6 : 1,
                        cursor: isSaving ? "not-allowed" : "pointer",
                    }}
                    onClick={handleSave}
                    disabled={isSaving}
                >
                    {isSaving ? "Saving..." : "Save Preference"}
                </button>
                {error && <p style={{ color: "red" }}>{error}</p>}
            </div>
        </div>
    );
};

const styles = {
    modalOverlay: {
        position: "fixed",
        top: 0,
        left: 0,
        width: "100%",
        height: "100%",
        backgroundColor: "rgba(0, 0, 0, 0.5)",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        zIndex: 1000,
    },
    modal: {
        backgroundColor: "white",
        padding: "20px",
        borderRadius: "8px",
        textAlign: "center",
        width: "300px",
    },
    options: {
        display: "flex",
        justifyContent: "space-around",
        margin: "20px 0",
    },
    optionButton: {
        padding: "10px 15px",
        border: "1px solid #ddd",
        borderRadius: "5px",
        cursor: "pointer",
    },
    saveButton: {
        padding: "10px 20px",
        backgroundColor: "#007bff",
        color: "white",
        border: "none",
        borderRadius: "5px",
        cursor: "pointer",
    },
};

export default BudgetModal;
