import React, { useContext, useEffect, useState } from "react";
import "./css/Dashboard.css";
import EditProfile from "./edit_profile";
import Chat from "./Chat";
import SetLesson from "./SetLesson";
import { useNavigate, useParams } from "react-router-dom";
import context from "../Context";
import DropDown from "./DropDown";

function Dashboard() {
  const { authTokens, userData } = useContext(context);
  const { page, id_ } = useParams();
  const [profile, setProfile] = useState(
    userData?.type.includes("mentor") ? "mentor" : "student"
  );
  const navigate = useNavigate();

  useEffect(() => {
    if (!authTokens?.access) {
      navigate("/");
    }
  }, []);

  return (
    <div className="main-dash">
      <div className="main-dash-nav">
        {userData?.type && userData.type.length === 2 && (
          <div className="user-types">
            {
              <span
                onClick={() => setProfile("student")}
                style={
                  profile === "student" ? { textDecoration: "underline" } : {}
                }
              >
                תלמיד
              </span>
            }
            |
            <span
              onClick={() => setProfile("mentor")}
              style={
                profile === "mentor" ? { textDecoration: "underline" } : {}
              }
            >
              מורה
            </span>
          </div>
        )}

        <p
          onClick={() => navigate("/dashboard/edit_profile/")}
          style={
            page === "edit_profile" ? { backgroundColor: "#00FFCA" } : {}
          }
        >
          עריכת פרופיל
        </p>
        <p
          onClick={() => navigate("/dashboard/chat/")}
          style={page === "chat" ? { backgroundColor: "#00FFCA" } : {}}
        >
          צ'אט
        </p>
        <p
          onClick={() => navigate("/dashboard/set_lesson/")}
          style={
            page === "set_lesson" ? { backgroundColor: "#00FFCA" } : {}
          }
        >
          קביעת שיעור
        </p>
      </div>
      <div className="data-container">
        {page === "edit_profile" && <EditProfile type={profile} />}
        {page === "chat" && <Chat type={profile} chat_id={id_ ? id_ : null}/>}
        {page === "set_lesson" && <SetLesson />}
      </div>
    </div>
  );
}

export default Dashboard;
