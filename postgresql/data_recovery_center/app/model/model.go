package model

import "time"

type ApplicationData struct {
	ID           int       `json:"id"`
	UUID         string    `json:"uuid"`
	Title        string    `json:"title"`
	Content      string    `json:"content"`
	Category     string    `json:"category"`
	SourceDC     string    `json:"source_dc"`
	IsReplicated bool      `json:"is_replicated"`
	CreatedAt    time.Time `json:"created_at"`
	UpdatedAt    time.Time `json:"updated_at"`
}

type CreateDataRequest struct {
	Title    string `json:"title"`
	Content  string `json:"content"`
	Category string `json:"category"`
}

type DRLog struct {
	ID          int       `json:"id"`
	EventType   string    `json:"event_type"`
	EventSource string    `json:"event_source"`
	Description string    `json:"description"`
	Metadata    any       `json:"metadata"`
	CreatedAt   time.Time `json:"created_at"`
}

type FailoverHistory struct {
	ID          int       `json:"id"`
	EventType   string    `json:"event_type"`
	FromHost    string    `json:"from_host"`
	ToHost      string    `json:"to_host"`
	InitiatedBy string    `json:"initiated_by"`
	DurationMS  int       `json:"duration_ms"`
	Status      string    `json:"status"`
	Notes       string    `json:"notes"`
	CreatedAt   time.Time `json:"created_at"`
}

type SystemStatusResponse struct {
	ActiveTarget string           `json:"active_target"`
	IsRecovery   bool             `json:"is_recovery_mode"`
	DBConnected  bool             `json:"db_connected"`
	TargetHost   string           `json:"target_host"`
	TotalData    int              `json:"total_data"`
	LastData     *ApplicationData `json:"last_data,omitempty"`
	CheckedAt    time.Time        `json:"checked_at"`
}

type ReplicationStatusResponse struct {
	IsPrimary       bool   `json:"is_primary"`
	IsInRecovery    bool   `json:"is_in_recovery"`
	ReplicationLag  string `json:"replication_lag,omitempty"`
	WALLSN          string `json:"wal_lsn"`
	ActiveReplicas  int    `json:"active_replicas"`
	ConnectedTarget string `json:"connected_target"`
}

type GenericResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
	Data    any    `json:"data,omitempty"`
}
