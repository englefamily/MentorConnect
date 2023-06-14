import axios from "axios"
import { HOST_URL } from './avariables'

export async function fetch_api(to, method, data) {
  if (to === 'student') {
    if (method === 'POST') {
        const response = await axios.post(HOST_URL + 'api/student/', data);
        return response;
      }
  }

  // Handle the case when "to" or "method" doesn't match the expected values
  throw new Error('Invalid parameters');
}

