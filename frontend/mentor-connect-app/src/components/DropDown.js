import React, { useState, useRef, useEffect } from "react";
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
  const dropdownRef = useRef(null);

  const [selectedValue, setSelectedValue] = useState("");

  const handleSelected = (event) => {
    props.onChange(event);
  };

  useEffect(() => {
    const handleDocumentClick = (event) => {
      // Check if the clicked element is inside the dropdown container or not
      if (!dropdownRef.current.contains(event.target)) {
        setIsOpen(false);
      }
    };

    document.addEventListener("click", handleDocumentClick);

    return () => {
      document.removeEventListener("click", handleDocumentClick);
    };
  }, []);

  const openSelected = async () => {
    Object.keys(props.objects).map((subject) => {
      let selectedFound = false;
      for (let index = 0; index < props.objects[subject].length; index++) {
        if (props.value.includes(props.objects[subject][index]["value"])) {
          selectedFound = true;
          break;
        }
      }
      if (selectedFound) {
        setIsSubjectOpen((prev) => ({
          ...prev,
          [subject]: true,
        }));
      }
    });
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
    openSelected();
  };

  const filteredSubjects = () => {
    if (props.subSubjects) {
      const res = Object.keys(props.objects).map((subject) => {
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
        if (
          subject.toLowerCase().includes(searchInput.toLowerCase()) ||
          isExist
        ) {
          return subject;
        }
      });
      return res;
    } else if (props.subjects) {
      const res = props.objects.filter((item) => {
        if (
          item.name.toLowerCase().includes(searchInput.toLowerCase())
        ) {
          return item;
        }
      })
      return res
    }
    return null
  };

  const handleSearchResClick = () => {
    setIsOpen(true);
    searchResRef.current.focus();
  };

  return (
    <div className="drop-down" ref={dropdownRef}>
      <input
        className="search-input"
        onClick={() => {
          isOpen ? setIsOpen(false) : setIsOpen(true);
          openSelected();
        }}
        onChange={handleSearchInputChange}
        placeholder={selectedValue ? selectedValue : props.placeholder}
        name="search_bar"
      />
      {(isOpen) && (
        <div
          className="search-res"
          ref={searchResRef}
          tabIndex={0}
        >
          {props.subSubjects &&
            filteredSubjects().map((subject, index) => (
              <React.Fragment key={index}>
                <li onClick={() => toggleSubject(subject)}>{subject}</li>
                {isSubjectOpen[subject] && (
                  <ul className="sub-list">
                    {props.objects[subject].map((item, index) => {
                      const { name, value } = item;
                      return (
                        <React.Fragment>
                          <input
                            id={index}
                            value={value}
                            name={props.name}
                            checked={props.value.includes(value)}
                            onChange={(e)=>{handleSelected(e); setSelectedValue(name)}}
                            type="checkbox"
                          />
                          <label htmlFor={index}>{name}</label>
                          <br />
                        </React.Fragment>
                      );
                    })}
                  </ul>
                )}
              </React.Fragment>
            ))}

          {props.subjects &&
            filteredSubjects().map((item, index) => {
              const { name, value } = item;
              return (
                <React.Fragment>
                  <input
                    id={index}
                    value={value}
                    name={props.name}
                    checked={props.value.includes(value)}
                    onChange={handleSelected}
                    type="checkbox"
                  />
                  <label className="labelCheckbox" htmlFor={index}>{name}</label>
                  <br />
                </React.Fragment>
              );
            })}
        </div>
      )}
    </div>
  );
};

export default DropDown;
