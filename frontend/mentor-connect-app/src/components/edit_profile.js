import React, { useContext, useEffect, useState } from "react";
import RegisterMentor from "./RegisterMentor.js";
import RegisterStudent from "./RegisterStudent.js";
import { fetch_api } from "../helpers/functions.js";
import context from "../Context.js";
import { useNavigate } from "react-router-dom";

function EditProfile(props) {
  const { authTokens } = useContext(context);
  const [profileData, setProfileData] = useState(null);
  const navigate = useNavigate();
  const [p, setP] = useState('sadasd')

  const getData = async () => {
    if (authTokens?.access) {
      const response = await fetch_api(
        props.type,
        "GET",
        `token=${authTokens.access}`
      );
      if (response?.data) {
        let data = {};
        if (props.type === "mentor") {
          console.log('mentor')
          data = {mentor: { ...response.data.mentor }};
          data.mentor.topics = data.mentor.topics.map((topic) => topic.id);
          delete data.mentor.id;
          delete data.mentor.students;
          delete data.mentor.user.password;
        } else if (props.type === "student") {
          console.log('student')
          data ={student: { ...response.data.student }};
          delete data.student.study_cities
          delete data.student.address_city
          delete data.student.topics
          delete data.student.year_of_birth
          delete data.student.short_description
        }

        setProfileData(data);
      }

    } else {
      navigate("/");
    }
  };

  useEffect(() => {
  getData()
  }, [props.type]);

  return (
    <div>
      {(profileData?.mentor) && <RegisterMentor edit={true} data={profileData.mentor} /> }
      {(profileData?.student) && <RegisterStudent edit={true} data={profileData.student}/>}
    </div>
  );
}

export default EditProfile;
