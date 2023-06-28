import axios from "axios";
import { HOST_URL } from "./avariables";

export async function fetch_api(to, method, data) {
  if (to === "student") {
    if (method === "POST") {
      const response = await axios.post(HOST_URL + "api/student/", data);
      return response;
    }
  } else if (to === "mentor") {
    console.log(data)
    const mentor_data = {...data}
    if (method === "POST") {
      mentor_data.experience_with = mentor_data.experience_with.map((item) => {
        return item.value;
      });
      mentor_data.study_cities = mentor_data.study_cities.map((item) => {
        return item.value;
      });
      console.log(mentor_data)
      const response = await axios.post(HOST_URL + "api/mentor/", mentor_data);
      return response;
    }
  } else if (to === "topic") {
    if (method === "GET") {
      const response = await axios.get(HOST_URL + "api/topic/");
      console.log(response.data.topic);
      return response;
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
