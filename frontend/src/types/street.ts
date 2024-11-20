export interface StreetBasicInfo {
  id?: number;
  street_name: string;
  ward: string | null;
  total_lights: number;
  total_power_consumption: number;
  operational_summary: { [key: string]: number };
  recent_issues: number;
}