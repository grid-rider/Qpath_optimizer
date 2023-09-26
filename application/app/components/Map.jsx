import React from "react";
import { Avatar, AvatarBadge } from "@chakra-ui/react";
import GoogleMapReact from "google-map-react";
//import Polyline from "google-map-react";

require("dotenv").config();

/**
 * Populates the provided state variables with the startpoint, midpoints, and endpoint
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
  // Initial values for testing. TODO: Replace with user input or API data
  startpoint = { lat: 40.7731, lng: -73.991321 };
  midpoints = [
    { lat: 40.7631, lng: -73.991321 },
    { lat: 40.7531, lng: -73.991321 },
    { lat: 40.7431, lng: -73.991321 },
  ];
  endpoint = { lat: 40.7331, lng: -73.971321 };

  const handleApiLoaded = (map, maps) => {
    // Use map and maps objects
  };

  // Set the default location of the map to be NYC
  const defaultGeoLoc = {
    center: {
      lat: 40.7431,
      lng: -73.991321,
    },
    zoom: 13,
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
        {/* Display the startpoint as an Avatar on the map */}
        <Avatar lat={startpoint.lat} lng={startpoint.lng}>
          <AvatarBadge boxSize="24px" bg="green.500" />
        </Avatar>

        {/* Display midpoints as Avatars on the map */}
        {midpoints.map((midpoint, index) => (
          <Avatar key={index} lat={midpoint.lat} lng={midpoint.lng}>
            <AvatarBadge boxSize="16px" bg="#696969" />
          </Avatar>
        ))}

        {/* Display the endpoint as an Avatar on the map */}
        <Avatar lat={endpoint.lat} lng={endpoint.lng}>
          <AvatarBadge boxSize="24px" bg="#7C5CDA" />
        </Avatar>

        {/* Add a Polyline component to draw lines (currently not working) */}
        {/* <Polyline path={polylineCoordinates} /> */}
      </GoogleMapReact>
    </div>
  );
}
