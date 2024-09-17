import React from 'react';
import './home.css';

const Home: React.FC = () => {
  return (
      <div className="home-container">
          <header className="home-header">
              <h1>Street Light Management Dashboard</h1>
              <p className="home-subtitle">Efficiently manage and maintain street lights within your Nigam</p>
          </header>

          <section className="home-card">
              <h2 className="section-title">Overview</h2>
              <p className="section-content">
                  The management of street lights within various Nigams presents significant challenges, particularly in terms of maintenance and cost analysis. With numerous street lights installed across different areas, it becomes crucial to have an efficient system that enables Nigams to monitor and manage these assets effectively.
              </p>
          </section>

          <section className="home-card">
              <h2 className="section-title">Objectives</h2>
              <ul className="section-list">
                  <li>Map View: Geographical representation with each street light marked by a pin.</li>
                  <li>Detailed Information for each light: Installation date, bulb manufacturer, warranty, and cost details.</li>
                  <li>Maintenance history and issue reports for each street light.</li>
              </ul>
          </section>

          <section className="home-card">
              <h2 className="section-title">Benefits</h2>
              <ul className="section-list">
                  <li>Streamline the management of street lights.</li>
                  <li>Enhance maintenance efficiency and reduce costs.</li>
                  <li>Improve budgeting and decision-making for infrastructure investments.</li>
              </ul>
          </section>
      </div>
  );
};

export default Home;
