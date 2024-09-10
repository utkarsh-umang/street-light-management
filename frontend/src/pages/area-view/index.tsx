import React, { useState } from "react";
import DeckGL from "@deck.gl/react";
import StaticMap from "react-map-gl";
import maplibregl from "maplibre-gl";
import { ViewState } from "../../types/viewstate";
import "maplibre-gl/dist/maplibre-gl.css";
import { transformRequest } from '../../services/ola-maps-api';


const Map: React.FC = () => {
  const [viewState, setViewState] = useState<ViewState>({
    longitude: 28.598051,
    latitude: 77.057919,
    zoom: 3,
  });

  return (
    <div>
      <DeckGL
        style={{ width: "100vw", height: "100vh", overflow: "hidden" }}
        viewState={viewState}
        onViewStateChange={() =>
          setViewState(viewState)
        }
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
