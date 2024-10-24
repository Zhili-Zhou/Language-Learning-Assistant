import React, { useState } from "react";
import { askAssistant } from "../api";

const AssistantWithMemory = () => {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState([]);

  const handleAskAssistant = async () => {
    const res = await askAssistant(message);
    setConversation([
      ...conversation,
      { role: "user", content: message },
      { role: "assistant", content: res.answer },
    ]);
    setMessage("");
  };

  const handleReset = async () => {
    await fetch("http://127.0.0.1:5000/reset", {
      method: "POST",
    });
    setConversation([]);
  };

  return (
    <div>
      <h2>Assistant with Memory</h2>

      <div>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          placeholder="Ask something..."
        />
        <button onClick={handleAskAssistant}>Ask</button>
        <button onClick={handleReset}>Reset Conversation</button>
      </div>

      <div>
        <h3>Conversation History</h3>
        {conversation.map((entry, index) => (
          <p key={index}>
            <strong>{entry.role === "user" ? "You" : "Assistant"}:</strong>{" "}
            {entry.content}
          </p>
        ))}
      </div>
    </div>
  );
};

export default AssistantWithMemory;
