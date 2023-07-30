import React, { useContext } from "react";
import context from "../Context";

function SetLesson() {
  const { userData } = useContext(context);

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
