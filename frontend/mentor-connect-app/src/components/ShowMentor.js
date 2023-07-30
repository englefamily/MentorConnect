import React from 'react'
import { useParams } from 'react-router-dom'

function ShowMentor() {
const { mentorId } = useParams()

  return (
    <div>
      {mentorId}
    </div>
  )
}

export default ShowMentor
