import React, { useState, useEffect } from 'react';

function StudentsSearch() {
  const [students, setStudents] = useState([]);
  const [filteredStudents, setFilteredStudents] = useState([]);
  const [criteria, setCriteria] = useState({
    sub_topic: '',
    city: '',
    hourly_rate: '',
    time: '',
    topic: '',
    feedback: '',
  });

  useEffect(() => {
    fetch('/api/students')
      .then((response) => response.json())
      .then((data) => setStudents(data.students));
  }, []);

  useEffect(() => {
    setFilteredStudents(
      students.filter((student) => {
        // Apply all the criteria for filtering
        return (
          (!criteria.sub_topic || student.sub_topic.name === criteria.sub_topic) &&
          (!criteria.city || student.city === criteria.city) &&
          (!criteria.hourly_rate || student.hourly_rate <= criteria.hourly_rate) &&
          (!criteria.time || student.available_time === criteria.time) &&
          (!criteria.topic || student.sub_topic.topic.name === criteria.topic) &&
          (!criteria.feedback || student.feedback.rating >= criteria.feedback)
        );
      })
    );
  }, [students, criteria]);

  const handleCriteriaChange = (e) => {
    const { name, value } = e.target;
    setCriteria((prevCriteria) => ({ ...prevCriteria, [name]: value }));
  };

  // Render the filteredStudents, add inputs to change the criteria, and call handleCriteriaChange on input change
  // ...
}

export default StudentsSearch;