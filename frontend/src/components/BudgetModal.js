import React, { useState } from "react";

const BudgetModal = ({ setBudgetPreference }) => {
    const [budget, setBudget] = useState(3); // Default is 3 (moderate sensitivity)

    const handleSave = () => {
        setBudgetPreference(budget); // Pass budget to parent component
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
                        >
                            {num}
                        </button>
                    ))}
                </div>
                <button style={styles.saveButton} onClick={handleSave}>
                    Save Preference
                </button>
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
