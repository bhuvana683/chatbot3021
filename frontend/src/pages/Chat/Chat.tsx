/* frontend/src/pages/Chat/Chat.tsx */

import { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState<{ role: string; content: string }[]>([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const projectId = localStorage.getItem("selectedProjectId");

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || !projectId) return;

    const userMessage = { role: "user", content: input };
    setMessages([...messages, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const token = localStorage.getItem("token");

      // Send request to backend
      const response = await fetch("http://127.0.0.1:8000/chat/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          message: userMessage.content,
          project_id: Number(projectId), // convert string to int
        }),
      });

      const data = await response.json();

      if (response.ok) {
        // Add bot response to messages
        setMessages((prev) => [...prev, { role: "bot", content: data.response }]);
      } else {
        alert(data.detail || data.message || "Failed to get response");
      }
    } catch (err) {
      console.error(err);
      alert("Error connecting to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <div className="messages">
        {messages.map((msg, idx) => (
          <div key={idx} className={msg.role === "user" ? "user-msg" : "bot-msg"}>
            {msg.content}
          </div>
        ))}
      </div>
      <form onSubmit={handleSend} className="chat-input">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a message..."
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? "Sending..." : "Send"}
        </button>
      </form>
    </div>
  );
}
