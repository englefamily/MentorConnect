import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const TeacherRegistrationForm = () => {
  const [formData, setFormData] = useState({
    gender: '',
    first_name: '',
    last_name: '',
    phone_num: '',
    education_level: '',
    education_start: '',
    education_completion: '',
    year_of_birth: '',
    city_residence: '',
    study_cities: [],
    self_description_title: '',
    self_description_content: '',
    teach_at_mentor: 0,
    teach_at_student: 0,
    teach_online: 0,
    experience_with: [],
    group_teaching: false
  });

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;

    if (type === 'checkbox') {
      const updatedValue = checked
        ? [...formData[name], value]
        : formData[name].filter((item) => item !== value);

      setFormData((prevFormData) => ({
        ...prevFormData,
        [name]: updatedValue
      }));
    } else {
      setFormData((prevFormData) => ({
        ...prevFormData,
        [name]: value
      }));
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    // TODO: Handle form submission
    console.log(formData);
    // Reset form
    setFormData({
      gender: '',
      first_name: '',
      last_name: '',
      phone_num: '',
      education_level: '',
      education_start: '',
      education_completion: '',
      year_of_birth: '',
      city_residence: '',
      study_cities: [],
      self_description_title: '',
      self_description_content: '',
      teach_at_mentor: 0,
      teach_at_student: 0,
      teach_online: 0,
      experience_with: [],
      group_teaching: false
    });
  };

  return (
    <div>
      <h2 style={{textAlign: 'right'}}>טופס הרשמה למורה</h2>
      <hr/>
      <Form onSubmit={handleSubmit} dir='rtl'>
        {/* Personal Information */}
        <h3>פרטים אישיים</h3>
        <Form.Group controlId="gender">
          <Form.Label>מין</Form.Label>
          <Form.Control
            as="select"
            name="gender"
            value={formData.gender}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            <option value="male">זכר</option>
            <option value="female">נקבה</option>
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="first_name">
          <Form.Label>שם פרטי</Form.Label>
          <Form.Control
            type="text"
            name="first_name"
            value={formData.first_name}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="last_name">
          <Form.Label>שם משפחה</Form.Label>
          <Form.Control
            type="text"
            name="last_name"
            value={formData.last_name}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="phone_num">
          <Form.Label>מספר טלפון</Form.Label>
          <Form.Control
            type="tel"
            name="phone_num"
            value={formData.phone_num}
            onChange={handleChange}
            required
          />
        </Form.Group>

        {/* Education */}
        <h3>השכלה</h3>
        <Form.Group controlId="education_level">
          <Form.Label>רמת השכלה</Form.Label>
          <Form.Control
            as="select"
            name="education_level"
            value={formData.education_level}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            {/* Add education level options */}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="education_start">
          <Form.Label>שנת התחלת הלימודים</Form.Label>
          <Form.Control
            as="select"
            name="education_start"
            value={formData.education_start}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            {/* Add education start options */}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="education_completion">
          <Form.Label>שנת השלמת הלימודים</Form.Label>
          <Form.Control
            as="select"
            name="education_completion"
            value={formData.education_completion}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            {/* Add education completion options */}
          </Form.Control>
        </Form.Group>

        {/* Additional Information */}
        <h3>מידע נוסף</h3>
        <Form.Group controlId="year_of_birth">
          <Form.Label>שנת לידה</Form.Label>
          <Form.Control
            as="select"
            name="year_of_birth"
            value={formData.year_of_birth}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            {/* Add year of birth options */}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="city_residence">
          <Form.Label>עיר מגורים</Form.Label>
          <Form.Control
            as="select"
            name="city_residence"
            value={formData.city_residence}
            onChange={handleChange}
            required
          >
            <option value="">בחר</option>
            {/* Add city residence options */}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="study_cities">
          <Form.Label>ערים בהן ניתן ללמוד</Form.Label>
          <Form.Control
            as="select"
            name="study_cities"
            value={formData.study_cities}
            onChange={handleChange}
            multiple
            required
          >
            {/* Add study cities options */}
          </Form.Control>
        </Form.Group>

        <Form.Group controlId="self_description_title">
          <Form.Label>כותרת התיאור האישי</Form.Label>
          <Form.Control
            type="text"
            name="self_description_title"
            value={formData.self_description_title}
            onChange={handleChange}
            required
          />
        </Form.Group>

        <Form.Group controlId="self_description_content">
          <Form.Label>תיאור עצמי</Form.Label>
          <Form.Control
            as="textarea"
            name="self_description_content"
            value={formData.self_description_content}
            onChange={handleChange}
            required
          />
        </Form.Group>

        {/* Teaching Experience */}
        <h3>פרטי השיעור</h3>
        <Form.Group controlId="teach_at_mentor">
          <Form.Label>הוראה בנושאים הקשורים לחניכים</Form.Label>
          <Form.Control
            type="number"
            name="teach_at_mentor"
            value={formData.teach_at_mentor}
            onChange={handleChange}
            step="0.01"
            min="0"
            max="100"
            required
          />
        </Form.Group>

        <Form.Group controlId="teach_at_student">
          <Form.Label>הוראה לתלמידים ביחס לחניכים</Form.Label>
          <Form.Control
            type="number"
            name="teach_at_student"
            value={formData.teach_at_student}
            onChange={handleChange}
            step="0.01"
            min="0"
            max="100"
            required
          />
        </Form.Group>

        <Form.Group controlId="teach_online">
          <Form.Label>הוראה מקוונת</Form.Label>
          <Form.Control
            type="number"
            name="teach_online"
            value={formData.teach_online}
            onChange={handleChange}
            step="0.01"
            min="0"
            max="100"
            required
          />
        </Form.Group>

        {/* Experience with */}
        <Form.Group controlId="experience_with">
          <Form.Label>ניסיון בתחומים הבאים</Form.Label>
          <Form.Check
            type="checkbox"
            name="experience_with"
            value="adhd"
            label="ADHD"
            onChange={handleChange}
            style={{alignItems: 'flex-end'}}
          />
          <Form.Check
            type="checkbox"
            name="experience_with"
            value="teaching"
            label="הוראה"
            onChange={handleChange}
          />
        </Form.Group>

        <Form.Group controlId="group_teaching">
          <Form.Check
            type="checkbox"
            name="group_teaching"
            label="הוראת קבוצה"
            checked={formData.group_teaching}
            onChange={handleChange}
          />
        </Form.Group>

        <Button variant="primary" type="submit">
          שלח
        </Button>
      </Form>
    </div>
  );
};

export default TeacherRegistrationForm;
