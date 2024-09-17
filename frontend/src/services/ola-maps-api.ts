import axios from 'axios';

const apiKey = process.env.REACT_APP_OLA_MAPS_API_KEY;
const vectorMapBaseURL = process.env.REACT_APP_OLA_MAPS_VECTOR_MAP_BASE_URL;

const apiService = axios.create({
    baseURL: vectorMapBaseURL,
    timeout: 5000, 
});

export const transformRequest = (url: string, resourceType: string | undefined) => {
    if (!apiKey) {
        console.error("API Key is missing!");
        return { url, resourceType };
    }
    
    if (url.includes("?")) {
        url = `${url}&api_key=${apiKey}`;
    } else {
        url = `${url}?api_key=${apiKey}`;
    }

    return { url, resourceType };
};

export default apiService;