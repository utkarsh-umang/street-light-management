import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';
import { ScatterplotLayer } from '@deck.gl/layers';
import { FlyToInterpolator } from '@deck.gl/core';


const Map: React.FC = () => {
  const [viewState, setViewState] = useState<ViewState>({
    longitude: 0,
    latitude: 0,
    zoom: 1,
    pitch: 0,
    bearing: 0,
    transitionDuration: 0
  });

  // This layer gives a red dot at the center of the map
  // const layer = new ScatterplotLayer({
  //   id: 'scatterplot-layer',
  //   data: [{ position: [77.057919, 28.598051], size: 100 }],
  //   getPosition: d => d.position,
  //   getRadius: d => d.size,
  //   getColor: [255, 0, 0]
  // }); 

  useEffect(() => {
    setTimeout(() => {
      setViewState({
        longitude: 77.057919,
        latitude: 28.598051,
        zoom: 15,
        pitch: 0,
        bearing: 0,
        transitionDuration: 2000,
        transitionInterpolator: new FlyToInterpolator(),
      });
    }, 2000);
  }, []);

  return (
    <div>
      <DeckGL
        style={{ width: "100vw", height: "100vh", overflow: "hidden" }}
        viewState={viewState}
        onViewStateChange={(nextViewState) => setViewState(nextViewState.viewState as ViewState)}
        controller={true}
        layers={[]}
      >
        <StaticMap
          mapLib={maplibregl as any}
          mapStyle="https://api.olamaps.io/tiles/vector/v1/styles/default-light-standard/style.json"
          transformRequest={transformRequest}
        />
      </DeckGL>
    </div>
  );
};

export default Map;
