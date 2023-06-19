import React, { useState } from 'react';
import { Form, Button, Alert } from 'react-bootstrap';
import { years } from '../helpers/avariables.js';
import { fetch_api } from '../helpers/api_request.js';

function RegisterStudent() {
    const [studentCreate, setStudentCreate] = useState(false)
    const [pw2, setPw2] = useState('');
    const [errors, setErrors] = useState({});
    const [studentData, setStudentData] = useState({
        user: {
            email: '',
            password: ''
        },
        first_name: '',
        last_name: '',
        phone_num: ''
    });
    const passwordRegex = /^(?=.*[a-zA-Z])(?=.*\d)(?=.*[!@#$%^&*()\-_=+{};:,<.>])(?!.*\s).{8,}$/;

    const validateField = (name, value) => {
        let error = '';

        // Validate required fields
        if (name === 'phone_num' && value.length !== 10) {
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
        if (name === 'confirm_password' && value !== studentData.user.password) {
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
            setStudentData((prevData) => ({
                ...prevData,
                user: {
                    ...prevData.user,
                    [name.substring(5)]: value
                }
            }));
        } else {
            setStudentData((prevData) => ({
                ...prevData,
                [name]: value
            }));
        }
    };

    const handleSubmit = (event) => {
        event.preventDefault();

        let updatedErrors = {};

        Object.entries(studentData).forEach(([name, value]) => {
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
            fetch_api('student', 'POST', studentData)
                .then((response) => {
                    setStudentCreate(true)
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

    const errorStyle = {
        color: 'red',
        fontSize: '70%',
        marginBottom: '0.5%'
    };

    const formStyle = {
        // display: 'flex',
        // flexDirection: 'column',
        // alignItems: 'flex-end',
    };

    const labelStyle = {
        fontWeight: 'bold'
    };

    const buttonStyle = {
        backgroundColor: '#05BFDB',
        borderColor: '#05BFDB'
    };

    const div_display = {
        display: 'flex',
        flexDirection: 'column',
        backgroundImage: 'url(https://img.freepik.com/premium-photo/group-happy-young-students-university_85574-4531.jpg'
    }

    return (
        <div style={div_display}>
            { studentCreate && <Alert key={'success'} variant={'success'} style={{textAlign: 'center'}}>משתמש נוצר</Alert>}
                
            
            <div style={{ width: '50%', marginLeft: '50%' }}>
                <Form dir="rtl" onSubmit={handleSubmit} style={formStyle}>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>שם פרטי</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="הכנס שם"
                            name="first_name"
                            value={studentData.first_name}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors.first_name && <p style={errorStyle}>{errors.first_name}</p>}
                    </Form.Group>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>שם משפחה</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="הכנס שם"
                            name="last_name"
                            value={studentData.last_name}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors.last_name && <p style={errorStyle}>{errors.last_name}</p>}
                    </Form.Group>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>מספר פאלפון</Form.Label>
                        <Form.Control
                            type="text"
                            placeholder="הכנס שם"
                            name="phone_num"
                            value={studentData.phone_num}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors.phone_num && <p style={errorStyle}>{errors.phone_num}</p>}
                    </Form.Group>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>אמייל</Form.Label>
                        <Form.Control
                            type="email"
                            placeholder="הכנס אמייל"
                            name="user.email"
                            value={studentData.user.email}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors['user.email'] && <p style={errorStyle}>{errors['user.email']}</p>}
                    </Form.Group>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>סיסמא</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder=""
                            name="user.password"
                            value={studentData.user.password}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors['user.password'] && <p style={errorStyle}>{errors['user.password']}</p>}
                    </Form.Group>
                    <Form.Group controlId="formName">
                        <Form.Label style={labelStyle}>אשר סיסמא</Form.Label>
                        <Form.Control
                            type="password"
                            placeholder=""
                            name="confirm_password"
                            value={pw2}
                            onChange={handleChange}
                            onBlur={handleChange}
                        />
                        {errors.confirm_password && <p style={errorStyle}>{errors.confirm_password}</p>}
                    </Form.Group>
                    <Button variant="primary" type="submit" style={buttonStyle}>
                        צור פרופיל
                    </Button>
                </Form></div>
            <div>
                {/* <img src='https://img.freepik.com/premium-photo/group-happy-young-students-university_85574-4531.jpg'/> */}
            </div>
        </div>
    );
}

export default RegisterStudent;
