import React, { useContext, useEffect, useState } from "react";
import "../css/MessageModal.css";
import context from "../../Context";
import { fetch_api } from "../../helpers/functions";
import { useNavigate } from "react-router-dom";

export default function MessageModal(props) {
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const [showMessageModal, setShowMessageModal] = useState(true);
  const navigate = useNavigate();
  //   const { setShowLoginModal, loginUser } = useContext(context);

  useEffect(() => {
    document.body.classList.add("active-modal");
    return document.body.classList.remove("active-modal");
  });

  const toggleModal = () => {
    setError("");
    props.setShowModal(false);
  };

  const handleSend = async (event) => {
    if (!message) {
      setError("שדה נדרש");
      return;
    }
    const data = {
      chat: `${props.mentor_id}-${props.student_id}`,
      user: props.student_id,
      content: message,
    };
    const response = await fetch_api("message", "POST", data);
    console.log(
      "🚀 ~ file: MessageModal.js:30 ~ handleSend ~ response:",
      response
    );
    if (response?.status === 201) {
      navigate(`/dashboard/chat/${props.mentor_id}-${props.student_id}/`);
      return;
    }
    setError("יש בעיה זמנית בשליחת ההודעה נסו מאוחר יותר");
  };

  return (
    <>
      {props.showModal && (
        <div className="bg-modal">
          <div className="main-modal">
            <div className="modal-content">
              <i onClick={toggleModal}>X</i>
              <h2>שלח הודעה ל{props.message_to}</h2>
              <textarea
                placeholder="מה תרצו לכתוב..."
                rows={3}
                id="message"
                type="text"
                value={message}
                onChange={(event) => setMessage(event.target.value)}
              ></textarea>

              {error && <span className="error">{error}</span>}
              <button className="submit-modal" onClick={handleSend}>
                שלח
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
