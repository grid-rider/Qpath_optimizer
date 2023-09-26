import React from "react";
import { Avatar, AvatarBadge } from "@chakra-ui/react";
import GoogleMapReact from "google-map-react";
import Polyline from "google-map-react";

require("dotenv").config();

/**
 * Populates the provide state variables with the startpoint, midpoints, and endpoint
 * @param {object:{lat,lng}} startpoint
 * @param {array:[{lat,lng},...,{lat,lng}]} midpoints
 * @param {object:{lat,lng}} endpoint
 * @param {function} setStartpoint
 * @param {function} setMidpoints
 * @param {function} setEndpoint
 * @returns
 */
export function Map({
  startpoint,
  endpoint,
  midpoints,
  setStartpoint,
  setEndpoint,
  setMidpoints,
}) {
  startpoint = { lat: 40.7731, lng: -73.991321 }; // should get from user input
  midpoints = [
    { lat: 40.7631, lng: -73.991321 },
    { lat: 40.7531, lng: -73.991321 },
    { lat: 40.7431, lng: -73.991321 },
  ]; // should get from api call to backend
  endpoint = { lat: 40.7331, lng: -73.971321 }; // should get from user input

  const defaultGeoLoc = {
    center: {
      lat: 40.7431,
      lng: -73.991321,
    },
    zoom: 13,
  };
  const handleApiLoaded = (map, maps) => {
    // use map and maps objects
  };

  // Create an array of coordinates for the polyline
  const polylineCoordinates = [startpoint, ...midpoints, endpoint];

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <GoogleMapReact
        bootstrapURLKeys={{ key: process.env.GOOGLE_MAP_API_KEY }}
        defaultCenter={defaultGeoLoc.center}
        defaultZoom={defaultGeoLoc.zoom}
        yesIWantToUseGoogleMapApiInternals
        onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)}
      >
        <Avatar lat={startpoint.lat} lng={startpoint.lng}>
          <AvatarBadge boxSize="24px" bg="green.500" />
        </Avatar>
        {midpoints.map((midpoint, index) => (
          <Avatar key={index} lat={midpoint.lat} lng={midpoint.lng}>
            <AvatarBadge boxSize="16px" bg="#696969" />
          </Avatar>
        ))}
        <Avatar lat={endpoint.lat} lng={endpoint.lng}>
          <AvatarBadge boxSize="24px" bg="#7C5CDA" />
        </Avatar>

        {/* Add a Polyline component to draw lines (currently not working)*/}
        {/* <Polyline path={polylineCoordinates} /> */}
      </GoogleMapReact>
    </div>
  );
}
