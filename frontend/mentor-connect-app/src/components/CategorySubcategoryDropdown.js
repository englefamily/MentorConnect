import React, { useState } from 'react';
import CategoryDropdown from './CategoryDropdown';
import SubcategoryDropdown from './SubcategoryDropdown';

const CategorySubcategoryDropdown = () => {
  const [selectedCategory, setSelectedCategory] = useState("");
  const [selectedSubcategory, setSelectedSubcategory] = useState("");

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    setSelectedSubcategory("");
  };

  const handleSubcategoryChange = (subcategory) => {
    setSelectedSubcategory(subcategory);
  };

  return (
    <div>
      <CategoryDropdown onCategoryChange={handleCategoryChange} />
      {selectedCategory && (
        <SubcategoryDropdown
          category={selectedCategory}
          onSubcategoryChange={handleSubcategoryChange}
        />
      )}
      {selectedSubcategory && (
        <p>You have selected subcategory {selectedSubcategory}.</p>
      )}
    </div>
  );
};

export default CategorySubcategoryDropdown;