import React, { useContext, useCallback, useState, useEffect } from "react";
import context from "../Context";
import axios from "axios";
import { fetch_api, transformData } from "../helpers/functions";
import DropDown from "./DropDown";
import "./css/SetLesson.css";

function SetLesson() {
  const { userData } = useContext(context);
  const [errors, setErrors] = useState([]);
  const [students, setStudents] = useState([]);
  const [mentorData, setMentorData] = useState([]);
  const [selectedStudent, setSelectedStudent] = useState([]);
  const [hourChoices, setHourChoices] = useState([]);
  const [topics, setTopics] = useState({});
  const [selectedTopic, setSelectedTopic] = useState([]);
  const [studySession, setStudySession] = useState({
    teach_method: "",
    topic: [],
    slot: {
      date: "",
      start_time: "",
      end_time: "",
      mentor: userData?.mentor_id,
    },
    student: [],
  });

  useEffect(() => {
    console.log(
      "🚀 ~ file: SetLesson.js:34 ~ SetLesson ~ studySession:",
      studySession
    );
  }, [studySession]);

  const getData = async () => {
    try {
      const response = await fetch_api(
        "students_mentor_chats",
        "GET",
        userData.user_id
      );
      const students = response.data.students;
      const mentor = response.data.mentor;
      console.log("🚀 ~ file: SetLesson.js:29 ~ getData ~ mentor:", mentor);
      console.log(
        "🚀 ~ file: SetLesson.js:13 ~ getStudents ~ student:",
        students
      );

      const orderStudents = students.map((student) => ({
        value: student.id,
        name: student.first_name + " " + student.last_name,
      }));
      console.log(
        "🚀 ~ file: SetLesson.js:28 ~ orderStudents ~ orderStudents:",
        orderStudents
      );
      setStudents(orderStudents);
      setTopics(transformData(mentor.topics));
      setMentorData(mentor);
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    const HOUR_CHOICES = [];
    const minutes = [0, 15, 30, 45]; // Replace this array with the desired minute values

    for (let x = 0; x < 24; x++) {
      for (let m of minutes) {
        const timeString = `${x}:${m.toString().padStart(2, "0")}`;
        const timeObj = new Date(`2000-01-01T${timeString}`);
        HOUR_CHOICES.push({ time: timeObj, display: timeString });
      }
    }
    setHourChoices(HOUR_CHOICES);
    getData();
  }, []);

  const handleSelect = (event) => {
    const value = parseInt(event.target.value);
    if (selectedStudent.includes(value)) {
      setSelectedStudent([]);
    } else {
      setSelectedStudent([value]);
    }
  };

  const handleSelectTopic = (event) => {
    const value = parseInt(event.target.value);
    if (selectedTopic.includes(value)) {
      setSelectedTopic([]);
    } else {
      setSelectedTopic([value]);
    }
  };

  const handleChange = (event) => {
    let { name, value } = event.target;
    console.log(
      "🚀 ~ file: SetLesson.js:96 ~ handleChange ~ name, value:",
      name,
      value
    );
    if (name.startsWith("slot.")) {
      setStudySession((prev) => ({
        ...prev,
        slot: {
          ...prev.slot,
          [name.substring(5)]: value,
        },
      }));
    } else if (name === "topic" || name === "student") {
      value = parseInt(value);
      if (
        (name === "topic" && studySession.topic.includes(value)) ||
        (name === "student" && studySession.student.includes(value))
      ) {
        setStudySession((prev) => ({
          ...prev,
          [name]: [],
        }));
      } else {
        setStudySession((prev) => ({
          ...prev,
          [name]: [value],
        }));
      }
    } else {
      setStudySession((prev) => ({
        ...prev,
        [name]: value,
      }));
    }
  };

  const validateData = () => {
    let updatedErrors = [];

    Object.entries(studySession).forEach(([name, value]) => {
      if (name === "slot") {
        Object.entries(value).forEach(([name, value]) => {
          if (!value) {
            if (name === "date") {
              updatedErrors.push(`תאריך המפגש לא הוגדר`);
            } else if (name === "start_time") {
              updatedErrors.push(`שעת תחילת המפגש לא הוגדרה`);
            } else if (name === "end_time") {
              updatedErrors.push(`שעת סיום המפגש לא הוגדרה`);
            } else if (name === "mentor") {
              updatedErrors.push(`בעיה במערכת, נסה להתנתק ולהתחבר שוב`);
            }
          }
        });
      } else {
        if (!value || (typeof value === "object" && value.length === 0)) {
          if (name === "teach_method") {
            updatedErrors.push(`בחר באחד מדרכי הלימוד`);
          } else if (name === "student") {
            updatedErrors.push("בחר תלמיד");
          } else if (name === "topic") {
            updatedErrors.push(`בחר את נושא הלימוד`);
          }
        }
      }
    });
    console.log(
      "🚀 ~ file: SetLesson.js:171 ~ validateData ~ updatedErrors:",
      updatedErrors
    );

    setErrors(updatedErrors);
    return updatedErrors.length;
  };

  const handleSubmit = () => {
    const errors = validateData();
    if (errors > 0) {
      return;
    }
    const data = { ...studySession };
    const transformTime = (inputString) => {
      const [hours, minutes] = inputString.split(":");

      const paddedHours = hours.padStart(2, "0");

      const formattedTime = `${paddedHours}:${minutes}:00`;
      return formattedTime
    };
    data.slot.end_time = transformTime(data.slot.end_time);
    data.slot.start_time = transformTime(data.slot.start_time);
    data.student = data.student[0];
    data.topic = data.topic[0];
    console.log("🚀 ~ file: SetLesson.js:193 ~ SetLesson ~ data:", data);

    try {
      fetch_api(
        "study_session",
        "POST",
        data
      )
      .then((response) => {
        if (response.status !== 201) {
          setErrors(['קיימת בעיה זמנית באתר בקביעת שיעור, נסה מאוחר יותר'])
          return
        } 
        
        
      })

      
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <h2>קביעת שיעור</h2>
      {students && (
        <DropDown
          subjects={true}
          placeholder="בחר תלמיד"
          objects={students}
          name="student"
          value={studySession.student}
          onChange={handleChange}
        />
      )}
      <DropDown
        subSubjects={true}
        className="search-input"
        placeholder="נושא לימוד"
        objects={topics}
        name="topic"
        value={studySession.topic}
        onChange={handleChange}
      />
      <label>תאריך המפגש:</label>
      <br />
      <input
        type="date"
        name="slot.date"
        value={studySession.slot.date}
        onChange={(e) => {
          handleChange(e);
        }}
      />
      <br />

      <label>שעת התחלה:</label>
      <br />
      {hourChoices && (
        <select
          name="slot.start_time"
          value={studySession.start_time}
          onChange={(e) => handleChange(e)}
        >
          <option value={""}>בחר שעה</option>
          {hourChoices.map((h) => (
            <option value={h.display}>{h.display}</option>
          ))}
        </select>
      )}
      <br />
      <label>שעת סיום:</label>
      <br />
      {hourChoices && (
        <select
          value={studySession.end_time}
          onChange={(e) => handleChange(e)}
          name="slot.end_time"
        >
          <option value={""}>בחר שעה</option>
          {hourChoices.map((h) => (
            <option value={h.display}>{h.display}</option>
          ))}
        </select>
      )}

      <br />
      <label>לימוד דרך:</label>
      <br />

      {mentorData && (
        <select
          name="teach_method"
          value={studySession.teach_method}
          onChange={(e) => handleChange(e)}
        >
          <option value={""}>בחר --</option>
          {[
            mentorData.teach_online,
            mentorData.teach_at_mentor,
            mentorData.teach_at_student,
          ].map((pay, index) => {
            let method = "";
            if (index === 0) {
              method = { name: "אונליין", value: "online" };
            } else if (index === 1) {
              method = { name: "בבית המורה", value: "at_mentor" };
            } else if (index === 2) {
              method = { name: "בבית התלמיד", value: "at_student" };
            }
            if (pay) {
              return <option value={method.value}>{method.name}</option>;
            } else {
              return null;
            }
          })}
        </select>
      )}

      <br />
      {errors && errors.map((error) => <p className="error">{error}</p>)}
      <br />
      <button onClick={handleSubmit}>קבע שיעור</button>
    </div>
  );
}

export default SetLesson;
