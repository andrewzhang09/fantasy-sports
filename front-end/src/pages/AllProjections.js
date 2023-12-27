// Import necessary dependencies
import React, { useEffect, useState } from 'react';
import { useParams, useLocation } from 'react-router-dom';

const AllProjections = () => {
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const timeInterval = queryParams.get('timeInterval');
  const teamId = queryParams.get('teamId');

  // State to store the fetched data
  const [matchupMap, setMatchupMap] = useState({});
  const [timeIntervals, setTimeIntervals] = useState({});

  useEffect(() => {
    const fetchData = async () => {
        try {
            const response = await fetch(`http://127.0.0.1:5000/all-projections?teamId=${teamId}&timeInterval=${timeInterval}`);
            const data = await response.json();
            const matchupMap = data.matchup_map;
            const timeIntervals = data.time_intervals;
            setMatchupMap(matchupMap);
            setTimeIntervals(timeIntervals);
            console.log(matchupMap);
            console.log(timeIntervals);
        } catch (error) {
            console.error('Error fetching data:', error);
        }
    };

    fetchData();
    
    }, [teamId, timeInterval]);

  // Render your component with the fetched data
  return (
    <div>
      <h1>Projections for {teamId} Against All Teams given Time Interval: {timeInterval}</h1>
    </div>
  );
};

export default AllProjections;

