"use client";

import React from "react";
import { useDashboardStore } from "@/lib/store";
import { Cpu, Zap, Eye, Shield } from "lucide-react";

export function PerformanceChart() {
  const { fps, latencyMs } = useDashboardStore();

  return (
    <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
      <div className="p-4 bg-card border border-border rounded-xl space-y-1">
        <div className="flex items-center justify-between text-gray-400 text-xs">
          <span>INFERENCE LATENCY</span>
          <Zap className="w-4 h-4 text-amber" />
        </div>
        <p className="text-2xl font-bold text-gray-100">{latencyMs.toFixed(1)} ms</p>
        <p className="text-[11px] text-emerald-400">Target: &lt;100ms</p>
      </div>

      <div className="p-4 bg-card border border-border rounded-xl space-y-1">
        <div className="flex items-center justify-between text-gray-400 text-xs">
          <span>PROCESSING FPS</span>
          <Cpu className="w-4 h-4 text-accent" />
        </div>
        <p className="text-2xl font-bold text-gray-100">{fps} FPS</p>
        <p className="text-[11px] text-emerald-400">Real-time Stream</p>
      </div>

      <div className="p-4 bg-card border border-border rounded-xl space-y-1">
        <div className="flex items-center justify-between text-gray-400 text-xs">
          <span>POSE DETECTOR</span>
          <Eye className="w-4 h-4 text-cyan" />
        </div>
        <p className="text-lg font-bold text-gray-100">MediaPipe 3D</p>
        <p className="text-[11px] text-gray-400">33 Landmarks</p>
      </div>

      <div className="p-4 bg-card border border-border rounded-xl space-y-1">
        <div className="flex items-center justify-between text-gray-400 text-xs">
          <span>PRIVACY STATUS</span>
          <Shield className="w-4 h-4 text-emerald" />
        </div>
        <p className="text-lg font-bold text-emerald-400">ENFORCED</p>
        <p className="text-[11px] text-gray-400">Frames Zeroed</p>
      </div>
    </div>
  );
}
