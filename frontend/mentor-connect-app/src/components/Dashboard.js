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
  const [component, setComponent] = useState(page);
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
          onClick={() => window.location.href = "edit_profile"}
          style={
            component === "edit_profile" ? { backgroundColor: "#00FFCA" } : {}
          }
        >
          עריכת פרופיל
        </p>
        <p
          onClick={() => window.location.href = "chat"}
          style={component === "chat" ? { backgroundColor: "#00FFCA" } : {}}
        >
          צ'אט
        </p>
        <p
          onClick={() => window.location.href = "set_lesson"}
          style={
            component === "set_lesson" ? { backgroundColor: "#00FFCA" } : {}
          }
        >
          קביעת שיעור
        </p>
      </div>
      <div className="data-container">
        {component === "edit_profile" && <EditProfile type={profile} />}
        {component === "chat" && <Chat type={profile} chat_id={id_ ? id_ : null}/>}
        {component === "set_lesson" && <SetLesson />}
      </div>
    </div>
  );
}

export default Dashboard;
