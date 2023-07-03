import React, { useContext, useEffect, useState } from "react";
import "../css/LoginModal.css";
import context from "../../Context";

export default function LoginModal() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { setShowLoginModal, loginUser } = useContext(context);

  useEffect(() => {
    document.body.classList.add("active-modal");
    return document.body.classList.remove("active-modal");
  });

  const toggleModal = () => {
    setShowLoginModal(false);
  };

  const handleAuth = async (event) => {
    const loginResponse = await loginUser(email, password);
    console.log(loginResponse);
    if (loginResponse?.error) {
      setError("אמייל או סיסמא אינם נכונים");
    } else {
      toggleModal();
    }
  };

  return (
    <div className="bg-modal">
      <div className="main-modal">
        <div className="modal-content">
          <i onClick={toggleModal}>X</i>
          <h2>כניסה</h2>
          <label htmlFor="email">הכנס אמייל</label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
          />
          <label htmlFor="password">הכנס סיסמא</label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
          />
          {error && <span className="error">{error}</span>}
          <button className="submit-modal" onClick={handleAuth}>
            התחבר
          </button>
        </div>
      </div>
    </div>
  );
}
