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
      const SMresponse = await fetch_api(
        "students_mentor_chats",
        "GET",
        userData.user_id
      );
      const studentsData = SMresponse.data.students;
      const mentorData = SMresponse.data.mentor;
      console.log("🚀 ~ file: SetLesson.js:29 ~ getData ~ mentor:", mentorData);
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

      const SSresponse = await fetch_api(
        "study_session",
        "GET",
        `mentor_id=${mentorData.id}`
      );
      const SSdata = SSresponse.data;
      setStudySessions(SSdata);
      console.log("🚀 ~ file: ShowLessons.js:44 ~ getData ~ SSdata:", SSdata);
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
      <SetLessonModal
        showModal={showSetLessonModal}
        setShowModal={setShowSetLessonModal}
        students={students}
        topics={topics}
        mentorData={mentorData}
      />
      <button onClick={() => setShowSetLessonModal(true)}>קביעת שיעור</button>
      <h2>שיעורים</h2>
      <div className="cards-container">
        {studySessions.length > 0 &&
          studySessions.map((study_session) => (
            <div className="ss-card" key={study_session.id}>

                <strong>השיעור התקיים בתאריך: </strong> {study_session.slot.date}
                {' '}
                <strong>בין השעות</strong> {study_session.slot.start_time} -{" "}
                {study_session.slot.end_time}
              
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
