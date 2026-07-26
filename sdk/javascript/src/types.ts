export interface Prediction {
  module_name: string;
  label: string;
  confidence: number;
  risk_level: "low" | "moderate" | "high" | "critical";
  score: number;
  contributing_features: Array<{ feature?: string; importance: number }>;
  timestamp: string;
  model_version: string;
}

export interface HumanState {
  session_id: string;
  timestamp: string;
  has_pose: boolean;
  posture_quality: number;
  gait_stability: number;
  fatigue_score: number;
  predictions: Prediction[];
}

export interface SessionInfo {
  session_id: string;
  camera_id: string;
  status: string;
  created_at: string;
}

export interface SDKOptions {
  endpoint?: string;
  apiKey?: string;
  timeout?: number;
}
