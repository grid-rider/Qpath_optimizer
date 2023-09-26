"use client";
import React, { useState } from "react";
import { CircularProgress } from "@chakra-ui/progress";
import { Map } from "./components/Map";

export default function Home() {
  const [startpoint, setStartpoint] = useState({
    lat: 40.7731,
    lng: -73.991321,
  });
  const [midpoints, setMidpoints] = useState([]);
  const [endpoint, setEndpoint] = useState({ lat: 40.7331, lng: -73.971321 });
  return (
    <main>
      <h1>Qpath Optimizer</h1>
      <CircularProgress isIndeterminate color="green.300" />
      <Map startpoint={startpoint} midpoints={midpoints} endpoint={endpoint} />
    </main>
  );
}
