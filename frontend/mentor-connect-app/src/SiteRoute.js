import React from "react";
import { Route, Routes } from "react-router-dom";
import Home from "./components/Home";
import RegisterForm from "./components/RegisterForm";
import RegisterMentor from "./components/RegisterMentor";
import RegisterStudent from "./components/RegisterStudent";
import ChatApp from "./components/DropDown";
import Login from "./components/modals/LoginModal";
import ShowMentors from "./components/ShowMentors";
import Dashboard from "./components/Dashboard";
import Test from "./components/Test";
import SendMessage from "./components/modals/MessageModal";

function SiteRoutes() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/registerMentor" element={<RegisterMentor />} />
        <Route path="/registerStudent" element={<RegisterStudent />} />
        <Route path="/mentors" element={<ShowMentors />} />
        <Route path="/login" element={<Login />} />
        <Route path="/dashboard/:page/:id_?" element={<Dashboard />} />
        <Route path="/test" element={<Test />} />
        <Route path="/modal" element={<SendMessage />} />
      </Routes>
    </>
  );
}

export default SiteRoutes;
