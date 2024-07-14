import React, { useState } from 'react';

const Chatbot = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');

  const handleSendMessage = () => {
    fetch('/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message: input })
    })
    .then(response => response.json())
    .then(data => {
      const botResponse = data.response;
      setMessages([...messages, { text: input, type: 'user' }]);
      setMessages([...messages, { text: botResponse, type: 'bot' }]);
      setInput('');
    })
    .catch(error => {
      console.error('Error:', error);
    });
  };

  return (
    <div>
      <ul>
        {messages.map((message, index) => (
          <li key={index} className={message.type === 'user' ? 'user-message' : 'bot-message'}>
            {message.text}
          </li>
        ))}
      </ul>
      <input
        type="text"
        value={input}
        onChange={(event) => setInput(event.target.value)}
        placeholder="Type your message..."
      />
      <button onClick={handleSendMessage}>Send</button>
    </div>
  );
};

export default Chatbot;