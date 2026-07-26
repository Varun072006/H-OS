"use client";

import React from "react";

export function SkeletonVisualizer() {
  // SVG Canvas 2D Skeleton Landmarks representation
  const joints = [
    { x: 300, y: 80, name: "head" },
    { x: 300, y: 140, name: "neck" },
    { x: 250, y: 150, name: "left_shoulder" },
    { x: 350, y: 150, name: "right_shoulder" },
    { x: 220, y: 230, name: "left_elbow" },
    { x: 380, y: 230, name: "right_elbow" },
    { x: 200, y: 310, name: "left_wrist" },
    { x: 400, y: 310, name: "right_wrist" },
    { x: 270, y: 290, name: "left_hip" },
    { x: 330, y: 290, name: "right_hip" },
    { x: 260, y: 400, name: "left_knee" },
    { x: 340, y: 400, name: "right_knee" },
    { x: 250, y: 500, name: "left_ankle" },
    { x: 350, y: 500, name: "right_ankle" },
  ];

  const bones = [
    [0, 1], [1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 7],
    [1, 8], [1, 9], [8, 9], [8, 10], [9, 11], [10, 12], [11, 13]
  ];

  return (
    <div className="relative w-full h-full bg-[#0d0e17] rounded-xl border border-border flex items-center justify-center overflow-hidden">
      <svg className="w-full h-full max-h-[520px]" viewBox="0 0 600 560">
        <defs>
          <linearGradient id="boneGrad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stopColor="#3b82f6" />
            <stop offset="50%" stopColor="#06b6d4" />
            <stop offset="100%" stopColor="#10b981" />
          </linearGradient>
        </defs>

        {/* Bone Edges */}
        {bones.map(([j1, j2], i) => (
          <line
            key={i}
            x1={joints[j1].x}
            y1={joints[j1].y}
            x2={joints[j2].x}
            y2={joints[j2].y}
            stroke="url(#boneGrad)"
            strokeWidth="4"
            strokeLinecap="round"
            className="opacity-90 transition-all duration-300"
          />
        ))}

        {/* Joint Nodes */}
        {joints.map((j, i) => (
          <g key={i}>
            <circle
              cx={j.x}
              cy={j.y}
              r="7"
              fill="#06b6d4"
              className="animate-pulse"
            />
            <circle
              cx={j.x}
              cy={j.y}
              r="3"
              fill="#ffffff"
            />
          </g>
        ))}
      </svg>
      <div className="absolute top-4 left-4 px-3 py-1 bg-black/60 backdrop-blur rounded-md border border-border text-xs text-emerald-400 font-mono">
        PRIVACY-FIRST: ANONYMOUS SKELETON GRAPH (RAW VIDEO DELETED)
      </div>
    </div>
  );
}
