import axios from "axios";

const BASE_URL = process.env.REACT_APP_BE_URL;

export const fetchInterpolatedPoints = async (startPoint: number[], endPoint: number[], numPoints: number) => {
  try {
    const response = await axios.post(`${BASE_URL}/api/interpolate-points`, {
      start_point: startPoint,
      end_point: endPoint,
      num_points: numPoints,
    });
    return response.data.points;
  } catch (error) {
    console.error("Error fetching interpolated points:", error);
    throw new Error("Failed to fetch points.");
  }
};

export const fetchStreetBasicInfo = async (streetId: number) => {
  try {
    const response = await axios.get(`${BASE_URL}/api/streets/${streetId}/basic`);
    console.log("here", response);
    return response.data;
  } catch (error) {
    console.error("Error fetching street information:", error);
    throw new Error("Failed to fetch street information.");
  }
};