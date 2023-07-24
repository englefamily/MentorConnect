import React, { useContext, useEffect, useState } from "react";
import "./css/ShowMentors.css";
import { fetch_api, transformData } from "../helpers/functions";
import DropDown from "./DropDown";
import { CITIES_CHOICES } from "../helpers/avariables";
import Rating from "./Rating";
import context from "../Context";
import { useNavigate } from "react-router-dom";
import SendMessage from "./modals/SendMessage";

function ShowMentors() {
  const { userData, setShowLoginModal } = useContext(context)
  const [topics, setTopics] = useState([]);
  const navigate = useNavigate()
  const [selectedTopics, setSelectedTopics] = useState([]);
  const [cities, setCities] = useState(CITIES_CHOICES);
  const [selectedCities, setSelectedCities] = useState([]);
  const [mentors, setMentors] = useState([]);
  const [error, setError] = useState("");

  const fetchData = async () => {
    try {
      const response = await fetch_api("topic", "GET");
      const topics = response.data.topics;
      console.log(topics);
      setTopics(transformData(topics));
    } catch (error) {
      console.error(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  const handleSelectTopic = (event) => {
    const value = parseInt(event.target.value);
    if (selectedTopics.includes(value)) {
      setSelectedTopics((prev) => {
        return prev.filter((item) => item !== value);
      });
    } else {
      setSelectedTopics((prev) => {
        return [...prev, value];
      });
    }
  };

  const handleSelectCity = (event) => {
    const value = event.target.value;
    if (selectedCities.includes(value)) {
      setSelectedCities((prev) => {
        return prev.filter((item) => item !== value);
      });
    } else {
      setSelectedCities((prev) => {
        return [...prev, value];
      });
    }
  };

  const handleSearch = async () => {
    const topicsData = selectedTopics.join(",");
    const citiesData = selectedCities.join(",");

    const resDataParams = `topics=${topicsData}&cities=${citiesData}`;
    const response = await fetch_api("mentor", "GET", resDataParams);
    console.log("🚀 ~ file: ShowMentors.js:64 ~ handleSearch ~ response:", response)

    if (response === "error") {
      setError("קיימת בעיה זמנית באתר נסו מאוחר יותר");
      return null;
    }
    const data = response.data.mentors;
    setMentors(data);
  };

  const handleConect = async (mentorId) => {
    if (!userData) {
      // return setShowLoginModal(true)
    }
    const response = await fetch_api('chat', 'POST', {id: `${mentorId}-${userData.user_id}`})
    if (response.status === 201) {
      navigate(`/dashboard/chat/${mentorId}-${userData.user_id}`)
    }
    
    console.log("🚀 ~ file: ShowMentors.js:79 ~ handleConect ~ response:", response)
  }

  // const data = {
  //   id: "2-30",
  //   mentor: {
  //     id: 1,
  //     first_name: "איתמר",
  //     last_name: "וליס",
  //     phone_num: "0553001033",
  //     user_id: 2,
  //   },
  //   student: {
  //     id: 18,
  //     first_name: "יאיר",
  //     last_name: "הארוני",
  //     phone_num: "0554883888",
  //     user_id: 30,
  //   },
  // };
  

  return (
    
    <div className="main-div">
      
      <div className="main-search">
        <div className="dd-search">
          <DropDown
            subSubjects={true}
            className="search-input"
            placeholder="נושא לימוד"
            objects={topics}
            value={selectedTopics}
            onChange={handleSelectTopic}
          />
        </div>
        <div className="dd-search">
          <DropDown
            className="search-input"
            subjects={true}
            placeholder="עיר\אזור"
            objects={cities}
            value={selectedCities}
            onChange={handleSelectCity}
          />
        </div>
        <button className="search-bth" onClick={handleSearch}>
          חפש
        </button>
      </div>
      <div className="cards-container">
        {error && <p>{error}</p>}
        {mentors &&
          !error &&
          mentors.map((mentor) => (
            <div className="card-container">

              <div className="right-card">
                <div className="img-container">
                  <img src="https://www.kanlomdim.co.il/assets/userfiles/3027//profileimage.jpg?v=2" />
                </div>
                <div className="teachs-container">
                  {mentor.teach_online !== 0 && <p>מלמד אולניין</p>}
                  {mentor.teach_at_mentor !== 0 && <p>מלמד בבית המורה</p>}
                  {mentor.teach_at_student !== 0 && <p>מלמד בבית תלמיד</p>}
                </div>
              </div>
              <div className="center-card">
                <h2>
                  {mentor.gender === "male" ? "מורה פרטי" : "מורה פרטית"}{" "}
                  {mentor.first_name}
                </h2>
                <h6>סוג השכלה: </h6> <span>{mentor.education_level}</span>
                <br />
                <h6>השכלה:</h6>{" "}
                <span>{mentor.topics.map((topic) => topic.field + ", ")}</span>
                <br />
                <h6>ערי לימוד: </h6>
                <span>{mentor.study_cities.map((city) => city + ", ")}</span>
                <br />
                <p>{mentor.self_description_title}</p>
              </div>
              <div className="left-card">
                <div className="rating-container">
                  <span>({mentor.rating.count_rating}) </span> 
                  <Rating value={mentor.rating.avg} />
                   
                  
                </div>
                <div className="price-container">
                  מחיר:{" "}
                  {Math.max(
                    mentor.teach_at_mentor,
                    mentor.teach_online,
                    mentor.teach_at_student
                  )}
                </div>
                <div className="bth-container">
                  <button onClick={()=>handleConect(mentor.user.id)}>צור קשר עם {mentor.first_name}</button>
                </div>
              </div>
            </div>
          ))}
      </div>
    </div>
  );
}

export default ShowMentors;
