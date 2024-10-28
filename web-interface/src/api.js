export const askAssistant = async (message) => {
  const response = await fetch("http://127.0.0.1:5000/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ message }), // 将用户输入发送给 Flask 后端
  });

  return await response.json();
};

export const fetchWordData = async (word) => {
  const response = await fetch("http://127.0.0.1:5000/vocabulary", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ word }), // Send the word to fetch definitions and examples
  });

  if (!response.ok) {
    throw new Error("Network response was not ok");
  }

  const data = await response.json();

  // Assuming the API returns an object with word details
  return {
    word: data.word,
    definition: data.definition,
    example: data.example || "No example available.", // Handle cases where there is no example
  };
};
