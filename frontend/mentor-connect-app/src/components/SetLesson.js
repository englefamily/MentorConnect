import React, { useContext, useCallback, useState } from "react";
import context from "../Context";
import axios from 'axios';

function SetLesson() {
  const { userData } = useContext(context);
  const [ form, setForm ] = useState({}); // Store Slot & Session values
  const [ response, setResponse ] = useState(null); // Manage & store API response

   // confirm user is a `mentor`
   if (userData.userRole !== "mentor") {
     return (
      <div>Only mentors can create Study Sessions</div>
      );
   }

  const handleChange = useCallback((event) => {
    setForm(f => ({ ...f, [event.target.name]: event.target.value }));
  }, []);

  const createLesson = async (e) => {
    e.preventDefault();

  return (
    <div>
      set lesson
      {userData.user_id}
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
