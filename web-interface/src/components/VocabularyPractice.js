import React, { useState } from "react";
import { fetchWordData } from "../api"; // Assume this API function is defined to fetch data

const VocabularyPractice = () => {
    const [word, setWord] = useState("");
    const [wordData, setWordData] = useState(null);
    const [error, setError] = useState("");

    const handleFetchWordData = async () => {
        try {
            const res = await fetchWordData(word);
            setWordData(res);
            setError("");
        } catch (err) {
            setError("Error fetching word data. Please try again.");
            setWordData(null);
        }
    };

    return (
        <div>
            <h2>Vocabulary Practice</h2>
            <input
                type="text"
                value={word}
                onChange={(e) => setWord(e.target.value)}
                placeholder="Enter a word..."
            />
            <button onClick={handleFetchWordData}>Get Definition</button>

            {error && <p style={{ color: "red" }}>{error}</p>}

            {wordData && (
                <div>
                    <h3>Word: {wordData.word}</h3>
                    <p><strong>Definition:</strong> {wordData.definition}</p>
                    <p><strong>Example Sentence:</strong> {wordData.example}</p>
                </div>
            )}
        </div>
    );
};

export default VocabularyPractice;
