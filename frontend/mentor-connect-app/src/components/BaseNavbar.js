import React from 'react'
import { Navbar, Nav } from 'react-bootstrap';

function BaseNavbar() {
  return (
    <Navbar bg="light" expand="lg" dir="rtl">
  <Navbar.Brand href="#home">mentorConect</Navbar.Brand>
  <Navbar.Toggle aria-controls="basic-navbar-nav" />
  <Navbar.Collapse id="basic-navbar-nav">
    <Nav className="ml-auto">
      <Nav.Link href="/" className="mr-3">בית</Nav.Link>
      <Nav.Link href="/registerMentor" className="mr-3">הרשמה למורה</Nav.Link>
      <Nav.Link href="/registerStudent" className="mr-3">הרשמה לתלמיד</Nav.Link>
      <Nav.Link href="/mentors" className="mr-3">מורים</Nav.Link>
      {/* <Nav.Link href="" className="mr-3">תלמידים</Nav.Link> */}
    </Nav>
  </Navbar.Collapse>
</Navbar>

  
  )
}

export default BaseNavbar
