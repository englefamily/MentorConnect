import React from 'react';
import { FaStar, FaStarHalfAlt, FaRegStar } from 'react-icons/fa';

function Rating({ value }) {
  const renderStars = () => {
    const stars = [];
    const fullStars = Math.floor(value);
    const hasHalfStar = value % 1 !== 0;

    for (let i = 0; i < fullStars; i++) {
      stars.push(<FaStar key={i} style={{color: 'rgb(245, 199, 91)'}} />);
    }

    if (hasHalfStar) {
      stars.push(<FaStarHalfAlt key={fullStars} style={{color: 'rgb(245, 199, 91)'}}/>);
    }

    while (stars.length < 5) {
      stars.push(<FaRegStar key={stars.length} style={{color: 'rgb(245, 199, 91)'}} />);
    }

    return stars.reverse();
  };

  return <div>{renderStars()}</div>;
}

export default Rating;
