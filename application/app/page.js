"use client";
import React, { useState } from "react";
import { Map } from "./components/Map";

export default function Home() {
  const [startpoint, setStartpoint] = useState();
  const [midpoints, setMidpoints] = useState([
    { lat: 40.7431, lng: -73.971321 },
    { lat: 40.7531, lng: -73.961321 },
  ]); //default value for testing. Remove when done
  const [endpoint, setEndpoint] = useState({
    lat: 40.7431,
    lng: -73.991321,
  }); //default value for testing. Remove when done
  const [choosingStartpoint, setChoosingStartpoint] = useState(true);
  return (
    <main>
      <h1>Qpath Optimizer</h1>
      <Map
        startpoint={startpoint}
        midpoints={midpoints}
        endpoint={endpoint}
        setStartpoint={setStartpoint}
        setEndpoint={setEndpoint}
        setMidpoints={setMidpoints}
        choosingStartpoint={choosingStartpoint}
        setChoosingStartpoint={setChoosingStartpoint}
      />
    </main>
  );
}
