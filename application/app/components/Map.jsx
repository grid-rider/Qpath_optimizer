import React, { useState } from "react";
//import { Avatar, AvatarBadge } from "@chakra-ui/react";
import GoogleMapReact from "google-map-react";

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
  usingCurser,
  setStartpoint,
  setEndpoint,
}) {
  const [startMarker, setStartMarker] = useState(null);
  const [midpointMarkers, setMidpointMarkers] = useState([]);
  const [endMarker, setEndMarker] = useState(null);
  const [pathLine, setPathLine] = useState([]); // [startpoint, ...midpoints, endpoint
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
        position: startpoint,
        map,
        title: "Start",
        icon: {
          url: "/startpoint.svg",
        },
      })
    );
    setMidpointMarkers(
      midpoints.map((midpoint) => {
        return new maps.Marker({
          position: midpoint,
          map,
          title: "Midpoint",
          icon: {
            url: "/midpoint.svg",
          },
        });
      })
    );
    setEndMarker(
      new maps.Marker({
        position: endpoint,
        map,
        title: "End",
        icon: {
          url: "/endpoint.svg",
        },
      })
    );
    setPathLine(
      new maps.Polyline({
        path: [startpoint, ...midpoints, endpoint],
        geodesic: true,
        strokeColor: "#696969",
        strokeOpacity: 1.0,
        strokeWeight: 3,
        map: map,
      })
    );
    console.log("map loaded");
  };

  const _onClick = ({ lat, lng }) => {
    if (usingCurser) return;
    if (choosingStartpoint) {
      setStartpoint({ lat, lng });
      startMarker.setPosition({ lat, lng });
      console.log(`startpoint:${lat} ${lng})}`);
      if (endpoint != null)
        pathLine.setPath([{ lat, lng }, ...midpoints, endpoint]);
    } else {
      setEndpoint({ lat, lng });
      endMarker.setPosition({ lat, lng });
      console.log(`endpoint:${lat} ${lng})}`);
      if (startpoint != null)
        pathLine.setPath([startpoint, ...midpoints, { lat, lng }]);
    }
  };

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
      ></GoogleMapReact>
    </div>
  );
}
