import React, { useState } from 'react';
import { Form, Button } from 'react-bootstrap';

const RegisterForm = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });

  const { name, email, password } = formData;

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Perform registration logic with the form data
    console.log(formData);
  };

  return (
    <Form onSubmit={handleSubmit}>
      <label></label>
    </Form>
  );
};

export default RegisterForm;
