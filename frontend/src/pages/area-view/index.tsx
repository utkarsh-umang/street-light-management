import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';
import { FlyToInterpolator } from '@deck.gl/core';
import './Map.css';

const Map: React.FC = () => {
  const [viewState, setViewState] = useState<ViewState>({
    longitude: 0,
    latitude: 0,
    zoom: 1,
    pitch: 0,
    bearing: 0,
    transitionDuration: 0
  });

  useEffect(() => {
    setTimeout(() => {
      setViewState({
        longitude: 77.05380098621715,
        latitude: 28.596382537282675,
        zoom: 17,
        pitch: 0,
        bearing: 0,
        transitionDuration: 5000,
        transitionInterpolator: new FlyToInterpolator(),
      });
    }, 2000);
  }, []);

  return (
    <div className="map-container">
      <DeckGL
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
