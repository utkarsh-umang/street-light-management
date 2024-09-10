import axios from 'axios';

const apiService = axios.create({
    baseURL: 'https://api.olamaps.io/tiles/vector/v1', // Replace with your API base URL
    timeout: 5000, // Adjust the timeout value as needed
});

const apiKey = process.env.REACT_APP_OLA_MAPS_API_KEY;
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