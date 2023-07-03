import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import RegisterForm from "./components/RegisterForm";
import RegisterMentor from "./components/RegisterMentor";
import RegisterStudent from "./components/RegisterStudent";
import ChatApp from "./components/DropDown";
import Login from "./components/modals/LoginModal";

function SiteRoutes() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/registerMentor" element={<RegisterMentor />} />
        <Route path="/registerStudent" element={<RegisterStudent />} />
        <Route path="/login" element={<Login />} />
        <Route path="/test" element={<ChatApp />} />
      </Routes>
    </>
  );
}

export default SiteRoutes;
