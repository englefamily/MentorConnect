import React, { useContext, useEffect, useState } from "react";
import logo from "../templates/test2.png";
import "./css/BaseNavbar.css";
import Login from "./modals/LoginModal";
import context from "../Context";
import { fetch_api } from "../helpers/functions";

function BaseNavbar() {
  const { setShowLoginModal, userData, logoutUser } = useContext(context);
  

  return (
    <>
      <nav className="main-nav">
        <ul className="nav-list">
          <li className="nav-item">
            <a href="/">
              <img src={logo} alt="Logo" className="nav-logo" />
            </a>
          </li>
          <li className="nav-item" style={{ cursor: "pointer" }}>
            <a onClick={() => setShowLoginModal(true)} className="nav-link">
              התחברות
            </a>
          </li>
          <li className="nav-item">
            <a href="/registerMentor" className="nav-link">
              הרשמה למורה
            </a>
          </li>
          <li className="nav-item">
            <a href="/registerStudent" className="nav-link">
              הרשמה לתלמיד
            </a>
          </li>
          <li className="nav-item">
            <a href="/mentors" className="nav-link">
              מורים
            </a>
          </li>
          <li className="nav-dropdown">
            <button class="dropbtn">{userData?.first_name ? userData.first_name : 'השם שלי'}</button>
            <div class="dropdown-content">
              <a href="#">החשבון שלי</a>
              <a onClick={logoutUser}>התנתק</a>
            </div>
          </li>
        </ul>
      </nav>
    </>
  );
}

export default BaseNavbar;
