import axios from "axios"
import { HOST_URL } from './avariables'

export function fetch_api(to, method, data) {
  if (to === 'student') {
    if (method === 'POST') {
      return axios.post(HOST_URL + 'api/student/', data)
        .then(response => {
          return response;
        })
        .catch(error => {
          console.log('aaa');
          return error.response.data.error; // Return the string 'eee' instead of throwing an error
        });
    }
  }

  // Handle the case when "to" or "method" doesn't match the expected values
  throw new Error('Invalid parameters');
}
