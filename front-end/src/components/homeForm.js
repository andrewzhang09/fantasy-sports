import React, { useState } from 'react';

const HomeForm = ({ formData, handleInputChange, handleSubmit }) => {
    return (
        <>
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
        </>
    )
};

export default HomeForm;