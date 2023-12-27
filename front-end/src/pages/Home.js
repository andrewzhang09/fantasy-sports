import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import HomeForm from '../components/homeForm';
import '../styles/Home.css';


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

    const navigate = useNavigate();

    const defaultTimeInterval = '2024_last_30';

    // FOR TEAM SELECTION
    const handleTeamChange = (teamId) => {
      console.log(teamId);
      setSelectedTeam(teamId);
    }

    // FOR FORM
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
    
    // BUTTON CLICK HANDLERS
    const handleAllProjectionsClick = (teamId, timeInterval) => {
      const url = `/all-projections?teamId=${teamId}&timeInterval=${timeInterval}`;
      navigate(url);
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
              <button onClick={() => handleAllProjectionsClick(selectedTeam, defaultTimeInterval)}>
                All Projections
              </button>
              <button onClick={() => window.location.href = 'https://dummy-url-2.com'}>Project Current Matchup</button>
              <button onClick={() => window.location.href = 'https://dummy-url-3.com'}>Project Trade</button>
            </>
          )}
        </div>
      </div>
    );
};

export default Home;