import React, { useState, useEffect } from "react";
import GoogleMapReact from "google-map-react";

import nyc_pop_data from "../../public/nyc_pop_data";

require("dotenv").config();

const GOOGLE_MAPS_API_KEY = process.env.NEXT_PUBLIC_GOOGLE_MAPS_API_KEY;

const csv = require("jquery-csv");

const POP_DATA = csv.toObjects(nyc_pop_data);

let heatMapData = [];

/**
 * Populates the provided state variable: startpoint and endpoint.
 * The startpoint, midpoints, and endpoint are objects with lat and lng properties.
 * The choosingStartpoint is a boolean that is true if the user is currently
 * choosing the startpoint and false if the user is currently choosing the endpoint.
 * The usingCurser is a boolean that is true if the user is currently using the curser
 * and clicking will not change the startpoint or endpoint.
 * @param {object:{lat,lng}} startpoint
 * @param {array:[{lat,lng},...,{lat,lng}]} midpoints
 * @param {object:{lat,lng}} endpoint
 * @param {array:[{lat,lng},...,{lat,lng}]} path
 * @param {boolean} choosingStartpoint
 * @param {boolean} usingCurser
 * @param {function} setStartpoint
 * @param {function} setEndpoint
 * @param {function} setMidpoints
 * @param {boolean} isHeatmapVisible
 * @returns
 */
export function Map({
  startpoint,
  midpoints,
  endpoint,
  path,
  choosingStartpoint,
  usingCurser,
  setStartpoint,
  setEndpoint,
  setMidpoints,
  isHeatmapVisible,
}) {
  const [startMarker, setStartMarker] = useState(null);
  const [midpointMarkers, setMidpointMarkers] = useState([]);
  const [endMarker, setEndMarker] = useState(null);
  const [pathLine, setPathLine] = useState([]); // [startpoint, ...midpoints, endpoint]
  const [heatMap, setHeatMap] = useState(null);

  // Set the default location of the map to be NYC
  const defaultGeoLoc = {
    center: {
      lat: 40.7431,
      lng: -73.991321,
    },
    zoom: 13,
  };

  //TODO: add a useEffect that updates the pathLine when the midpoints change
  useEffect(() => {
    if (startMarker != null) {
      if (startpoint == null) {
        startMarker.setPosition(null);
        pathLine.setPath([]);
      } else if (startpoint != null) {
        startMarker.setPosition(startpoint);
      }
    }
    if (endMarker != null) {
      if (endpoint == null) {
        endMarker.setPosition(null);
        pathLine.setPath([]);
      } else if (endpoint != null) {
        endMarker.setPosition(endpoint);
      }
    }

    if (midpointMarkers != null) {
      if (midpoints == null) {
        for (let marker of midpointMarkers){
          marker.setPosition(null);
        }
        pathLine.setPath([]);
      } else if (midpoints != null) {

      }
    }
  }, [startpoint, midpoints, endpoint]);

  useEffect(() => {
    if( path != null && midpoints != null && endpoint != null){ //Guard
      console.log("Drawing new path")
      console.log(path)
      if(path.length > 0 ){
          pathLine.setPath(path);
          if(path.length > 1) {
            // setMidpoints(path.slice(1,path.length-2))
            
            // setMidpointMarkers((midpointMarkers) => {
            //   for(let i = 1; i < path.length - 2; i++){
            //     midpointMarkers[i-1].setPosition(path[i]);
            //   }
            // })

          }
      }    
    }
  }, [path]);

  useEffect(() => {
    if (isHeatmapVisible) {
      heatMap?.setData(heatMapData);
    } else {
      heatMap?.setData([]);
    }
  }, [isHeatmapVisible]);

    console.log("Midpoints: " + midpoints)

  async function getHeatMapData(map, maps) {
    const { HeatmapLayer } = await google.maps.importLibrary("visualization");
    for (let i = 0; i < POP_DATA.length; i++) {
      let lat = Number(POP_DATA[i].latitude);
      let lng = Number(POP_DATA[i].longitude);
      let totalPop = Number(
        POP_DATA[i].totalPop.slice(0, POP_DATA[i].totalPop.length - 1)
      );
      let entry = {
        location: new maps.LatLng(lat, lng),
        weight: totalPop,
      };
      heatMapData.push(entry);
    }
    setHeatMap(
      new HeatmapLayer({
        data: heatMapData,
        map: map,
      })
    );
  }

  const handleApiLoaded = (map, maps) => {
    getHeatMapData(map, maps);

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

    setMidpointMarkers([    
      new maps.Marker({
          position: null,
          map,
          title: "Midpoint",
          icon: {
            url: "/midpoint.svg",
          },
        }),
        new maps.Marker({
          position: null,
          map,
          title: "Midpoint",
          icon: {
            url: "/midpoint.svg",
          },
        }),
        new maps.Marker({
          position: null,
          map,
          title: "Midpoint",
          icon: {
            url: "/midpoint.svg",
          },
        }),
        new maps.Marker({
          position: null,
          map,
          title: "Midpoint",
          icon: {
            url: "/midpoint.svg",
          },
        })
      ]
    
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
    } else {
      setEndpoint({ lat, lng });
      endMarker.setPosition({ lat, lng });
      console.log(`endpoint:${lat} ${lng})}`);
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
        options={{ disableDefaultUI: true }}
      ></GoogleMapReact>
    </div>
  );
}
