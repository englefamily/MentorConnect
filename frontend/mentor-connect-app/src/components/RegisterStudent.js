import React, { useEffect, useState } from 'react'
import { Form, Button } from 'react-bootstrap';
import { years } from '../helpers/avariables.js'
import { fetch_api } from '../helpers/api_request.js'


//check if it work
//check if it work 2
//check if it work 3
//check if it work 4
function RegisterStudent() {
    const [pw2, setPw2] = useState('')
    const [errors, setErrors] = useState({});

    const [studentData, setStudentData] = useState({
        user: {
            email: '',
            password: ''
        },
        first_name: '',
        last_name: '',
        // year_of_birth: '',
        // short_description: '',
        phone_num: ''

    })

    useEffect(() => {
        console.log(studentData)
    }, [studentData])

    const handleChange = event => {
        const { name, value } = event.target;
        if (name === 'email' || name === 'password') {
            setStudentData(prev => ({
                ...prev,
                user: {
                    ...prev.user,
                    [name]: value
                }
            }));
        } else {
            setStudentData(prev => ({
                ...prev,
                [name]: value
            }));
        }
    };

    const validateForm = () => {
        let isValid = true;
        const errors = {};

        // Validate first name
        if (!studentData.first_name) {
            errors.first_name = 'שדה חובה';
            isValid = false;
        }

        // Validate last name
        if (!studentData.last_name) {
            errors.last_name = 'שדה חובה';
            isValid = false;
        }

        // Validate phone number
        if (!studentData.phone_num) {
            errors.phone_num = 'שדה חובה';
            isValid = false;
        }

        // Validate email
        if (!studentData.user.email) {
            errors.email = 'שדה חובה';
            isValid = false;
        }

        // Validate password
        if (!studentData.user.password) {
            errors.password = 'שדה חובה';
            isValid = false;
        }

        // Validate confirm password
        if (studentData.user.password !== pw2) {
            errors.confirm_password = 'הסיסמאות לא תואמות';
            isValid = false;
        }

        setErrors(errors);
        return isValid;
    };

    function handelSubmit(event) {
        event.preventDefault()
        if (validateForm()) {
            fetch_api('student', 'POST', studentData)
                .then((response) => {
                    console.log(response)
                })
                .catch((response) => {
                    const error = response.response.data.error
                    console.log(error)
                    if (error?.user?.email != undefined && error?.user?.email[0] === 'user with this email address already exists.')
                        console.log('email error')
                    
                    if (error?.phone_num != undefined && error?.phone_num[0] === 'student with this phone num already exists.'){
                        console.log('phone error')
                    }
                })

            
        }

    }

    const errorStyle = {
        color: 'red',
        fontSize: '70%',
        // paddingBottom: '0px',
        marginBottom: '0.5%'
    }

    return (

        <Form dir='rtl' onSubmit={handelSubmit}>
            <Form.Group controlId="formName">
                <Form.Label>שם פרטי</Form.Label>
                <Form.Control type="text" placeholder="הכנס שם" name='first_name' value={studentData.first_name} onChange={handleChange} />
            </Form.Group>
            {errors.first_name && <p style={errorStyle}>{errors.first_name}</p>}
            <Form.Group controlId="formName">
                <Form.Label>שם משפחה</Form.Label>
                <Form.Control type="text" placeholder="הכנס שם" name='last_name' value={studentData.last_name} onChange={handleChange} />
            </Form.Group>
            {errors.last_name && <p style={errorStyle}>{errors.last_name}</p>}
            <Form.Group controlId="formName">
                <Form.Label>מספר פאלפון</Form.Label>
                <Form.Control type="text" placeholder="הכנס שם" name='phone_num' value={studentData.phone_num} onChange={handleChange} />
            </Form.Group>
            {errors.phone_num && <p style={errorStyle}>{errors.phone_num}</p>}
            <Form.Group controlId="formName">
                <Form.Label>אמייל</Form.Label>
                <Form.Control type="email" placeholder="הכנס אמייל" name='email' value={studentData.user.email} onChange={handleChange} />
            </Form.Group>
            {errors.email && <p style={errorStyle}>{errors.email}</p>}

            {/* <Form.Group controlId="formName">
                <Form.Label>שנת לידה</Form.Label>
                <Form.Select name='year_of_birth' value={studentData.year_of_birth} onChange={handleChange}>
                    <option value="">Choose an option</option>
                    {years.map((year, index) => (
                        <option key={index} value={year}>{year}</option>
                    ))}
                    <option value="option1">Option 1</option>
                </Form.Select>
            </Form.Group> */}
            {/* <Form.Group controlId="formMessage">
                <Form.Label>קצת עליך</Form.Label >
                <Form.Control as="textarea" rows={3} placeholder="(:" name='short_description' value={studentData.short_description} onChange={handleChange} />
            </Form.Group> */}
            <Form.Group controlId="formName">
                <Form.Label>סיסמא</Form.Label>
                <Form.Control type="password" placeholder="" name='password' value={studentData.user.password} onChange={handleChange} />
            </Form.Group>
            {errors.password && <p style={errorStyle}>{errors.password}</p>}
            <Form.Group controlId="formName">
                <Form.Label>אשר סיסמא</Form.Label>
                <Form.Control type="password" placeholder="" value={pw2} onChange={(e) => { setPw2(e.target.value) }} />
            </Form.Group>
            {errors.confirm_password && <p style={errorStyle}>{errors.confirm_password}</p>}
            <Button variant="primary" type="submit">צור פרופיל</Button>
        </Form>
    )
}
// comment
export default RegisterStudent
