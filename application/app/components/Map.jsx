import React, { useState } from "react";
import { Avatar, AvatarBadge } from "@chakra-ui/react";
import GoogleMapReact from "google-map-react";
import { m } from "framer-motion";
//import Polyline from "google-map-react";

require("dotenv").config();

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

/**
 * Populates the provided state variable: startpoint and endpoint.
 * The startpoint, midpoints, and endpoint are objects with lat and lng properties.
 * The choosingStartpoint is a boolean that is true if the user is currently
 * choosing the startpoint and false if the user is currently choosing the endpoint.
 * @param {object:{lat,lng}} startpoint
 * @param {array:[{lat,lng},...,{lat,lng}]} midpoints
 * @param {object:{lat,lng}} endpoint
 * @param {boolean} choosingStartpoint
 * @param {function} setStartpoint
 * @param {function} setEndpoint
 * @returns
 */
export function Map({
  startpoint,
  midpoints,
  endpoint,
  choosingStartpoint,
  setStartpoint,
  setEndpoint,
}) {
  const [startMarker, setStartMarker] = useState(null);
  const [midpointMarkers, setMidpointMarkers] = useState([]);
  const [endMarker, setEndMarker] = useState(null);

  // Set the default location of the map to be NYC
  const defaultGeoLoc = {
    center: {
      lat: 40.7431,
      lng: -73.991321,
    },
    zoom: 13,
  };

  const handleApiLoaded = (map, maps) => {
    setStartMarker(
      new maps.Marker({
        map,
        title: "Start",
      })
    );
    setMidpointMarkers(
      new maps.Marker({
        map,
        title: "Midpoint",
      })
    );
    setEndMarker(
      new maps.Marker({
        map,
        title: "End",
      })
    );
  };

  const _onClick = ({ lat, lng }) => {
    if (choosingStartpoint) {
      setStartpoint({ lat, lng });
      startMarker.setPosition({ lat, lng });
      console.log(`startpoint:${startpoint.lat} ${startpoint.lng})}`);
    } else {
      setEndpoint({ lat, lng });
      endMarker.setPosition({ lat, lng });
      console.log(`endpoint:${endpoint.lat} ${endpoint.lng})}`);
    }
  };

  // Create an array of coordinates for the polyline
  const polylineCoordinates = [startpoint, ...midpoints, endpoint];

  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <GoogleMapReact
        bootstrapURLKeys={{
          key: GOOGLE_MAPS_API_KEY,
        }}
        defaultCenter={defaultGeoLoc.center}
        defaultZoom={defaultGeoLoc.zoom}
        yesIWantToUseGoogleMapApiInternals
        onGoogleApiLoaded={({ map, maps }) => handleApiLoaded(map, maps)}
        onClick={_onClick}
      >
        {/* Add a Polyline component to draw lines (currently not working) */}
        {/* <Polyline path={polylineCoordinates} /> */}
      </GoogleMapReact>
    </div>
  );
}
