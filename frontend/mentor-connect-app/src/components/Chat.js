import React, { useContext, useEffect, useRef, useState } from "react";
import "./css/Chat.css";
import { fetch_api } from "../helpers/functions";
import context from "../Context";
import { WS_HOST_URL } from "../helpers/avariables";
import { useStateManager } from "react-select";

const Chat = (props) => {
  const { userData } = useContext(context);
  console.log("🚀 ~ file: Chat.js:9 ~ Chat ~ UserData:", userData);
  const [newMessage, setNewMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [ws, setWs] = useState({});
  const [chats, setChats] = useState([]);
  const [selectedChat, setSelectedChat] = useState(null);
  const [chatLoaded, setChatLoaded] = useState(false);
  const scrollContainerRef = useRef(null);
  const chat_id = props.chat_id;

  const getData = async () => {
    const response = await fetch_api("get-chats", "GET", userData?.user_id);
    console.log("🚀 ~ file: Chat.js:19 ~ getData ~ response:", response);
    const chats = response.data.chats;
    console.log("🚀 ~ file: Chat.js:20 ~ getData ~ chats:", chats);
    return chats;
  };

  useEffect(() => {
    getData().then((chats) => {
      setChats(chats);
      initializeWebSocketConnections(chats);
    });
  }, []);

  useEffect(() => {
    console.log("🚀 ~ file: Chat.js:34 ~ Chat ~ messages:", messages);
    handleScrollDown()
  }, [messages]);

  useEffect(() => {
    if (chat_id && chats.length && !chatLoaded) {
      chats.forEach((chat) => {
        if (chat_id === chat?.id) {
          setSelectedChat(chat);
        }
      });
    }
    if (chats.length) {
      setChatLoaded(true);
    }
  }, [chats]);

  useEffect(() => {
    handleScrollDown()
  }, [selectedChat])

  const initializeWebSocketConnections = (chats) => {
    chats.forEach(async (chat) => {
      const response = await fetch_api("get-messages", "GET", chat.id);
      setMessages((prevMessages) => ({
        ...prevMessages,
        [chat.id]: response.data.messages,
      }));
      const socket = new WebSocket(`${WS_HOST_URL}ws/${chat.id}/`);
      setWs((prevWs) => ({
        ...prevWs,
        [chat.id]: socket,
      }));
      socket.onopen = () => {
        console.log(`WebSocket connection established for room ${chat.id}.`);
      };

      socket.onmessage = (event) => {
        const message = JSON.parse(event.data);
        console.log(
          "🚀 ~ file: Chat.js:44 ~ chats.forEach ~ message:",
          message
        );
        setMessages((prevMessages) => ({
          ...prevMessages,
          [chat?.id]: [...(prevMessages[chat?.id] || []), message],
        }));

        setChats((prevChats) => {
          return [
            chat,
            ...prevChats.filter((Pchat) => {
              return Pchat !== chat;
            }),
          ];
        });
      };

      socket.onclose = () => {
        console.log(`WebSocket connection closed for room ${chat?.id}.`);
      };
    });
  };

  const handleScrollDown = () => {
    const scrollContainer = scrollContainerRef.current;
    if (scrollContainer) {
      scrollContainer.scrollTop = scrollContainer.scrollHeight;
    }
  };

  const submitMessage = () => {
    if (newMessage.trim() !== "") {
      const message = {
        email: userData.email,
        message: newMessage,
        chat_id: selectedChat?.id,
      };
      console.log("🚀 ~ file: Chat.js:99 ~ submitMessage ~ message:", message);

      ws[selectedChat?.id].send(JSON.stringify(message));
      setNewMessage("");
    }
  };

  return (
    <div>
      <div className="main-root">
        <div className="main-chat">
          <div className="chat-top">
            {selectedChat && (
              <h6>
                {selectedChat?.mentor?.user_id === userData?.user_id
                  ? `${selectedChat.student.first_name} ${selectedChat.student.last_name}`
                  : `${selectedChat?.mentor.first_name} ${selectedChat?.mentor.last_name}`}
              </h6>
            )}
          </div>
          <div className="chat-center" id="chatCenter" ref={scrollContainerRef}>
            {selectedChat &&
              messages[selectedChat?.id] &&
              messages[selectedChat?.id].map((message, index) => (
                <div
                  key={index}
                  className={
                    message.email === userData.email ? "message1" : "message2"
                  }
                >
                  {message.message}
                </div>
              ))}
          </div>
          {selectedChat && (
            <div className="chat-bottom">
              <input
                value={newMessage}
                onChange={(e) => setNewMessage(e.target.value)}
                onKeyDown={(e) => {
                  e.key === "Enter" && submitMessage();
                }}
              />
              <button onClick={submitMessage}></button>
            </div>
          )}
        </div>
        <div className="main-menu">
          <div className="content-card"></div>
          {chats.length ? (
            chats.map((chat, index) => (
              <div
                key={index}
                className="content-card"
                style={
                  selectedChat?.id === chat?.id
                    ? { backgroundColor: "#C9C9C9" }
                    : {}
                }
                onClick={() => setSelectedChat(chat)}
              >
                <div className="img-container">
                  <img src="https://static.lessoons.co.il/assets/users/profileImages/33035/xl1617525321.jpg.pagespeed.ic.ssdASHvNlu.webp" />
                </div>
                <div className="name-last-container">
                  <h6>
                    {chat?.mentor?.user_id === userData?.user_id
                      ? `${chat.student.first_name} ${chat.student.last_name}`
                      : `${chat?.mentor.first_name} ${chat?.mentor.last_name}`}
                  </h6>
                  <p>
                    {messages[chat?.id] && messages[chat?.id].length > 0
                      ? messages[chat?.id][messages[chat?.id].length - 1].message
                          .length > 10
                        ? messages[chat?.id][
                            messages[chat?.id].length - 1
                          ].message.slice(0, 10) + "..."
                        : messages[chat?.id][messages[chat?.id].length - 1]
                            .message
                      : ""}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <h3>עדיין אין צאטים</h3>
          )}
        </div>
      </div>
      {/* <button onClick={handleClick}>Scroll down</button> */}
    </div>
  );
};

export default Chat;
