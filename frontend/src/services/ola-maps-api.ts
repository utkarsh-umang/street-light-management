import axios from 'axios';

const apiService = axios.create({
    baseURL: 'https://api.example.com', // Replace with your API base URL
    timeout: 5000, // Adjust the timeout value as needed
});

export default apiService;