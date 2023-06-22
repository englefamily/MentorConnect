// Create code for a single dropdown box using React's `Select` tag so that when a category is selected
// a further sub-list opens, in the same dropdown list, to allow selection of multiple items using checkboxes.
// It also would have `search as you type` functionality that shows matching categories and sub-list items.
// The list woould need to be able to handle RTL languages.

import React, { useState } from 'react';

const CategoryDropdown = (props) => {
  const [selectedCategory, setSelectedCategory] = useState("");

  const handleCategoryChange = (event) => {
    setSelectedCategory(event.target.value);
    props.onCategoryChange(event.target.value);
  };

  return (
    <div>
      <label htmlFor="category">Select a category:</label>
      <select id="category" value={selectedCategory} onChange={handleCategoryChange}>
        <option value="">-- Select a category --</option>
        <option value="category1">Category 1</option>
        <option value="category2">Category 2</option>
        <option value="category3">Category 3</option>
      </select>
    </div>
  );
};

export default CategoryDropdown;