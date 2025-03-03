// Chat/WebSocket types
export interface WebSocketMessage {
  type: 'message' | 'client_info'
  sender?: string
  content?: string
  client_id?: string
  display_name?: string
}

// Server configuration types
export interface ServerStats {
  active_connections: number
  uptime_seconds: number
  clients: ClientInfo[]
}

export interface ClientInfo {
  id: string
  display_name: string
  connected_for: number
  message_count: number
}

export interface HealthStatus {
  ok: boolean
  message: string
}

export type NameSelectionMode = 'server' | 'preset' | 'custom'