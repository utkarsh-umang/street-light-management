import React from "react";
import {
  ChevronRight,
  AlertCircle,
  Zap,
  Lightbulb,
  BarChart2,
} from "lucide-react";
import { StreetBasicInfo } from "../../types/street";
import "./Sidebar.css";

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
  streetInfo: StreetBasicInfo | null;
  onViewDetails: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  isOpen,
  onClose,
  streetInfo,
  onViewDetails,
}) => {
  if (!isOpen || !streetInfo) return null;

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>{streetInfo.street_name}</h2>
        <button onClick={onClose}>
          <ChevronRight className="icon" />
        </button>
      </div>

      <div className="sidebar-content">
        <div className="section">
          <div className="section-title">
            <Lightbulb />
            Ward
          </div>
          <div className="section-value">{streetInfo.ward || "N/A"}</div>
        </div>

        <div className="section">
          <div className="section-title">
            <Lightbulb />
            Total Lights
          </div>
          <div className="section-value">{streetInfo.total_lights ?? "N/A"}</div>
        </div>

        <div className="section">
          <div className="section-title">
            <Zap />
            Power Usage
          </div>
          <div className="section-value">
            {streetInfo.total_power_consumption?.toFixed(1) ?? "0.0"} kWh
          </div>
        </div>

        <div className="section">
          <div className="section-title">
            <BarChart2 />
            Operational Status
          </div>
          <div className="operational-status">
            {Object.entries(streetInfo.operational_summary || {}).map(
              ([status, count]) => (
                <div key={status}>
                  <span>{status}</span>
                  <span>{count}</span>
                </div>
              )
            )}
          </div>
        </div>

        <div className="section">
          <div className="section-title">
            <AlertCircle />
            Recent Issues
          </div>
          <div className="section-value">
            {streetInfo.recent_issues ?? 0}
          </div>
        </div>
      </div>

      <div className="sidebar-footer">
        <button onClick={onViewDetails}>See Detailed View</button>
      </div>
    </div>
  );
};

export default Sidebar;
