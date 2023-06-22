import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';
import { fetch_api } from '../helpers/api_request.js';

const RegisterMentor = () => {
  const [mentorCreated, setMentorCreated] = useState(false)
  const [pw2, setPw2] = useState('');
  const [errors, setErrors] = useState({});
  const [mentorData, setMentorData] = useState({
    user: {
      email: "",
      password: ""
    },
    study_cities: [
    ],
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
    teach_at_mentor: "",
    teach_at_student: "",
    teach_online: "",
    experience_with: [
    ],
    group_teaching: true,
    // students: [
    //     1
    // ],
    sub_topics: [
    ]
  });
  const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?!.*\s).{8,}$/;
  const phoneNumberRegex = /^05\d{8}$/;


  const validateField = (name, value) => {
    let error = '';

    // Validate required fields
    if (name === 'phone_num' && !phoneNumberRegex.test(value)) {
      error = 'מספר הפאלפון חייב להיות בעל 10 ספרות';
    }

    if (name === 'user.password' && !passwordRegex.test(value)) {
      error = `כללי הסיסמה:
            - מכילה לפחות 8 תווים
            - מכילה לפחות אות אחת גדולה או קטנה (a-z או A-Z)
            - מכילה לפחות מספר אחד (0-9)
            - מכילה לפחות תו מיוחד אחד (!@#$%^&*()\-_=+{};:,<.>)
            - אינה מכילה רווחים`;
    }

    if (value.trim() === '') {
      error = 'שדה חובה';
    }

    // Validate confirm password
    if (name === 'confirm_password' && value !== mentorData.user.password) {
      error = 'הסיסמאות לא תואמות';
    }

    return error;
  };

  const handleChange = (event) => {
    const { name, value } = event.target;
    let error = validateField(name, value);

    setErrors((prevErrors) => {
      if (name === 'user.password' && value === pw2) {
        return {
          ...prevErrors,
          [name]: error,
          confirm_password: ''
        };
      } else if (name === 'user.password' && pw2 && value !== pw2) {
        return {
          ...prevErrors,
          [name]: error,
          confirm_password: 'הסיסמאות לא תואמות'
        };
      } else {
        return {
          ...prevErrors,
          [name]: error
        };
      }
    });

    if (name === 'confirm_password') {
      setPw2(value);
    } else if (name.startsWith('user.')) {
      setMentorData((prevData) => ({
        ...prevData,
        user: {
          ...prevData.user,
          [name.substring(5)]: value
        }
      }));
    } else {
      setMentorData((prevData) => ({
        ...prevData,
        [name]: value
      }));
    }
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    let updatedErrors = {};

    Object.entries(mentorData).forEach(([name, value]) => {
      if (name === 'user') {
        Object.entries(value).forEach(([name, value]) => {
          const error = validateField('user.' + name, value);
          if (error !== '') {
            updatedErrors['user.' + name] = error;
          }
        });
      } else {
        const error = validateField(name, value);
        if (error !== '') {
          updatedErrors[name] = error;
        }
      }
      const error = validateField('confirm_password', pw2);
      if (error !== '') {
        updatedErrors['confirm_password'] = error;
      }
    });
    setErrors(updatedErrors);

    if (Object.keys(updatedErrors).length === 0) {
      fetch_api('mentor', 'POST', mentorData)
        .then((response) => {
          setMentorCreated(true)
          console.log(response);
        })
        .catch((response) => {
          let phone_num_error = '';
          let email_error = '';
          const error = response.response.data.error;

          if (
            error?.user?.email != undefined &&
            error?.user?.email[0] === 'user with this email address already exists.'
          ) {
            email_error = 'המייל כבר קיים במערכת';
          }
          if (
            error?.phone_num != undefined &&
            error?.phone_num[0] === 'student with this phone num already exists.'
          ) {
            phone_num_error = 'מספר הפאלפון כבר קיים במערכת';
          }

          setErrors((prevErrors) => ({
            ...prevErrors,
            ['user.email']: email_error,
            ['phone_num']: phone_num_error
          }));
        });
    }
  };

  return (
    <div className="registration-form">
      <h2 style={{ textAlign: 'right' }}>טופס הרשמה</h2>
      <Form onSubmit={handleSubmit} dir='rtl'>
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
          {errors.first_name && <Form.Text className="text-danger">{errors.first_name}</Form.Text>}
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
          {errors.last_name && <Form.Text className="text-danger">{errors.last_name}</Form.Text>}
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
          {errors.phone_num && <Form.Text className="text-danger">{errors.phone_num}</Form.Text>}
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
          {errors['user.email'] && <Form.Text className="text-danger">{errors['user.email']}</Form.Text>}
        </Form.Group>

        <Form.Group controlId="user.password">
          <Form.Label>סיסמה</Form.Label>
          <Form.Control
            type="password"
            name="user.password"
            value={mentorData.user.password}
            onChange={handleChange}
            onBlur={handleChange}
          />
          {errors['user.password'] && <Form.Text className="text-danger">{errors['user.password']}</Form.Text>}
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
          {errors.confirm_password && <Form.Text className="text-danger">{errors.confirm_password}</Form.Text>}
        </Form.Group>

        {/* Study Cities */}
        {/* <Form.Group controlId="studyCities">
          <Form.Label>ערים לימוד</Form.Label>
          <Form.Control
            as="select"
            name="studyCities"
            multiple
            value={mentorData.studyCities}
            onChange={handleChange}
          >
            <option value="Tel Aviv-Yafo">תל אביב-יפו</option>
            <option value="Jerusalem">ירושלים</option>
          </Form.Control>
          {errors.studyCities && <Form.Text className="text-danger">{errors.studyCities}</Form.Text>}
        </Form.Group> */}

        {/* Gender */}
        {/* <Form.Group controlId="gender">
          <Form.Label>מין</Form.Label>
          <Form.Control
            as="select"
            name="gender"
            value={mentorData.gender}
            onChange={handleChange}
          >
            <option value="">בחר מין</option>
            <option value="male">זכר</option>
            <option value="female">נקבה</option>
          </Form.Control>
          {errors.gender && <Form.Text className="text-danger">{errors.gender}</Form.Text>}
        </Form.Group> */}

        {/* Education Level */}
        {/* <Form.Group controlId="educationLevel">
          <Form.Label>רמת השכלה</Form.Label>
          <Form.Control
            as="select"
            name="educationLevel"
            value={mentorData.educationLevel}
            onChange={handleChange}
          >
            <option value="">בחר רמת השכלה</option>
          </Form.Control>
          {errors.educationLevel && <Form.Text className="text-danger">{errors.educationLevel}</Form.Text>}
        </Form.Group> */}

        {/* Education Start */}
        {/* <Form.Group controlId="educationStart">
          <Form.Label>תחילת לימודים</Form.Label>
          <Form.Control
            as="select"
            name="educationStart"
            value={mentorData.educationStart}
            onChange={handleChange}
          >
            <option value="">בחר שנת התחלת לימודים</option>
          </Form.Control>
          {errors.educationStart && <Form.Text className="text-danger">{errors.educationStart}</Form.Text>}
        </Form.Group> */}

        {/* Education Completion */}
        {/* <Form.Group controlId="educationCompletion">
          <Form.Label>סיום לימודים</Form.Label>
          <Form.Control
            as="select"
            name="educationCompletion"
            value={mentorData.educationCompletion}
            onChange={handleChange}
          >
            <option value="">בחר שנת סיום לימודים</option>
          </Form.Control>
          {errors.educationCompletion && <Form.Text className="text-danger">{errors.educationCompletion}</Form.Text>}
        </Form.Group> */}

        {/* Year of Birth */}
        {/* <Form.Group controlId="yearOfBirth">
          <Form.Label>שנת לידה</Form.Label>
          <Form.Control
            as="select"
            name="yearOfBirth"
            value={mentorData.yearOfBirth}
            onChange={handleChange}
          >
            <option value="">בחר שנת לידה</option>
          </Form.Control>
          {errors.yearOfBirth && <Form.Text className="text-danger">{errors.yearOfBirth}</Form.Text>}
        </Form.Group> */}

        {/* City of Residence */}
        {/* <Form.Group controlId="cityResidence">
          <Form.Label>עיר מגורים</Form.Label>
          <Form.Control
            as="select"
            name="cityResidence"
            value={mentorData.cityResidence}
            onChange={handleChange}
          >
            <option value="">בחר עיר מגורים</option>
          </Form.Control>
          {errors.cityResidence && <Form.Text className="text-danger">{errors.cityResidence}</Form.Text>}
        </Form.Group> */}

        {/* Self Description Title */}
        {/* <Form.Group controlId="selfDescriptionTitle">
          <Form.Label>כותרת תיאור עצמי</Form.Label>
          <Form.Control
            type="text"
            name="selfDescriptionTitle"
            value={mentorData.selfDescriptionTitle}
            onChange={handleChange}
          />
          {errors.selfDescriptionTitle && <Form.Text className="text-danger">{errors.selfDescriptionTitle}</Form.Text>}
        </Form.Group> */}

        {/* Self Description Content */}
        {/* <Form.Group controlId="selfDescriptionContent">
          <Form.Label>תיאור עצמי</Form.Label>
          <Form.Control
            as="textarea"
            rows={4}
            name="selfDescriptionContent"
            value={mentorData.selfDescriptionContent}
            onChange={handleChange}
          />
          {errors.selfDescriptionContent && <Form.Text className="text-danger">{errors.selfDescriptionContent}</Form.Text>}
        </Form.Group> */}

        {/* Teach at Mentor */}
        {/* <Form.Group controlId="teachAtMentor">
          <Form.Label>לימוד עם מנטור (בש"ח)</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            name="teachAtMentor"
            value={mentorData.teachAtMentor}
            onChange={handleChange}
          />
          {errors.teachAtMentor && <Form.Text className="text-danger">{errors.teachAtMentor}</Form.Text>}
        </Form.Group> */}

        {/* Teach at Student */}
        {/* <Form.Group controlId="teachAtStudent">
          <Form.Label>לימוד עם תלמיד (בש"ח)</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            name="teachAtStudent"
            value={mentorData.teachAtStudent}
            onChange={handleChange}
          />
          {errors.teachAtStudent && <Form.Text className="text-danger">{errors.teachAtStudent}</Form.Text>}
        </Form.Group> */}

        {/* Teach Online */}
        {/* <Form.Group controlId="teachOnline">
          <Form.Label>לימוד מקוון (בש"ח)</Form.Label>
          <Form.Control
            type="number"
            step="0.01"
            name="teachOnline"
            value={mentorData.teachOnline}
            onChange={handleChange}
          />
          {errors.teachOnline && <Form.Text className="text-danger">{errors.teachOnline}</Form.Text>}
        </Form.Group> */}

        {/* Experience With */}
        {/* <Form.Group controlId="experienceWith">
          <Form.Label>ניסיון ב</Form.Label>
          <Form.Check
            inline
            label="ADHD"
            type="checkbox"
            name="experienceWith"
            value="adhd"
            checked={mentorData.experienceWith.includes('adhd')}
            onChange={handleChange}
          />
          <Form.Check
            inline
            label="לימוד"
            type="checkbox"
            name="experienceWith"
            value="teaching"
            checked={mentorData.experienceWith.includes('teaching')}
            onChange={handleChange}
          />
          {errors.experienceWith && <Form.Text className="text-danger">{errors.experienceWith}</Form.Text>}
        </Form.Group> */}

        {/* Group Teaching */}
        {/* <Form.Group controlId="groupTeaching">
          <Form.Check
            type="checkbox"
            label="לימוד קבוצתי"
            name="groupTeaching"
            checked={mentorData.groupTeaching}
            onChange={handleChange}
          />
          {errors.groupTeaching && <Form.Text className="text-danger">{errors.groupTeaching}</Form.Text>}
        </Form.Group> */}

        <Button variant="primary" type="submit">
          שלח
        </Button>
      </Form>
    </div>
  );
};

export default RegisterMentor;
