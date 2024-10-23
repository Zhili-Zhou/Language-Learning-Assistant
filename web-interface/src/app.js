import React, { useState } from "react";
import axios from "axios";

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
      <form onSubmit={handleSubmit}>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask something..."
          rows="4"
          cols="50"
        />
        <br />
        <button type="submit">Submit</button>
      </form>
      <div>
        <h2>Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}

export default App;
