import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';
import { FlyToInterpolator } from '@deck.gl/core';
import { ScatterplotLayer, PathLayer } from '@deck.gl/layers';
import { fetchInterpolatedPoints } from "../../services/be-api";
import './Map.css';
import Loading from "../../components/loading/Loading";

const mapStyle = process.env.REACT_APP_MAP_STYLE;

const Map: React.FC = () => {
  const [viewState, setViewState] = useState<ViewState>({
    longitude: 0,
    latitude: 0,
    zoom: 1,
    pitch: 0,
    bearing: 0,
    transitionDuration: 0
  });

  const [streetPoints, setStreetPoints] = useState<number[][]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

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

    const fetchPoints = async () => {
      try {
        const points = await fetchInterpolatedPoints(
          [77.0521098621715, 28.596682537282675],
          [77.0544098621715, 28.595122537282675], 
          10
        );
        setStreetPoints(points);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch street points");
        setLoading(false);
      }
    };

    fetchPoints();
  }, []);

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

  return ( loading ? 
    <Loading /> : error ? 
    <div>{error}</div> :
    <div className="map-container">
      <DeckGL
        viewState={viewState}
        onViewStateChange={(nextViewState) => setViewState(nextViewState.viewState as ViewState)}
        controller={true}
        layers={[pathLayer, scatterplotLayer]}
      >
        <StaticMap
          mapLib={maplibregl as any}
          mapStyle={mapStyle}
          transformRequest={transformRequest}
        />
      </DeckGL>
    </div>
  );
};

export default Map;
