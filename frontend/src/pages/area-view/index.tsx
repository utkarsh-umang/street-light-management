import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';
import { FlyToInterpolator } from '@deck.gl/core';
import { ScatterplotLayer, PathLayer } from '@deck.gl/layers';
import './Map.css';

const interpolatePoints = (start: number[], end: number[], numPoints: number) => {
  const latStep = (end[1] - start[1]) / (numPoints - 1);
  const lonStep = (end[0] - start[0]) / (numPoints - 1);
  
  const points = [];
  for (let i = 0; i < numPoints; i++) {
    const lat = start[1] + latStep * i;
    const lon = start[0] + lonStep * i;
    points.push([lon, lat]);
  }
  return points;
};

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

  const startCoord = [77.0521098621715, 28.596682537282675];
  const endCoord = [77.0544098621715, 28.595122537282675];
  
  const streetPoints = interpolatePoints(startCoord, endCoord, 10);

  const pathLayer = new PathLayer({
    id: 'path-layer',
    data: [streetPoints],
    getPath: d => d,
    getWidth: 1,
    getColor: [0, 128, 255], 
    pickable: true, 
    onClick: () => alert('Street clicked!'),
  });

  const scatterplotLayer = new ScatterplotLayer({
    id: 'scatterplot-layer',
    data: streetPoints.map(point => ({ position: point, size: 1 })),
    getPosition: d => d.position,
    getRadius: d => d.size,
    getColor: [255, 0, 0],
    radiusMinPixels: 5,
  });

  return (
    <div className="map-container">
      <DeckGL
        viewState={viewState}
        onViewStateChange={(nextViewState) => setViewState(nextViewState.viewState as ViewState)}
        controller={true}
        layers={[pathLayer, scatterplotLayer]}
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
