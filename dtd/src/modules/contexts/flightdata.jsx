import React, { createContext, useState, useEffect } from 'react';

import dtd_report from '../../../../data_processing/data/output/reports/dtd_report.json';

export const FlightDataContext = createContext();

export const FlightDataProvider = ({ children }) => {
    const [flightDataReport, setFlightDataReport] = useState(dtd_report);
    // const [airportVisits, setAirportVisits] = useState([]);

    // useEffect(() => {
    //     d3.csv("./airport_visits.csv", function(data) {
    //         setAirportVisits(data);
    //     });
    // }, [])

    const value = {
        flightDataReport,
        // airportVisits,
    };

    return (
        <FlightDataContext.Provider value={value}>
            {children}
        </FlightDataContext.Provider>
    );
};