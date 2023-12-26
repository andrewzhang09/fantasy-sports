// Import necessary dependencies
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';

const AllProjections = () => {
  // Get the teamId from the URL using useParams
  const { teamId } = useParams();

  // State to store the fetched data
  const [projections, setProjections] = useState([]);

  useEffect(() => {
    // Define the Flask endpoint URL
    const apiUrl = `http://127.0.0.1:5000/all-projections?teamId=${teamId}`;

    // Make the GET request using the fetch API
    fetch(apiUrl)
      .then((response) => response.json())
      .then((data) => {
        // Update the state with the fetched data
        setProjections(data);
      })
      .catch((error) => {
        console.error('Error fetching data:', error);
      });
  }, [teamId]); // Re-run the effect when teamId changes

  // Render your component with the fetched data
  return (
    <div>
      <h1>Projections for Team {teamId}</h1>
      {/* Render the projections data as needed */}
      <ul>
        {projections.map((projection) => (
          <li key={projection.id}>{/* Render projection data here */}</li>
        ))}
      </ul>
    </div>
  );
};

export default AllProjections;

