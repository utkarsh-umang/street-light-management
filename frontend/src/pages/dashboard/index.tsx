import React, { useEffect, useState } from "react";
import "./Dashboard.css";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  CartesianGrid,
  Legend,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import { fetchStreetDetailedInfo } from "../../services/be-api";

const Dashboard: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [toggleConsumption, setToggleConsumption] = useState<"daily" | "monthly">("daily");

  useEffect(() => {
    const fetchData = async () => {
      const streetData = await fetchStreetDetailedInfo(3);
      setData(streetData);
    };
    fetchData();
  }, []);

  if (!data) return <div>Loading...</div>;

  const energyConsumptionData =
    toggleConsumption === "daily"
      ? data.energy_summary.per_light_consumption.map((light: any) => ({
          lightId: `Light ${light.light_id}`,
          consumption: light.daily_consumption,
        }))
      : data.energy_summary.per_light_consumption.map((light: any) => ({
          lightId: `Light ${light.light_id}`,
          consumption: light.monthly_consumption,
        }));

  const maintenanceCostData = data.maintenance_summary.maintenance.map(
    (maintenance: any) => ({
      date: maintenance.date,
      cost: maintenance.cost,
      type: maintenance.type,
      street_light_id: maintenance.street_light_id,
    })
  );

  const costSummaryData = [
    { name: "Installation Cost", value: data.cost_summary.total_installation_cost },
    { name: "Maintenance Cost", value: data.cost_summary.total_maintenance_cost },
    { name: "Electricity Cost", value: data.cost_summary.total_electricity_cost },
  ];

  const COLORS = ["#0088FE", "#00C49F", "#FFBB28"];

  return (
    <div className="dashboard">
      <div className="summary-cards">
        <div className="card">
          <h3>Total Lights</h3>
          <p>{data.lights_info.length}</p>
        </div>
        <div className="card">
          <h3>Monthly Energy Usage</h3>
          <p>{data.energy_summary.total_monthly_consumption} kWh</p>
        </div>
        <div className="card">
          <h3>Maintenance Records</h3>
          <p>{data.maintenance_summary.total_maintenance_records}</p>
        </div>
      </div>

      <div className="second-row">
        <div className="pie-card">
          <h4>Cost Distribution</h4>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
                <Tooltip
                content={({ active, payload }) => {
                    if (active && payload && payload.length) {
                    const { name, value } = payload[0].payload;
                    return (
                        <div className="custom-tooltip" style={{ backgroundColor: "#fff", border: "1px solid #ccc", padding: "10px", borderRadius: "5px" }}>
                        <p>{name}</p>
                        <p>Cost: ₹{value}</p>
                        </div>
                    );
                    }
                    return null;
                }}
                />
                <Pie
                data={costSummaryData}
                dataKey="value"
                nameKey="name"
                cx="50%"
                cy="50%"
                outerRadius={80}
                label
                >
                    {costSummaryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                </Pie>
            </PieChart>
          </ResponsiveContainer>
          <p>Total Cost: ₹{data.cost_summary.total_cost}</p>
        </div>
        <div className="warranty-card">
          <h4>Warranty Summary</h4>
          <p>Active Warranties: {data.warranty_summary.active_warranties}</p>
          <p>Expiring Soon: {data.warranty_summary.expiring_soon}</p>
        </div>
      </div>

      <div className="charts">
        <div className="chart">
          <div className="chart-header">
            <h4>Energy Consumption</h4>
            <button
              onClick={() =>
                setToggleConsumption(toggleConsumption === "daily" ? "monthly" : "daily")
              }
            >
              Show {toggleConsumption === "daily" ? "Monthly" : "Daily"}
            </button>
          </div>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={energyConsumptionData}>
              <XAxis dataKey="lightId" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="consumption" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        </div>
        <div className="chart">
          <h4>Maintenance Costs</h4>
          <ResponsiveContainer width="100%" height={300}>
            <LineChart data={maintenanceCostData}>
              <CartesianGrid stroke="#f5f5f5" />
              <XAxis dataKey="date" />
              <YAxis />
              <Tooltip formatter={(value, name, props) => [`₹${value}`, `${props.payload.type} on light id - ${props.payload.street_light_id}`]} />
              <Legend />
              <Line type="monotone" dataKey="cost" stroke="#8884d8" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="table">
        <h4>Lights Specifications</h4>
        <table>
          <thead>
            <tr>
              <th>Light ID</th>
              <th>Contractor Name</th>
              <th>Installation Date</th>
              <th>Manufacturer & Type</th>
              <th>Wattage</th>
              <th>Status</th>
              <th>Last Check</th>
            </tr>
          </thead>
          <tbody>
            {data.lights_info.map((light: any) => (
              <tr key={light.id}>
                <td>{light.id}</td>
                <td>{light.installation.contractor_name}</td>
                <td>{light.installation.installation_date}</td>
                <td>
                  {light.specifications.bulb_manufacturer} ({light.specifications.bulb_type})
                </td>
                <td>{light.specifications.wattage} W</td>
                <td>{light.status.current_status}</td>
                <td>{light.status.last_status_update}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Dashboard;