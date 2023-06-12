import React from 'react'
import { Navbar, Nav } from 'react-bootstrap';
import logo from '../templates/test2.png';


function BaseNavbar() {
  return (<>
    <Navbar expand="lg" dir="rtl" className='bg-custom'>
      <Navbar.Brand href="#home"><img src={logo} alt="Logo" style={{ width: '150px' }} /></Navbar.Brand>
      <Navbar.Toggle aria-controls="basic-navbar-nav" />
      <Navbar.Collapse id="basic-navbar-nav">
        <Nav className="ml-auto">
          <Nav.Link href="/" className="mr-3" style={{color: '#0A4D68'}}>בית</Nav.Link>
          <Nav.Link href="/registerMentor" className="mr-3">הרשמה למורה</Nav.Link>
          <Nav.Link href="/registerStudent" className="mr-3">הרשמה לתלמיד</Nav.Link>
          <Nav.Link href="/mentors" className="mr-3">מורים</Nav.Link>
          {/* <Nav.Link href="" className="mr-3">תלמידים</Nav.Link> */}
        </Nav>
      </Navbar.Collapse>
    </Navbar>


    </>)
}

export default BaseNavbar
