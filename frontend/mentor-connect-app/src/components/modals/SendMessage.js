import React, { useContext, useEffect, useState } from "react";
import "../css/SendMessage.css";
import context from "../../Context";

export default function SendMessage(props) {
  const [message, setMessage] = useState("היי מתעניין לגבי השיעור");
  const [error, setError] = useState("");
  const [showMessageModal, setShowMessageModal] = true
//   const { setShowLoginModal, loginUser } = useContext(context);

  useEffect(() => {
    document.body.classList.add("active-modal");
    return document.body.classList.remove("active-modal");
  });

  const toggleModal = () => {
    setShowMessageModal(false);
  };

  const handleAuth = async (event) => {
    // const loginResponse = await loginUser(email, password);
    // console.log(loginResponse);
    // if (loginResponse) {
    //   toggleModal();
    // } else {
    //   setError("אמייל או סיסמא אינם נכונים")
    // }
  };

  return (
    <div className="bg-modal">
      <div className="main-modal">
        <div className="modal-content">
          <i onClick={toggleModal}>X</i>
          <h2>שלח הודעה ל {props.mentor_name}</h2>
          <label htmlFor="message">מה תרצו לכתוב...</label>
          <input
            id="message"
            type="text"
            value={message}
            onChange={(event) => setMessage(event.target.value)}
          />

          {error && <span className="error">{error}</span>}
          <button className="submit-modal" onClick={handleAuth}>
            שלח
          </button>
          
        </div>
      </div>
    </div>
  );
}
