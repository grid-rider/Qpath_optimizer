"use client";
import React, { useState } from "react";
import { Map } from "./components/Map";
import { ControlPannel } from "./components/ControlPannel";
import { Sidebar } from "./components/Sidebar";

export default function Home() {
  const [startpoint, setStartpoint] = useState();

  // midpoints structured as follows: [{ lat: 40.7431, lng: -73.971321 }, { lat: 40.7531, lng: -73.961321 },]

  const [midpoints, setMidpoints] = useState([]); //default value for testing. Remove when done

  const [endpoint, setEndpoint] = useState();
  const [choosingStartpoint, setChoosingStartpoint] = useState(true);
  const [usingCurser, setUsingCurser] = useState(false);
  const [path, setPath] =useState([])

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
        path={path}
      />
      <ControlPannel
        setStartpoint={setStartpoint}
        setEndpoint={setEndpoint}
        setChoosingStartpoint={setChoosingStartpoint}
        setUsingCurser={setUsingCurser}
      />
      <Sidebar 
        startpoint={startpoint}
        endpoint={endpoint}
        midpoints={midpoints}
        path={path}
        setPath={setPath}
        setStartpoint={setStartpoint}
        setEndpoint={setEndpoint}
      />
    </main>
  );
}
