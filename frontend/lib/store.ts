"use client";

import { create } from "zustand";

export interface PredictionItem {
  module_name: string;
  label: string;
  confidence: number;
  risk_level: "low" | "moderate" | "high" | "critical";
  score: number;
  contributing_features: Array<{ feature?: string; importance: number }>;
  timestamp: string;
  model_version: string;
}

export interface DashboardState {
  activeSessionId: string;
  isStreaming: boolean;
  fps: number;
  latencyMs: number;
  selectedModel: string;
  predictions: PredictionItem[];
  postureQuality: number;
  gaitStability: number;
  fatigueScore: number;
  setStreaming: (streaming: boolean) => void;
  setMetrics: (fps: number, latencyMs: number) => void;
  updateState: (data: Partial<DashboardState>) => void;
}

export const useDashboardStore = create<DashboardState>((set) => ({
  activeSessionId: "sess_demo_live",
  isStreaming: false,
  fps: 30,
  latencyMs: 18.5,
  selectedModel: "stgcn_default",
  predictions: [
    {
      module_name: "fall_risk",
      label: "Normal Mobility",
      confidence: 0.94,
      risk_level: "low",
      score: 0.12,
      contributing_features: [{ feature: "gait_stability", importance: 0.88 }],
      timestamp: new Date().toISOString(),
      model_version: "stgcn-v1.0",
    },
    {
      module_name: "posture",
      label: "Ergonomic Posture",
      confidence: 0.91,
      risk_level: "low",
      score: 0.18,
      contributing_features: [{ feature: "spinal_load", importance: 0.91 }],
      timestamp: new Date().toISOString(),
      model_version: "posture-v1.0",
    },
  ],
  postureQuality: 0.92,
  gaitStability: 0.95,
  fatigueScore: 0.1,
  setStreaming: (isStreaming) => set({ isStreaming }),
  setMetrics: (fps, latencyMs) => set({ fps, latencyMs }),
  updateState: (data) => set((state) => ({ ...state, ...data })),
}));
