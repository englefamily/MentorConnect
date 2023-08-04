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
  try {
    if (to === "student") {
      if (method === "POST") {
        const response = await api.post(HOST_URL + "api/student/", data);
        return response;
      } else if (method === "GET") {
        const response = await api.get(HOST_URL + `api/student/?${data}`);
        return response;
      } else if (method === "PUT") {
        const response = await api.put(HOST_URL + `api/student/`, data);
        return response;
      }
    } else if (to === "mentor") {
      if (method === "POST") {
        const mentor_data = { ...data };
        const response = await api.post(HOST_URL + "api/mentor/", mentor_data);
        return response;
      } else if (method === "GET") {
        const response = await api.get(HOST_URL + `api/mentor/?${data}`);
        return response;
      } else if (method === "PUT") {
        const response = await api.put(HOST_URL + `api/mentor/`, data);
        return response;
      }
    } else if (to === "topic") {
      if (method === "GET") {
        const response = await api.get(HOST_URL + "api/topic/");
        return response;
      }
    } else if (to === "chat") {
      if (method === 'GET') {
        const response = await api.get(HOST_URL + `text-chat/api/chat/${data}`);
        return response;
      }
      if (method === 'POST') {
        const response = await api.post(HOST_URL + `text-chat/api/chat/`, data);
        return response;
      }
    } else if (to === "get-chats") {
      if (method === 'GET') {
        const response = await api.get(HOST_URL + `text-chat/api/get-chats/${data}/`);
        return response;
      }
    } else if (to === "get-messages") {
      if (method === 'GET') {
        const response = await api.get(HOST_URL + `text-chat/api/get-messages/${data}/`);
        return response;
      }
    } else if (to === "message") {
      if (method === 'POST') {
        const response = await api.post(HOST_URL + `text-chat/api/message/`, data);
        return response;
      }
    } else if (to === "study_session") {
      if (method === 'POST') {
        const response = await api.post(HOST_URL + `api/study_session/`, data);
        return response;
      } else if (method === 'GET') {
        const response = await api.get(HOST_URL + `api/study_session/?${data}`)
        return response
      } else if (method === 'PUT') {
        const response = await api.put(HOST_URL + `api/study_session/${data.id}/`, data.data)
        return response
      }
    } else if (to === "students_mentor_chats") {
      if (method === 'GET') {
        const response = await api.get(HOST_URL + `api/students_mentor_chats/${data}/`);
        return response;
      }
    } else if (to === "token") {
      if (method === "POST") {
        const response = await api.post(HOST_URL + "api/token/", data);
        return response;
      }
    } else if (to === "refresh-token") {
      if (method === "POST") {
        const response = await api.post(HOST_URL + "api/token/refresh/", data);
        return response;
      }
    }

    // Handle the case when "to" or "method" doesn't match the expected values
    throw new Error("Invalid parameters");
  } catch (error) {
    console.log("🚀 ~ file: functions.js:91 ~ fetch_api ~ error:", error);
    return error;
  }
}

export const transformData = (data) => {
  const transformedData = {};

  data.forEach((item) => {
    const { field, name, id } = item;

    if (!transformedData[field]) {
      transformedData[field] = [];
    }

    transformedData[field].push({ name: name, value: id });
  });

  return transformedData;
};
