"use client";
import React, { useState } from "react";
import { Map } from "./components/Map";
import { ControlPannel } from "./components/ControlPannel";
import { Sidebar } from "./components/Sidebar";

export default function Home() {
  const [startpoint, setStartpoint] = useState();
  const [midpoints, setMidpoints] = useState([
    { lat: 40.7431, lng: -73.971321 },
    { lat: 40.7531, lng: -73.961321 },
  ]); //default value for testing. Remove when done
  const [endpoint, setEndpoint] = useState();
  const [choosingStartpoint, setChoosingStartpoint] = useState(true);
  const [usingCurser, setUsingCurser] = useState(false);

  return (
    <main>
      <Map
        startpoint={startpoint}
        midpoints={midpoints}
        endpoint={endpoint}
        setStartpoint={setStartpoint}
        setEndpoint={setEndpoint}
        choosingStartpoint={choosingStartpoint}
        usingCurser={usingCurser}
      />
      <ControlPannel
        setStartpoint={setStartpoint}
        setEndpoint={setEndpoint}
        setChoosingStartpoint={setChoosingStartpoint}
        setUsingCurser={setUsingCurser}
      />
      <Sidebar />
    </main>
  );
}
