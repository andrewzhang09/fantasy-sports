import React, { useState } from 'react';

const Home = () => {
    const [formData, setFormData] = useState({
        league_id: 1,
        year: 2024,
        swid: '',
        espn_s2: '',
    })

    const [teams, setTeams] = useState([]);

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData({...formData, [name]: value });
    }

    const handleSubmit = async () => {
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
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
        <div>
          <h1>My App</h1>
          <form onSubmit={handleSubmit}>
            <label>
              League ID:
              <input
                type="text"
                name="league_id"
                value={formData.league_id}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              Year:
              <input
                type="text"
                name="year"
                value={formData.year}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              SWID:
              <input
                type="text"
                name="swid"
                value={formData.swid}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <label>
              ESPN S2:
              <input
                type="text"
                name="espn_s2"
                value={formData.espn_s2}
                onChange={handleInputChange}
              />
            </label>
            <br />
            <button type="submit">Submit</button>
          </form>
        </div>
    );
};

export default Home;