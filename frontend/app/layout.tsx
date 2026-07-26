import React from "react";
import "./globals.css";

export const metadata = {
  title: "HumanOS Dashboard — Privacy-First Human Motion Intelligence Platform",
  description: "Operating system for understanding human movement, behavior, physical state, and future risks.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-background text-gray-100 font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
