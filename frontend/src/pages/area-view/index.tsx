import React, { useState, useEffect } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';
import { FlyToInterpolator } from '@deck.gl/core';
import { ScatterplotLayer, PathLayer } from '@deck.gl/layers';
import { fetchInterpolatedPoints, fetchStreetBasicInfo } from "../../services/be-api";
import './Map.css';
import Loading from "../../components/loading/Loading";
import Sidebar from "../../components/sidebar/Sidebar";
import { StreetBasicInfo } from '../../types/street';

const mapStyle = process.env.REACT_APP_MAP_STYLE;

const Map: React.FC = () => {
  const [viewState, setViewState] = useState<ViewState>({
    longitude: 0,
    latitude: 0,
    zoom: 1,
    pitch: 0,
    bearing: 0,
    transitionDuration: 0,
  });

  const [streetPoints, setStreetPoints] = useState<number[][]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);
  const [selectedStreetInfo, setSelectedStreetInfo] = useState<StreetBasicInfo | null>(null);
  const [streetPathData, setStreetPathData] = useState<StreetBasicInfo | null>(null); // New state

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

    const fetchData = async () => {
      try {
        const streetData = await fetchStreetBasicInfo(3);
        const points = await fetchInterpolatedPoints(
          [streetData.coordinates.start.longitude, streetData.coordinates.start.latitude],
          [streetData.coordinates.end.longitude, streetData.coordinates.end.latitude],
          streetData.total_lights
        );
        setStreetPathData(streetData);
        setStreetPoints(points);
        setLoading(false);
      } catch (err) {
        setError("Failed to fetch street points");
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const pathLayer = streetPathData
    ? new PathLayer({
        id: "path-layer",
        data: [streetPathData],
        getPath: (d) => [
          [d.coordinates.start.longitude, d.coordinates.start.latitude],
          [d.coordinates.end.longitude, d.coordinates.end.latitude],
        ],
        getWidth: 5,
        getColor: [0, 128, 255],
        pickable: true,
        onClick: (info) => {
          if (info.object) {
            setSelectedStreetInfo(info.object); 
            setIsSidebarOpen(true);
          }
        },
      })
    : null;

  const scatterplotLayer = new ScatterplotLayer({
    id: "scatterplot-layer",
    data: streetPoints.map((point) => ({ position: point, size: 1 })),
    getPosition: (d) => d.position,
    getRadius: (d) => d.size,
    getColor: [255, 0, 0],
    radiusMinPixels: 5,
  });

  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
    setSelectedStreetInfo(null);
  };

  const handleViewDetails = () => {
    console.log("Navigating to detailed street view...");
  };

  return loading ? (
    <Loading />
  ) : error ? (
    <div>{error}</div>
  ) : (
    <div className="map-container" style={{ position: "relative" }}>
      <DeckGL
        viewState={viewState}
        onViewStateChange={(nextViewState) =>
          setViewState(nextViewState.viewState as ViewState)
        }
        controller={true}
        layers={[pathLayer, scatterplotLayer].filter(Boolean)}
      >
        <StaticMap
          mapLib={maplibregl as any}
          mapStyle={mapStyle}
          transformRequest={transformRequest}
        />
      </DeckGL>

      <Sidebar
        isOpen={isSidebarOpen}
        onClose={handleCloseSidebar}
        streetInfo={selectedStreetInfo}
        onViewDetails={handleViewDetails}
      />
    </div>
  );
};

export default Map;
