import React, { useState, useRef } from "react";
import "./css/DropDown.css";

const DropDown = (props) => {
  const objects = {
    Math: [
      { name: "Algebra", id: 1 },
      { name: "Calculus", id: 2 },
      { name: "Geometry", id: 3 },
    ],
    English: [
      { name: "Poetry", id: 4 },
      { name: "Grammar", id: 5 },
      { name: "Literature", id: 6 },
    ],
  };

  const [isOpen, setIsOpen] = useState(false);
  const [isSubjectOpen, setIsSubjectOpen] = useState({});
  const [searchInput, setSearchInput] = useState("");
  const searchResRef = useRef(null);

  const handleSelected = (event) => {
    props.onChange(event);
  };

  const toggleSubject = (subject) => {
    setIsSubjectOpen((prev) => ({
      ...prev,
      [subject]: !prev[subject],
    }));
  };

  const handleSearchInputChange = (event) => {
    setIsOpen(true);
    setSearchInput(event.target.value);
  };

  const filteredSubjects = Object.keys(props.objects).map((subject) => {
    let isExist = false;
    for (let index = 0; index < props.objects[subject].length; index++) {
      if (
        props.objects[subject][index]["name"]
          .toLowerCase()
          .includes(searchInput.toLowerCase())
      ) {
        isExist = true;
        break;
      }
    }
    if (subject.toLowerCase().includes(searchInput.toLowerCase()) || isExist) {
      return subject;
    }
  });

  const handleSearchResClick = () => {
    setIsOpen(true);
    searchResRef.current.focus();
  };

  return (
    <div className="drop-down">
      <input
        className="search-input"
        onClick={() => setIsOpen(!isOpen)}
        onChange={handleSearchInputChange}
        placeholder="Search"
        name="search_bar"
      />
      {isOpen && (
        <div
          className="search-res"
          // onBlur={() => {
          //   setIsOpen(false);
          // }}
          ref={searchResRef}
          tabIndex={0}
        >
          {filteredSubjects.map((subject, index) => (
            <React.Fragment key={index}>
              <li onClick={() => toggleSubject(subject)}>{subject}</li>
              {isSubjectOpen[subject] && (
                <ul className="sub-list">
                  {props.objects[subject].map((item) => {
                    const { name, id } = item;
                    return (
                      <React.Fragment key={id}>
                        <input
                          id={id}
                          value={name}
                          name="topics"
                          checked={props.value.includes(id)}
                          onChange={handleSelected}
                          type="checkbox"
                        />
                        <label htmlFor={id}>{name}</label>
                        <br />
                      </React.Fragment>
                    );
                  })}
                </ul>
              )}
            </React.Fragment>
          ))}
        </div>
      )}
    </div>
  );
};

export default DropDown;
