import React, { useState } from 'react';
import '../styles/Home.css';

const HomeForm = ({ formData, handleInputChange, handleSubmit }) => {
    return (
        <>
          <h1>My App</h1>
          <form onSubmit={handleSubmit}>
            <div>
                <label>
                League ID:
                <input
                    type="text"
                    name="league_id"
                    value={formData.league_id}
                    onChange={handleInputChange}
                />
                </label>
            </div>
            <br />
            <div>
                <label>
                Year:
                <input
                    type="text"
                    name="year"
                    value={formData.year}
                    onChange={handleInputChange}
                />
                </label>
            </div>
            <br />
            <div>
                <label>
                SWID:
                <input
                    type="text"
                    name="swid"
                    value={formData.swid}
                    onChange={handleInputChange}
                />
                </label>
            </div>
            <br />
            <div>
                <label>
                ESPN S2:  
                <input
                    type="text"
                    name="espn_s2"
                    value={formData.espn_s2}
                    onChange={handleInputChange}
                />
                </label>
            </div>
            <br />
            <button type="submit">Submit</button>
          </form>
        </>
    )
};

export default HomeForm;