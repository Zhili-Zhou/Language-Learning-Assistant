import React, { useState } from "react";
import axios from "axios";
import AssistantWithMemory from "./components/AssistantWithMemory";

function App() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${process.env.REACT_APP_BACKEND_URL}/ask`, {
        message: input,
      });
      setResponse(res.data.answer);
    } catch (err) {
      console.error(err);
      setResponse("Error communicating with the assistant");
    }
  };

  return (
    <div className="App">
      <h1>Language Learning Assistant</h1>
      <AssistantWithMemory />
      <VocabularyPractice />
    </div>
  );
}

export default App;
