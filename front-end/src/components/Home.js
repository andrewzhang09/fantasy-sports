import React, { useState } from 'react';
import HomeForm from './homeForm';

// TODO: make default values in field semi transparent

const Home = () => {
    const [formData, setFormData] = useState({
        league_id: '',
        year: '',
        swid: '',
        espn_s2: '',
    })

    const [teams, setTeams] = useState([]);

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
            }
        } catch (error) {
            console.error('Error submitting form:', error);
        }
    };

    return (
      <>
        <HomeForm 
          formData={formData}
          handleInputChange={handleInputChange}
          handleSubmit={handleSubmit}
        />
      </>
    );
};

export default Home;