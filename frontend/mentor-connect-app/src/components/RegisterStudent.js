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

    const validator = (event) => {
        let isValid = true;
        let error = '';

        // Validate first name
        if (event.target.name === 'first_name') {
            console.log(event.target.value)
            if (!studentData[event.target.name]) {
                error = 'שדה חובה';
                isValid = false;
            }

        }

        // Validate last name
        if (event.target.name === 'last_name') {
            if (!event.target.value) {
                console.log('---------')
                error = 'שדה חובה';
                isValid = false;
            }
        }

        // Validate phone number
        if (event.target.name === 'phone_num') {
            if (!event.target.value) {
                error = 'שדה חובה';
                isValid = false;
            }
        }

        // Validate email
        if (event.target.name === 'email') {
            if (!event.target.value) {
                error = 'שדה חובה';
                isValid = false;
            }
        }

        // Validate password
        if (event.target.name === 'password') {
            if (!event.target.value) {
                error = 'שדה חובה';
                isValid = false;
            }
        }

        // Validate confirm password
        if (event.target.name === 'confirm_password') {
            if (!event.target.value) {
                error = 'שדה חובה';
                isValid = false;
            } else if (studentData.user.password !== pw2) {
                error = 'הסיסמאות לא תואמות';
                isValid = false;
            }
        }

        setErrors((prevErrors) => ({
            ...prevErrors,
            [event.target.name]: error
        }));
        return isValid;
    };

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

    function handelSubmit(event) {
        event.preventDefault()
        if (0 === 0) {
            fetch_api('student', 'POST', studentData)
                .then((response) => {
                    console.log(response)
                })
                .catch((response) => {
                    const error = response.response.data.error
                    console.log(error)
                    if (error?.user?.email != undefined && error?.user?.email[0] === 'user with this email address already exists.') {
                        setErrors((prevErrors) => ({
                            ...prevErrors,
                            ['email']: 'המייל כבר קיים במערכת'
                        }))
                        console.log('email error')
                    }
                    if (error?.phone_num != undefined && error?.phone_num[0] === 'student with this phone num already exists.') {
                        setErrors((prevErrors) => ({
                            ...prevErrors,
                            ['phone_num']: 'מספר הפאלפון כבר קיים במערכת'
                        }))
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
                <Form.Control type="text" placeholder="הכנס שם" name='first_name' value={studentData.first_name} onChange={(e) => { handleChange(e); validator(e) }} onBlur={validator} />
            </Form.Group>
            {errors.first_name && <p style={errorStyle}>{errors.first_name}</p>}
            <Form.Group controlId="formName">
                <Form.Label>שם משפחה</Form.Label>
                <Form.Control type="text" placeholder="הכנס שם" name='last_name' value={studentData.last_name} onChange={(e) => { handleChange(e); validator(e) }} onBlur={validator} />
            </Form.Group>
            {errors.last_name && <p style={errorStyle}>{errors.last_name}</p>}
            <Form.Group controlId="formName">
                <Form.Label>מספר פאלפון</Form.Label>
                <Form.Control type="text" placeholder="הכנס שם" name='phone_num' value={studentData.phone_num} onChange={handleChange} onBlur={validator} />
            </Form.Group>
            {errors.phone_num && <p style={errorStyle}>{errors.phone_num}</p>}
            <Form.Group controlId="formName">
                <Form.Label>אמייל</Form.Label>
                <Form.Control type="email" placeholder="הכנס אמייל" name='email' value={studentData.user.email} onChange={handleChange} onBlur={validator} />
            </Form.Group>
            {errors.email && <p style={errorStyle}>{errors.email}</p>}

            {/* <Form.Group controlId="formName">
                <Form.Label>שנת לידה</Form.Label>
                <Form.Select name='year_of_birth' value={studentData.year_of_birth} onChange={handleChange} onBlur={validator}>
                    <option value="">Choose an option</option>
                    {years.map((year, index) => (
                        <option key={index} value={year}>{year}</option>
                    ))}
                    <option value="option1">Option 1</option>
                </Form.Select>
            </Form.Group> */}
            {/* <Form.Group controlId="formMessage">
                <Form.Label>קצת עליך</Form.Label >
                <Form.Control as="textarea" rows={3} placeholder="(:" name='short_description' value={studentData.short_description} onChange={handleChange} onBlur={validator} />
            </Form.Group> */}
            <Form.Group controlId="formName">
                <Form.Label>סיסמא</Form.Label>
                <Form.Control type="password" placeholder="" name='password' value={studentData.user.password} onChange={(e) => { handleChange(e); validator(e) }} onBlur={validator} />
            </Form.Group>
            {errors.password && <p style={errorStyle}>{errors.password}</p>}
            <Form.Group controlId="formName">
                <Form.Label>אשר סיסמא</Form.Label>
                <Form.Control type="password" placeholder="" name='confirm_password' value={pw2} onChange={(e) => { setPw2({e.target.value}, validator(e))}} onBlur={validator} />
            </Form.Group>
            {errors.confirm_password && <p style={errorStyle}>{errors.confirm_password}</p>}
            <Button variant="primary" type="submit">צור פרופיל</Button>
        </Form>
    )
}
// comment
export default RegisterStudent
