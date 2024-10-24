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
