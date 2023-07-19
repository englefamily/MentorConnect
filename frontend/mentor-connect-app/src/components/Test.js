import React, { useState, useEffect } from 'react';
import axios from 'axios';

const Test = () => {
  const [rooms, setRooms] = useState([1,2,3,4,5]);
  const [messages, setMessages] = useState({});
  const [messageInput, setMessageInput] = useState('');

  useEffect(() => {
    // Fetch the user's chat rooms
    axios.get('/api/chat/rooms/')
      .then(response => {
        setRooms(response.data);
        const roomIds = response.data.map(room => room.id);
        initializeWebSocketConnections(roomIds);
      })
      .catch(error => {
        console.error('Error retrieving chat rooms:', error);
      });
  }, []);

  const initializeWebSocketConnections = (roomIds) => {
    roomIds.forEach(roomId => {
      const socket = new WebSocket(`ws://localhost:8000/ws/chat/${roomId}/`);

      socket.onopen = () => {
        console.log(`WebSocket connection established for room ${roomId}.`);
      };

      socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        setMessages(prevMessages => ({
          ...prevMessages,
          [roomId]: [...(prevMessages[roomId] || []), message],
        }));
      };

      socket.onclose = () => {
        console.log(`WebSocket connection closed for room ${roomId}.`);
      };
    });
  };

  const sendMessage = (roomId) => {
    if (messageInput.trim() === '') {
      return;
    }

    const message = {
      message: messageInput,
    };

    axios.post(`/api/chat/${roomId}/`, message)
      .then(() => {
        setMessageInput('');
      })
      .catch((error) => {
        console.error('Error sending message:', error);
      });
  };

  return (
    <div>
      <div className="room-list">
        <h2>Chat Rooms</h2>
        {rooms.map((room) => (
          <div key={room.id}>
            <h3>{room.name}</h3>
            <div className="message-container">
              {messages[room.id] &&
                messages[room.id].map((message, index) => (
                  <div key={index}>
                    <strong>{message.username}: </strong>
                    {message.message} ({message.timestamp})
                  </div>
                ))}
            </div>
            <input
              type="text"
              value={messageInput}
              onChange={(e) => setMessageInput(e.target.value)}
            />
            <button onClick={() => sendMessage(room.id)}>Send</button>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Test;
