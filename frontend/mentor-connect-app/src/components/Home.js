import React, { useEffect } from 'react'

function Home() {
  useEffect(() => {

  window.location.replace('mentors')
}, [])
  return (
    <div>
      <h1>בית</h1>
    </div>
  )
}

export default Home
