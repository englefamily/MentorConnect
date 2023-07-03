import axios from "axios";
import { HOST_URL } from "./avariables";
import { useContext } from "react";
import context from "../Context";


const api = axios.create();

// // Add a request interceptor
// api.interceptors.request.use(
//   (config) => {
//     // Modify config if needed (e.g., add headers, authentication token)
//     return config;
//   },
//   (error) => {
//     return Promise.reject(error);
//   }
// );

// // Add a response interceptor
// api.interceptors.response.use(
//   (response) => {
//     // Process successful responses
//     return response;
//   },
//   (error) => {
//     // Handle specific HTTP error codes
//     if (error.response && error.response.status === 401 || error.response.status === 400) {
//       // Handle 401 error (Unauthorized)
//       // Perform any desired action (e.g., handle authentication, redirect user, etc.)
//       console.log('401/400 Error:', error.message);
//       // Return a resolved promise with the error response
//       return Promise.resolve(error.response);
//     }

//     // Return the error to continue propagating it
//     return Promise.reject(error);
//   }
// );



export async function fetch_api(to, method, data) {

  if (to === "student") {
    if (method === "POST") {
      const response = await api.post(HOST_URL + "api/student/", data);
      return response;
    }
  } else if (to === "mentor") {
    console.log(data);
    const mentor_data = { ...data };
    if (method === "POST") {
      mentor_data.experience_with = mentor_data.experience_with.map((item) => {
        return item.value;
      });
      mentor_data.study_cities = mentor_data.study_cities.map((item) => {
        return item.value;
      });
      console.log(mentor_data);
      const response = await api.post(HOST_URL + "api/mentor/", mentor_data);
      return response;
    }
  } else if (to === "topic") {
    if (method === "GET") {
      const response = await api.get(HOST_URL + "api/topic/");
      console.log(response.data.topics);
      return response;
    }
  } else if (to === "token") {
    if (method === 'POST') {
      const response = await api.post(HOST_URL + "api/token/", data)
      return response
    }
  } else if (to === 'refresh-token') {
    if (method === 'POST') {
      const response = await api.post(HOST_URL + 'api/token/refresh/', data)
      return response
    }
  }

  // Handle the case when "to" or "method" doesn't match the expected values
  throw new Error("Invalid parameters");
}

export const transformData = (data) => {
  const transformedData = {};

  data.forEach((item) => {
    const { topic_field, topic_name, id } = item;

    if (!transformedData[topic_name]) {
      transformedData[topic_name] = [];
    }

    transformedData[topic_name].push({ name: topic_field, id: id });
  });

  return transformedData;
};
