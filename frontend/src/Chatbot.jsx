import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

function Chatbot() {
  const [messages, setMessages] = useState([]); // {sender, text}
  const [inputText, setInputText] = useState("");
  const chatboxRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (chatboxRef.current) {
      chatboxRef.current.scrollTop = chatboxRef.current.scrollHeight;
    }
  }, [messages]);

  const handleSend = async () => {
    if (!inputText.trim()) return;

    const textToSend = inputText;
    const userMessage = { sender: "user", text: textToSend };
    setMessages((prev) => [...prev, userMessage]);
    setInputText("");

    try {
      const res = await axios.post("http://127.0.0.1:5000/get_response", {
        message: textToSend,
      });

      const botReply = res.data.reply || "Sorry, no reply.";
      const botMessage = { sender: "bot", text: botReply };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errMsg = { sender: "bot", text: "Error connecting to server." };
      setMessages((prev) => [...prev, errMsg]);
    }
  };

  const renderMessageContent = (msg) => {
    const text = msg.text || "";
    const fallbackMarker = "Please submit a request/complaint";
    if (msg.sender === "bot" && text.includes(fallbackMarker)) {
      const before = text.split(fallbackMarker)[0];
      return (
        <span>
          {before}
          <span className="complaint-link" onClick={() => navigate("/complaint")}>
            Submit a request/complaint here
          </span>
          .
        </span>
      );
    }
    return <span>{text}</span>;
  };

  return (
    <div>
      <h2 className="text-center mt-3" style={{ color: "#fff" }}>Customer Service Chatbot</h2>

      <div id="chat-container" className="container mt-4">
        <div id="chatbox" className="chat-box" ref={chatboxRef}>
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.sender}`}>
              {renderMessageContent(msg)}
            </div>
          ))}
        </div>

        <div className="input-area text-center mt-3" style={{ display: "flex" }}>
          <input
            id="userInput"
            type="text"
            placeholder="Type your message here..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <button className="btn btn-secondary" onClick={handleSend}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default Chatbot;
