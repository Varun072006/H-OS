"use client";

import React from "react";
import { SkeletonVisualizer } from "@/components/skeleton-visualizer";
import { PredictionPanel } from "@/components/prediction-panel";
import { PerformanceChart } from "@/components/performance-chart";
import { Shield, Activity, Video, Settings, Play, Square } from "lucide-react";
import { useDashboardStore } from "@/lib/store";

export default function DashboardPage() {
  const { isStreaming, setStreaming, postureQuality, gaitStability, fatigueScore } = useDashboardStore();

  return (
    <div className="min-h-screen flex flex-col max-w-7xl mx-auto p-4 md:p-6 space-y-6">
      {/* Header Bar */}
      <header className="flex items-center justify-between p-4 bg-card border border-border rounded-xl">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-accent/20 border border-accent/40 flex items-center justify-center">
            <Activity className="w-6 h-6 text-accent" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white">HumanOS</h1>
            <p className="text-xs text-gray-400">The Privacy-First Human Intelligence Platform</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            onClick={() => setStreaming(!isStreaming)}
            className={`px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2 transition-all ${
              isStreaming
                ? "bg-rose-500/20 text-rose-400 border border-rose-500/40 hover:bg-rose-500/30"
                : "bg-accent text-white hover:bg-accent/90 shadow-lg shadow-accent/20"
            }`}
          >
            {isStreaming ? (
              <>
                <Square className="w-4 h-4" /> Stop Live Stream
              </>
            ) : (
              <>
                <Play className="w-4 h-4" /> Start Stream Pipeline
              </>
            )}
          </button>
        </div>
      </header>

      {/* Metrics Row */}
      <PerformanceChart />

      {/* Main Grid: Visualizer + Predictions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Cols: Skeleton Visualizer */}
        <div className="lg:col-span-2 space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-gray-100 flex items-center gap-2">
              <Video className="w-5 h-5 text-cyan" />
              Continuous Motion Stream
            </h2>
            <div className="flex items-center gap-2 text-xs text-emerald-400 font-mono">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping" />
              PRIVACY BOUNDARY ACTIVE
            </div>
          </div>

          <SkeletonVisualizer />

          {/* Physical State Indicators */}
          <div className="grid grid-cols-3 gap-3">
            <div className="p-3 bg-card border border-border rounded-lg text-center">
              <p className="text-xs text-gray-400">Posture Quality</p>
              <p className="text-lg font-bold text-emerald-400">{(postureQuality * 100).toFixed(0)}%</p>
            </div>
            <div className="p-3 bg-card border border-border rounded-lg text-center">
              <p className="text-xs text-gray-400">Gait Stability</p>
              <p className="text-lg font-bold text-accent">{(gaitStability * 100).toFixed(0)}%</p>
            </div>
            <div className="p-3 bg-card border border-border rounded-lg text-center">
              <p className="text-xs text-gray-400">Fatigue Index</p>
              <p className="text-lg font-bold text-amber">{(fatigueScore * 100).toFixed(0)}%</p>
            </div>
          </div>
        </div>

        {/* Right Col: Predictions & Intelligence */}
        <div className="space-y-4">
          <PredictionPanel />
        </div>
      </div>
    </div>
  );
}
