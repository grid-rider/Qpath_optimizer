"use client";
import React, { useState } from "react";
import { CircularProgress } from "@chakra-ui/progress";
import { Map } from "./components/Map";

export default function Home() {
  const [startpoint, setStartpoint] = useState();
  const [midpoints, setMidpoints] = useState([]);
  const [endpoint, setEndpoint] = useState();
  const [choosingStartpoint, setChoosingStartpoint] = useState(true);
  return (
    <main>
      <h1>Qpath Optimizer</h1>
      <CircularProgress isIndeterminate color="green.300" />
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
