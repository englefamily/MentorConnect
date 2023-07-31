import React, { useContext, useCallback, useState, useEffect } from "react";
import context from "../Context";
import axios from 'axios';
import { fetch_api } from "../helpers/functions";

function SetLesson() {
  const { userData } = useContext(context);
  const [students, setStudents] = useState([])

  const getStudents = async () => {
    try {
      const response = await fetch_api("students_mentor_chats", "GET", userData.user_id);
      const student = response.data.students;
      console.log("🚀 ~ file: SetLesson.js:13 ~ getStudents ~ student:", student)

      setStudents(student)
    } catch (error) {
      console.error(error);
    }
  }


  useEffect(()=>{
    getStudents()
  }, [])

  return (
    <div>
      {students && students.map((student)=>student.first_name)}
      {/* <DropDown
        subjects={true}
        placeholder="עיר\אזור"
        objects={CITIES_CHOICES}
        name="city_residence"
        value={mentorData.city_residence}
        onChange={handleChange}
      /> */}
    </div>
  );
}

export default SetLesson;
