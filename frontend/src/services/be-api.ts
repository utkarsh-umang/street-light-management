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