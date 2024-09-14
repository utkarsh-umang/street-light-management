import React from 'react';
import './Header.css';

const Header: React.FC = () => {
    return (
        <header className="header">
            <div className="app-name">
                <a href="/">StreetSmart</a>
            </div>
            <nav>
                <ul className="nav-list">
                    <li><a href="/map">Map</a></li>
                    <li><a href="/dashboard">Dashboard</a></li>
                </ul>
            </nav>
        </header>
    );
};

export default Header;