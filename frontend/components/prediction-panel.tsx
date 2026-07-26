"use client";

import React from "react";
import { useDashboardStore } from "@/lib/store";
import { AlertTriangle, ShieldCheck, Activity, HeartPulse } from "lucide-react";

export function PredictionPanel() {
  const { predictions } = useDashboardStore();

  const getRiskBadge = (level: string) => {
    switch (level) {
      case "critical":
        return <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-rose-500/20 text-rose-400 border border-rose-500/40">CRITICAL</span>;
      case "high":
        return <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-amber-500/20 text-amber-400 border border-amber-500/40">HIGH</span>;
      case "moderate":
        return <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-cyan-500/20 text-cyan-400 border border-cyan-500/40">MODERATE</span>;
      default:
        return <span className="px-2.5 py-0.5 rounded text-xs font-semibold bg-emerald-500/20 text-emerald-400 border border-emerald-500/40">LOW RISK</span>;
    }
  };

  return (
    <div className="space-y-4">
      <h2 className="text-lg font-bold text-gray-100 flex items-center gap-2">
        <Activity className="w-5 h-5 text-accent" />
        Real-Time Prediction Intelligence
      </h2>

      <div className="grid grid-cols-1 gap-3">
        {predictions.map((p, idx) => (
          <div
            key={idx}
            className="p-4 bg-card border border-border rounded-xl flex items-center justify-between hover:border-accent/40 transition-all"
          >
            <div className="space-y-1">
              <div className="flex items-center gap-2">
                <span className="text-xs uppercase font-mono tracking-wider text-gray-400">
                  {p.module_name.replace("_", " ")}
                </span>
                {getRiskBadge(p.risk_level)}
              </div>
              <p className="text-base font-semibold text-gray-100">{p.label}</p>
              <div className="flex items-center gap-4 text-xs text-gray-400">
                <span>Confidence: {(p.confidence * 100).toFixed(0)}%</span>
                <span>Model: {p.model_version}</span>
              </div>
            </div>

            <div className="w-16 h-16 rounded-full bg-background border border-border flex flex-col items-center justify-center">
              <span className="text-sm font-bold text-accent">{(p.score * 100).toFixed(0)}%</span>
              <span className="text-[10px] text-gray-400">score</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
