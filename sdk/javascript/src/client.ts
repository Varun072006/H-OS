import { HumanState, SDKOptions, SessionInfo } from "./types";

export class HumanOSClient {
  private endpoint: string;
  private apiKey?: string;

  constructor(options: SDKOptions = {}) {
    this.endpoint = (options.endpoint || "http://localhost:8765").replace(/\/$/, "");
    this.apiKey = options.apiKey;
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      ...(options.headers as Record<string, string>),
    };
    if (this.apiKey) {
      headers["X-API-Key"] = this.apiKey;
    }

    const response = await fetch(`${this.endpoint}${path}`, {
      ...options,
      headers,
    });

    if (!response.ok) {
      throw new Error(`HumanOS API Error [${response.status}]: ${await response.text()}`);
    }

    return response.json() as Promise<T>;
  }

  async health(): Promise<{ status: string; version: string }> {
    return this.request<{ status: string; version: string }>("/v1/health");
  }

  async createSession(cameraId: string, sourceType: string = "webcam"): Promise<SessionInfo> {
    return this.request<SessionInfo>("/v1/sessions", {
      method: "POST",
      body: JSON.stringify({ camera_id: cameraId, source_type: sourceType }),
    });
  }

  async getHumanState(sessionId: string): Promise<HumanState> {
    return this.request<HumanState>(`/v1/sessions/${sessionId}/state`);
  }

  async closeSession(sessionId: string): Promise<boolean> {
    const res = await this.request<{ status: string }>(`/v1/sessions/${sessionId}`, {
      method: "DELETE",
    });
    return res.status === "closed";
  }
}
