import React from 'react';
import './Loading.css'; 

const Loading: React.FC = () => {
    return (
        <div className="loading-container">
            <div className="spinner"></div>
            <p>Awesomeness Loading...</p>
        </div>
    );
};

export default Loading;