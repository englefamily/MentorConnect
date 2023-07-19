import React, { useContext, useEffect, useState } from "react";
import "./css/Chat.css";
import { fetch_api } from "../helpers/functions";
import context from "../Context";
const URL = "ws://127.0.0.1:8000/ws/2-5/";

const Chat = () => {
  const { userData } = useContext(context)
  console.log("🚀 ~ file: Chat.js:9 ~ Chat ~ UserData:", userData)
  const [newMessage, setNewMessage] = useState();
  const [messages, setMessages] = useState([]);
  const [ws, setWs] = useState(null);
  const getData = async () => {
    const response = await fetch_api('chat', 'GET', `?id=${userData.user_id}`)
    const chats = response.data.chats
    console.log("🚀 ~ file: Chat.js:15 ~ getData ~ chats:", chats)
  }

  useEffect(() => {
    // getData()
  }, [])


  useEffect(() => {
    const websocket = new WebSocket(URL);
    setWs(websocket);

    websocket.onopen = () => {
      console.log("connected");
    };

    websocket.onmessage = (evt) => {
      const message = JSON.parse(evt.data);
      console.log("🚀 ~ message:", message);
      addMessage(message);
      setNewMessage("");
    };

    websocket.onclose = () => {
      console.log("disconnected");
      setWs(new WebSocket(URL));
    };

    return () => {
      websocket.close();
    };
  }, []);

  const addMessage = (message) => {
    setMessages((prevMessages) => [message, ...prevMessages]);
  };

  const submitMessage = () => {
    const message = {
      email: userData.email,
      message: newMessage,
      chat_id: "2-5",
    };
    ws.send(JSON.stringify(message));
  };

  return (
    <div>
      <div className="main-root">
        <div className="main-chat">
          <div className="chat-top"></div>
          <div className="chat-center">
            {messages.reverse().map((message) => (
              <div className={message.email === userData.email ? 'message1' : 'message2'}>
                {message.message}
              </div>
              ))}
          </div>
          <div className="chat-bottom">
            <input value={newMessage} onChange={(e)=>setNewMessage(e.target.value)}/>
            <button onClick={submitMessage}></button>
          </div>
        </div>
        <div className="main-menu">
          {[1, 2, 3].map(() => (
            <div className="content-card">sdfsdfsdfsd</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Chat;
