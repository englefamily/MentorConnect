import React, { useContext, useEffect, useState } from "react";
import SetLessonModal from "./modals/SetLessonModal.js";
import { fetch_api, transformData } from "../helpers/functions.js";
import context from "../Context.js";
import "./css/ShowLessons.css";

function ShowLessons() {
  const { userData } = useContext(context);

  const [showSetLessonModal, setShowSetLessonModal] = useState(false);
  const [students, setStudents] = useState([]);
  const [mentorData, setMentorData] = useState([]);
  const [topics, setTopics] = useState({});
  const [studySessions, setStudySessions] = useState([]);

  const getData = async () => {
    try {
      if (userData.type.includes("mentor")) {
        const SMresponse = await fetch_api(
          "students_mentor_chats",
          "GET",
          userData.user_id
        );
        const studentsData = SMresponse.data.students;
        const mentorData = SMresponse.data.mentor;
        console.log(
          "🚀 ~ file: SetLesson.js:29 ~ getData ~ mentor:",
          mentorData
        );
        console.log(
          "🚀 ~ file: SetLesson.js:13 ~ getStudents ~ student:",
          studentsData
        );

        const orderStudents = studentsData.map((student) => ({
          value: student.id,
          name: student.first_name + " " + student.last_name,
        }));
        console.log(
          "🚀 ~ file: SetLesson.js:28 ~ orderStudents ~ orderStudents:",
          orderStudents
        );
        setStudents(orderStudents);
        setTopics(transformData(mentorData.topics));
        setMentorData(mentorData);
      }

      const SSresponse = await fetch_api(
        "study_session",
        "GET",
        `user_id=${userData.user_id}&user_type=${
          userData.type.includes("mentor") ? "mentor" : "student"
        }`
      );
      const SSdata = SSresponse.data;
      console.log("🚀 ~ file: ShowLessons.js:44 ~ getData ~ SSdata:", SSdata);
      setStudySessions(SSdata);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    // fetch_api('study_session', 'GET', )
    getData();
  }, []);

  useEffect(() => {
    console.log(
      "🚀 ~ file: ShowLessons.js:53 ~ ShowLessons ~ students, mentorData, topics:",
      students,
      mentorData,
      topics
    );
  }, [students, mentorData, topics]);

  return (
    <div className="main-div">
      {userData?.type.includes("mentor") && (
        <>
          <SetLessonModal
            showModal={showSetLessonModal}
            setShowModal={setShowSetLessonModal}
            students={students}
            topics={topics}
            mentorData={mentorData}
          />
          <button onClick={() => setShowSetLessonModal(true)}>
            קביעת שיעור
          </button>
        </>
      )}
      <h2>שיעורים</h2>
      <div className="cards-container">
        {studySessions.length > 0 &&
          studySessions.map((study_session) => (
            <div className="ss-card" key={study_session.id}>
              <div className="first-column">
                <strong>השיעור התקיים בתאריך: </strong>{" "}
                {study_session.slot.date} <strong>בין השעות</strong>{" "}
                {study_session.slot.start_time} - {study_session.slot.end_time}
              </div>
              <div className="sec-column">
                <strong>השיעור יועבר </strong>
                {study_session.teach_method === "online" && "אונליין"}{" "}
                {study_session.teach_method === "at_mentor" && "בבית המורה"}{" "}
                {study_session.teach_method === "at_student" && "אצל התלמיד"}
                <strong>בנושא:</strong> {study_session.topic_name}{" "}
              </div>
              <div className="th-column">
                <strong>ההתלמיד:</strong> {study_session.student_name}{" "}
                <strong>המורה:</strong> {study_session.mentor_name}{" "}
              </div>

              <div className="fo-column">
                <strong>
                  {!(
                    userData.type.includes("mentor") &&
                    study_session.student_approved &&
                    study_session.date_passed
                  ) &&
                    !(
                      userData.type.includes("student") &&
                      !study_session.student_approved
                    ) &&
                    "סטטוס: "}
                </strong>
                <label>
                  {(userData.type.includes("mentor") &&
                    study_session.student_approved && !study_session.date_passed) &&
                    "התלמיד אישור את המפגש"}
                </label>
                <label>
                  {userData.type.includes("mentor") &&
                    !study_session.student_approved &&
                    "מחכה לאישור התלמיד"}
                </label>
                <label>
                  {(userData.type.includes("student") &&
                    study_session.student_approved && !study_session.session_happened) &&
                    "אישרת את המפגש"}
                </label>
                <label>
                  {userData.type.includes("student") &&
                    !study_session.student_approved && (
                      <button className="apr-bth">אשר</button>
                    )}
                </label>
                <label>
                  {(userData.type.includes("mentor") &&
                    study_session.student_approved &&
                    study_session.date_passed && !study_session.session_happened) && (
                      <button className="cml-bth">שיעור הושלם</button>
                    )}
                </label>
                <label>
                  {userData.type.includes("student") &&
                    study_session.student_approved &&
                    study_session.session_happened &&
                    "השיעור בוצע"}
                </label>
                <label>
                  {userData.type.includes("mentor") &&
                    study_session.student_approved &&
                    study_session.session_happened &&
                    "השיעור בוצע"}
                </label>
              </div>

              {/* <strong>Teach Method:</strong> {study_session.teach_method} */}

              {/* <strong>Session Happened:</strong>{" "}
                {study_session.session_happened ? "Yes" : "No"}
              
                <strong>Student Approved:</strong>{" "}
                {study_session.student_approved ? "Yes" : "No"}
              
                <strong>Topic:</strong> {study_session.topic}
              
                <strong>Student:</strong> {study_session.student}
              
                <strong>Hourly Rate:</strong> ${study_session.hourly_rate} */}
            </div>
          ))}
      </div>
    </div>
  );
}

export default ShowLessons;
