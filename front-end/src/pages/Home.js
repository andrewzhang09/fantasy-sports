import React, { useState } from 'react';
import HomeForm from '../components/homeForm';
import '../styles/Home.css';

// TODO: make default values in field semi transparent

const Home = () => {
    const [formData, setFormData] = useState({
        league_id: '',
        year: '',
        swid: '',
        espn_s2: '',
    })

    const [formSubmitted, setFormSubmitted] = useState(false);

    const [teams, setTeams] = useState({});

    const [selectedTeam, setSelectedTeam] = useState(null);

    // TODO: resubmitting form should reset the options
    const handleTeamChange = (teamId) => {
      console.log(teamId);
      setSelectedTeam(teamId);
    }

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({...formData, [name]: value });
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const response = await fetch('http://127.0.0.1:5000/submitHomeForm', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData),
            });

            const result = await response.json();
            console.log('Server response:', result);

            // teams are under the 'teams' key in the response
            if (result.teams) {
                setTeams(result.teams);
                setFormSubmitted(true);
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
      <div>
        <div className="centered-components">
          <HomeForm 
            formData={formData}
            handleInputChange={handleInputChange}
            handleSubmit={handleSubmit}
          />
        </div>
        <div className="centered-components">
          {formSubmitted && (
            <>
              <h2>Select a Team:</h2>
              {Object.keys(teams).map((teamKey) => {
                const team = teams[teamKey];
                return (
                  <label>
                    <input
                      type="radio"
                      name="selectedTeam"
                      value={team.team_id}
                      checked={selectedTeam === team.team_id}
                      onChange={() => handleTeamChange(team.team_id)}
                    />
                    {team.team_name}
                  </label>
                );
              })}
            </>
          )}
        </div>
        <div className="button-container">
          {selectedTeam && (
            <>
              <button onClick={() => window.location.href = 'https://dummy-url-1.com'}>All Projections</button>
              <button onClick={() => window.location.href = 'https://dummy-url-2.com'}>Project Current Matchup</button>
              <button onClick={() => window.location.href = 'https://dummy-url-3.com'}>Project Trade</button>
            </>
          )}
        </div>
      </div>
    );
};

export default Home;