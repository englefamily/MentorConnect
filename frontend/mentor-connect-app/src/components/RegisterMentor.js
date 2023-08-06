import React, { useContext, useEffect, useState } from "react";
import { Form, Button } from "react-bootstrap";
import { fetch_api, transformData } from "../helpers/functions.js";
import {
  years,
  EDUCATION_LEVEL,
  CITIES_CHOICES,
  EXPERIENCE_WITH,
} from "../helpers/avariables.js";
import Select from "react-select";
import DropDown from "./DropDown.js";
import { useNavigate } from "react-router-dom";
import context from "../Context.js";

const RegisterMentor = (props) => {
  console.log("🚀 ~ file: RegisterMentor.js:16 ~ RegisterMentor ~ props:", props)
  const { loginUser, authTokens } = useContext(context);
  const [mentorCreated, setMentorCreated] = useState(false);
  const [teachField, setTeachField] = useState(
    props.edit
      ? {
          teach_at_mentor: props.data.teach_at_mentor ? false : true,
          teach_at_student: props.data.teach_at_student ? false : true,
          teach_online: props.data.teach_online ? false : true,
        }
      : {
          teach_at_mentor: true,
          teach_at_student: true,
          teach_online: true,
        }
  );
  const [pw2, setPw2] = useState("");
  const [topics, setTopics] = useState([]);
  const [errors, setErrors] = useState({});
  const [mentorData, setMentorData] = useState(
    props.edit
      ? props.data
      : {
          user: {
            email: "",
            password: "",
          },
          // study_cities: [],
          gender: "",
          first_name: "",
          last_name: "",
          phone_num: "",
          education_level: "",
          education_start: "",
          education_completion: "",
          year_of_birth: "",
          city_residence: "",
          self_description_title: "",
          self_description_content: "",
          teach_at_mentor: 0,
          teach_at_student: 0,
          teach_online: 0,
          study_cities: [],
          experience_with: [],
          group_teaching: false,
          topics: [],
        }
  );

  const passwordRegex =
    /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?!.*\s).{8,}$/;
  const phoneNumberRegex = /^05\d{8}$/;
  const priceRegex = /^([4-9][0-9]|[1-3][0-9]{2}|400)$/;
  const textRegex = /^[\u0591-\u05F4a-zA-Z]+$/u;

  const navigate = useNavigate();

  useEffect(() => {
  }, [mentorData, topics]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch_api("topic", "GET");
        const topics = response.data.topics;
        setTopics(transformData(topics));
      } catch (error) {
        console.error(error);
      }
    };

    fetchData();
  }, []);

  const validateField = (name, value) => {
    let error = "";

    if (name === "experience_with" || name === "group_teaching") {
      return error;
    }
    // Validate required fields
    if (name === "phone_num" && !phoneNumberRegex.test(value)) {
      error = "מספר הפאלפון חייב להיות בעל 10 ספרות";
    }

    if (
      name === "teach_online" ||
      name === "teach_at_mentor" ||
      name === "teach_at_student"
    ) {
      if (!priceRegex.test(value) && teachField[name] !== true) {
        error = "טווח המחירים חייב להיות בין 40 ל 400";
      }

      if (value === "" && teachField[name] !== true) {
        error = "שדה חובה";
      }
      return error;
    }

    if (name === "user.password" && !passwordRegex.test(value)) {
      error = `כללי הסיסמה:
            - מכילה לפחות 8 תווים
            - מכילה לפחות אות אחת גדולה או קטנה (a-z או A-Z)
            - מכילה לפחות מספר אחד (0-9)
            - מכילה לפחות תו מיוחד אחד (!@#$%^&*()\-_=+{};:,<.>)
            - אינה מכילה רווחים`;
    }
    //
    if (typeof value === "object") {
      if (value.length === 0) {
        error = "שדה חובה";
      }
      return error;
    }

    if (name.endsWith("name") && !textRegex.test(value)) {
      error = "שדה זה יכול להכיל רק אותיות";
    }

    if (
      typeof value === "string" &&
      (value === undefined || value.trim() === "")
    ) {
      error = "שדה חובה";
    }

    // Validate confirm password
    if (name === "confirm_password" && value !== mentorData.user.password) {
      error = "הסיסמאות לא תואמות";
    }
    return error;
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    if (value === null) {
      value = "";
    }

    if (name.startsWith("teach_") && value === "on") {
      if (teachField[name] === false) {
        setMentorData((prevState) => ({
          ...prevState,
          [name]: 0,
        }));
        setErrors((prevErrors) => ({
          ...prevErrors,
          [name]: "",
        }));
      }
      setTeachField((prevState) => ({
        ...prevState,
        [name]: !prevState[name],
      }));
      return null;
    }

    let error = validateField(name, value);
    setErrors((prevErrors) => {
      if (name === "user.password" && value === pw2) {
        // todo to match if user.password
        return {
          ...prevErrors,
          [name]: error,
          confirm_password: "",
        };
      } else if (name === "user.password" && pw2 && value !== pw2) {
        return {
          ...prevErrors,
          [name]: error,
          confirm_password: "הסיסמאות לא תואמות",
        };
      } else {
        return {
          ...prevErrors,
          [name]: error,
        };
      }
    });
    if (name === "group_teaching") {
      setMentorData((prevState) => ({
        ...prevState,
        [name]: !prevState[name],
      }));
    } else if (name === "confirm_password") {
      setPw2(value);
    } else if (name.startsWith("user.")) {
      setMentorData((prevData) => ({
        ...prevData,
        user: {
          ...prevData.user,
          [name.substring(5)]: value,
        },
      }));
    } else if (
      name === "topics" ||
      name === "study_cities" ||
      name === "experience_with"
    ) {
      setMentorData((prev) => {
        if (name === "topics") {
          const topicId = parseInt(value);
          const updatedTopics = prev.topics.includes(topicId)
            ? prev.topics.filter((item) => item !== topicId)
            : [...prev.topics, topicId];

          return {
            ...prev,
            [name]: updatedTopics,
          };
        } else if (name === "study_cities") {
          const updatedStudyCities = prev.study_cities.includes(value)
            ? prev.study_cities.filter((city) => city !== value)
            : [...prev.study_cities, value];

          return {
            ...prev,
            [name]: updatedStudyCities,
          };
        } else if (name === "experience_with") {
          const updatedExperienceWith = prev.experience_with.includes(value)
            ? prev.experience_with.filter((experience) => experience !== value)
            : [...prev.experience_with, value];

          return {
            ...prev,
            [name]: updatedExperienceWith,
          };
        }
        return prev;
      });
    } else {
      setMentorData((prevData) => ({
        ...prevData,
        [name]: value,
      }));
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    let updatedErrors = {};

    Object.entries(mentorData).forEach(([name, value]) => {
      if (name === "user") {
        Object.entries(value).forEach(([name, value]) => {
          if (!props.edit || (props.edit && name !== "password")) {
            const error = validateField("user." + name, value);
            if (error !== "") {
              updatedErrors["user." + name] = error;
            }
          }
        });
      } else {
        const error = validateField(name, value);
        if (error !== "") {
          updatedErrors[name] = error;
        }
      }
      if (!props.edit) {
        const error = validateField("confirm_password", pw2);
        if (error !== "") {
          updatedErrors["confirm_password"] = error;
        }
      }
      if (
        teachField.teach_at_mentor &&
        teachField.teach_at_student &&
        teachField.teach_online
      ) {
        updatedErrors["teach_at"] = "חובה לבחור את אחד מדרכי הלימוד";
      }
    });
    setErrors(updatedErrors);
    if (Object.keys(updatedErrors).length === 0) {
      handleFetch().then((response) => {
        console.log("🚀 ~ file: RegisterMentor.js:295 ~ handleFetch ~ response:", response)
        // if (response?.response?.status === 500) {
        //   return;
        //   }
          
        const error = response?.response?.data?.error;
        console.log("🚀 ~ file: RegisterMentor.js:301 ~ handleFetch ~ error:", error === "UNIQUE constraint failed: student.phone_num")
        if (error) {
          let phone_num_error = "";
          let email_error = "";
          if (
            error?.user?.email !== undefined &&
            error?.user?.email[0] ===
              "user with this email address already exists."
          ) {
            email_error = "המייל כבר קיים במערכת";
          }

          if (
            error?.phone_num !== undefined &&
            (error?.phone_num[0] === "mentor with this phone num already exists.")
          ) {
            phone_num_error = "מספר הפאלפון כבר קיים במערכת";
          }
          if (
            error !== undefined &&
            (error === "UNIQUE constraint failed: student.phone_num")
          ) {
            phone_num_error = "מספר הפאלפון כבר קיים במערכת";
          }
          setErrors((prevErrors) => ({
            ...prevErrors,
            ["user.email"]: email_error,
            ["phone_num"]: phone_num_error,
          }));
        } else {
          if (props.edit) {
          // window.location.reload()
          return ;
          }
          loginUser(mentorData.user.email, mentorData.user.password).then((res) => {
            if (res !== null){
            navigate("/dashboard/edit_profile");
          }
          })
          
        }
        
      });
    }
  };

  const handleFetch = async () => {
    let res = null;
    if (props.edit) {
      mentorData["token"] = authTokens?.access;
      res = await fetch_api("mentor", "PUT", mentorData);
    } else {
      res = await fetch_api("mentor", "POST", mentorData);
    }
    return res;
  };

  return (
    <div
      className="registration-form"
      style={{ overflowY: "scroll", height: "93.5vh" }}
    >
      <h2 style={{ textAlign: "right" }}>טופס הרשמה</h2>
      <Form onSubmit={handleSubmit} dir="rtl">
        <h4>פרופיל</h4>
        {/* First Name */}
        <Form.Group controlId="firstName">
          <Form.Label>שם פרטי</Form.Label>
          <Form.Control
            type="text"
            name="first_name"
            value={mentorData.first_name}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors.first_name && (
            <Form.Text className="text-danger">{errors.first_name}</Form.Text>
          )}
        </Form.Group>
        {/* Last Name */}
        <Form.Group controlId="lastName">
          <Form.Label>שם משפחה</Form.Label>
          <Form.Control
            type="text"
            name="last_name"
            value={mentorData.last_name}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors.last_name && (
            <Form.Text className="text-danger">{errors.last_name}</Form.Text>
          )}
        </Form.Group>
        {/* Phone Number */}
        <Form.Group controlId="phoneNum">
          <Form.Label>מספר טלפון</Form.Label>
          <Form.Control
            type="tel"
            name="phone_num"
            value={mentorData.phone_num}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors.phone_num && (
            <Form.Text className="text-danger">{errors.phone_num}</Form.Text>
          )}
        </Form.Group>
        <Form.Group controlId="email">
          <Form.Label>כתובת דוא"ל</Form.Label>
          <Form.Control
            type="email"
            name="user.email"
            value={mentorData.user.email}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors["user.email"] && (
            <Form.Text className="text-danger">
              {errors["user.email"]}
            </Form.Text>
          )}
        </Form.Group>
        {!props.edit && (
          <>
            <Form.Group controlId="user.password">
              <Form.Label>סיסמה</Form.Label>
              <Form.Control
                type="password"
                name="user.password"
                value={mentorData.user.password}
                onChange={handleChange}
                onBlur={handleChange}
              />
              {errors["user.password"] && (
                <Form.Text className="text-danger">
                  {errors["user.password"]}
                </Form.Text>
              )}
            </Form.Group>
            <Form.Group controlId="confirmPassword">
              <Form.Label>אשר סיסמא</Form.Label>
              <Form.Control
                type="password"
                name="confirm_password"
                value={pw2}
                onChange={handleChange}
                onBlur={handleChange}
              />
              {errors.confirm_password && (
                <Form.Text className="text-danger">
                  {errors.confirm_password}
                </Form.Text>
              )}
            </Form.Group>
          </>
        )}
        <br />
        <h4>פרטים אישיים</h4>
        {/* Gender */}
        <Form.Group controlId="gender">
          <Form.Label>מין</Form.Label>
          <Form.Control
            as="select"
            name="gender"
            value={mentorData.gender}
            onChange={handleChange}
            onBlur={handleChange}
          >
            <option value="">בחר מין</option>
            <option value="male">זכר</option>
            <option value="female">נקבה</option>
          </Form.Control>
          {errors.gender && (
            <Form.Text className="text-danger">{errors.gender}</Form.Text>
          )}
        </Form.Group>
        {/* Year of Birth */}
        <Form.Group controlId="yearOfBirth">
          <Form.Label>שנת לידה</Form.Label>
          <Form.Control
            as="select"
            name="year_of_birth"
            value={mentorData.year_of_birth}
            onChange={handleChange}
            onBlur={handleChange}
          >
            <option value="">בחר שנת לידה</option>
            {years(1933, 2006)
              .reverse()
              .map((year) => (
                <option value={year}>{year}</option>
              ))}
          </Form.Control>
          {errors.year_of_birth && (
            <Form.Text className="text-danger">
              {errors.year_of_birth}
            </Form.Text>
          )}
        </Form.Group>
        {/* City of Residence */}
        <Form.Group controlId="cityResidence">
          <Form.Label>עיר מגורים</Form.Label>
          <DropDown
            subjects={true}
            placeholder="עיר\אזור"
            objects={CITIES_CHOICES}
            name="city_residence"
            value={mentorData.city_residence}
            onChange={handleChange}
          />

          {errors.city_residence && (
            <Form.Text className="text-danger">
              {errors.city_residence}
            </Form.Text>
          )}
        </Form.Group>{" "}
        {/* Education Level */}
        <Form.Group controlId="educationLevel">
          <Form.Label>רמת השכלה</Form.Label>
          <Form.Control
            as="select"
            name="education_level"
            value={mentorData.education_level}
            onChange={handleChange}
            onBlur={handleChange}
          >
            <option value="">בחר רמת השכלה</option>
            {EDUCATION_LEVEL.map(([value_, name_]) => (
              <option value={value_}>{name_}</option>
            ))}
          </Form.Control>
          {errors.education_level && (
            <Form.Text className="text-danger">
              {errors.education_level}
            </Form.Text>
          )}
        </Form.Group>
        {/* Education Start */}
        <Form.Group controlId="educationStart">
          <Form.Label>תחילת לימודים</Form.Label>
          <Form.Control
            as="select"
            name="education_start"
            value={mentorData.education_start}
            onChange={handleChange}
            onBlur={handleChange}
          >
            <option value="">בחר שנת התחלת לימודים</option>
            {years(1983, 2023)
              .reverse()
              .map((year) => (
                <option value={year}>{year}</option>
              ))}
          </Form.Control>
          {errors.education_start && (
            <Form.Text className="text-danger">
              {errors.education_start}
            </Form.Text>
          )}
        </Form.Group>
        {/* Education Completion */}
        <Form.Group controlId="educationCompletion">
          <Form.Label>סיום לימודים</Form.Label>
          <Form.Control
            as="select"
            name="education_completion"
            value={mentorData.education_completion}
            onChange={handleChange}
            onBlur={handleChange}
          >
            <option value="">בחר שנת סיום לימודים</option>
            {years(1984, 2030)
              .reverse()
              .map((year) => (
                <option value={year}>{year}</option>
              ))}
          </Form.Control>
          {errors.education_completion && (
            <Form.Text className="text-danger">
              {errors.education_completion}
            </Form.Text>
          )}
        </Form.Group>
        <br />
        <h4>פרטי השיעור</h4>
        <Form.Group controlId="educationCompletion">
          <Form.Label>נושאי לימוד</Form.Label>
          <DropDown
            subSubjects={true}
            name={"topics"}
            objects={topics}
            value={mentorData.topics}
            placeholder={"חפש נושא"}
            onChange={handleChange}
          />
          {errors.topics && (
            <Form.Text className="text-danger">{errors.topics}</Form.Text>
          )}
        </Form.Group>
        <Form.Group>
          <Form.Label>שיעורי אונליין</Form.Label>
          <br />
          <input
            type="checkbox"
            name="teach_online"
            onChange={handleChange}
            checked={!teachField.teach_online}
          />
          <Form.Control
            type="number"
            placeholder="מחיר"
            disabled={teachField.teach_online}
            name="teach_online"
            onChange={handleChange}
            value={mentorData.teach_online}
          />
        </Form.Group>
        {errors.teach_online && (
          <Form.Text className="text-danger">{errors.teach_online}</Form.Text>
        )}
        <Form.Group>
          <Form.Label>שיעורים אצל מורה</Form.Label>
          <br />
          <input
            type="checkbox"
            name="teach_at_mentor"
            onChange={handleChange}
            checked={!teachField.teach_at_mentor}
          />
          <Form.Control
            type="number"
            placeholder="מחיר"
            disabled={teachField.teach_at_mentor}
            name="teach_at_mentor"
            onChange={handleChange}
            value={mentorData.teach_at_mentor}
          />
        </Form.Group>
        {errors.teach_at_mentor && (
          <Form.Text className="text-danger">
            {errors.teach_at_mentor}
          </Form.Text>
        )}
        <Form.Group>
          <Form.Label>שיעורים אצל תלמיד</Form.Label>
          <br />
          <input
            type="checkbox"
            name="teach_at_student"
            onChange={handleChange}
            checked={!teachField.teach_at_student}
          />
          <Form.Control
            type="number"
            placeholder="מחיר"
            disabled={teachField.teach_at_student}
            name="teach_at_student"
            onChange={handleChange}
            value={mentorData.teach_at_student}
          />
          {errors.teach_at_student && (
            <Form.Text className="text-danger">
              {errors.teach_at_student}
            </Form.Text>
          )}
        </Form.Group>
        {errors.teach_at && (
          <Form.Text className="text-danger">{errors.teach_at}</Form.Text>
        )}
        {/* Study Cities */}
        {/* todo add is Disable */}
        <Form.Group controlId="studyCities">
          <Form.Label>ערי לימוד</Form.Label>

          <DropDown
            subjects={true}
            placeholder="עיר\אזור"
            objects={CITIES_CHOICES}
            name="study_cities"
            value={mentorData.study_cities}
            onChange={handleChange}
          />

          {/* <Select
            isMulti
            name="study_cities"
            value={mentorData.study_cities}
            options={CITIES_CHOICES}
            onChange={(res) => {
              handleChange({ target: { value: res, name: "study_cities" } });
            }}
            onBlur={(res) => {
              handleChange({
                target: {
                  value: mentorData.study_cities,
                  name: "study_cities",
                },
              });
            }}
          /> */}
          {errors.study_cities && (
            <Form.Text className="text-danger">{errors.study_cities}</Form.Text>
          )}
        </Form.Group>
        <br />
        <Form.Group>
          <input
            type="checkbox"
            name="group_teaching"
            checked={mentorData.group_teaching}
            onChange={handleChange}
            style={{ marginLeft: "2px" }}
          />
          <Form.Label>מלמד בקבוצות</Form.Label>
        </Form.Group>
        <Form.Group controlId="experienceWith">
          <Form.Label>ניסיון עם</Form.Label>
          <DropDown
            subjects={true}
            placeholder="ניסיון עם"
            objects={EXPERIENCE_WITH}
            name="experience_with"
            value={mentorData.experience_with}
            onChange={handleChange}
          />
          {/* <Select
            isMulti
            name="experience_with"
            value={mentorData.experience_with}
            options={EXPERIENCE_WITH}
            onChange={(res) => {
              handleChange({ target: { value: res, name: "experience_with" } });
            }}
            onBlur={(res) => {
              handleChange({
                target: {
                  value: mentorData.experience_with,
                  name: "experience_with",
                },
              });
            }}
          /> */}
          {errors.experience_with && (
            <Form.Text className="text-danger">
              {errors.experience_with}
            </Form.Text>
          )}
        </Form.Group>
        {/* Self Description Title */}
        <Form.Group controlId="selfDescriptionTitle">
          <Form.Label>ספר על עצמך בקצרה</Form.Label>
          <Form.Control
            as="textarea"
            rows={3}
            name="self_description_title"
            value={mentorData.self_description_title}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors.self_description_title && (
            <Form.Text className="text-danger">
              {errors.self_description_title}
            </Form.Text>
          )}
        </Form.Group>
        {/* Self Description Content */}
        <Form.Group controlId="selfDescriptionContent">
          <Form.Label>ספר על עצמך ועל התנהלות השיעור האריכות</Form.Label>
          <Form.Control
            as="textarea"
            rows={7}
            name="self_description_content"
            value={mentorData.self_description_content}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors.self_description_content && (
            <Form.Text className="text-danger">
              {errors.self_description_content}
            </Form.Text>
          )}
        </Form.Group>
        <Button variant="primary" type="submit">
          שלח
        </Button>
      </Form>
    </div>
  );
};

export default RegisterMentor;
