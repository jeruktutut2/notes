package repository

import (
	"context"
	"fmt"
	"log"
	"sync"
	"time"

	"drc-app/config"
	"drc-app/model"

	"github.com/jackc/pgx/v5/pgxpool"
)

type Repository interface {
	GetActiveTarget() string
	SetActiveTarget(target string) error
	Ping(ctx context.Context) error
	GetReplicationInfo(ctx context.Context) (*model.ReplicationStatusResponse, error)
	GetSystemStatus(ctx context.Context) (*model.SystemStatusResponse, error)
	CreateData(ctx context.Context, req model.CreateDataRequest) (*model.ApplicationData, error)
	ListData(ctx context.Context) ([]model.ApplicationData, error)
	GetDataByID(ctx context.Context, id int) (*model.ApplicationData, error)
	LogDREvent(ctx context.Context, eventType, source, desc string) error
	ListDRLogs(ctx context.Context) ([]model.DRLog, error)
	RecordFailover(ctx context.Context, eventType, fromHost, toHost, initiatedBy string, durationMS int, notes string) error
	Close()
}

type repository struct {
	mu           sync.RWMutex
	cfg          *config.Config
	activeTarget string // "dc" or "drc"
	dcPool       *pgxpool.Pool
	drcPool      *pgxpool.Pool
}

func NewRepository(cfg *config.Config) (Repository, error) {
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	dcPool, err := pgxpool.New(ctx, cfg.DCDB.DSN())
	if err != nil {
		log.Printf("[WARN] Failed to connect to DC Pool: %v", err)
	}

	drcPool, err := pgxpool.New(ctx, cfg.DRCDB.DSN())
	if err != nil {
		log.Printf("[WARN] Failed to connect to DRC Pool: %v", err)
	}

	repo := &repository{
		cfg:          cfg,
		activeTarget: cfg.ActiveDB,
		dcPool:       dcPool,
		drcPool:      drcPool,
	}

	return repo, nil
}

func (r *repository) getPool() (*pgxpool.Pool, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if r.activeTarget == "drc" {
		if r.drcPool == nil {
			return nil, fmt.Errorf("DRC database pool is not connected")
		}
		return r.drcPool, nil
	}

	if r.dcPool == nil {
		return nil, fmt.Errorf("DC database pool is not connected")
	}
	return r.dcPool, nil
}

func (r *repository) GetActiveTarget() string {
	r.mu.RLock()
	defer r.mu.RUnlock()
	return r.activeTarget
}

func (r *repository) SetActiveTarget(target string) error {
	if target != "dc" && target != "drc" {
		return fmt.Errorf("invalid target: %s (must be 'dc' or 'drc')", target)
	}

	r.mu.Lock()
	defer r.mu.Unlock()
	r.activeTarget = target
	log.Printf("[INFO] Active database target switched to: %s", target)
	return nil
}

func (r *repository) Ping(ctx context.Context) error {
	pool, err := r.getPool()
	if err != nil {
		return err
	}
	return pool.Ping(ctx)
}

func (r *repository) GetReplicationInfo(ctx context.Context) (*model.ReplicationStatusResponse, error) {
	pool, err := r.getPool()
	if err != nil {
		return nil, err
	}

	var inRecovery bool
	err = pool.QueryRow(ctx, "SELECT pg_is_in_recovery()").Scan(&inRecovery)
	if err != nil {
		return nil, fmt.Errorf("query recovery status failed: %w", err)
	}

	res := &model.ReplicationStatusResponse{
		IsPrimary:       !inRecovery,
		IsInRecovery:    inRecovery,
		ConnectedTarget: r.GetActiveTarget(),
	}

	if !inRecovery {
		// We are Primary - check active replication clients
		var lsn string
		_ = pool.QueryRow(ctx, "SELECT pg_current_wal_lsn()::text").Scan(&lsn)
		res.WALLSN = lsn

		var count int
		_ = pool.QueryRow(ctx, "SELECT count(*) FROM pg_stat_replication").Scan(&count)
		res.ActiveReplicas = count
	} else {
		// We are Standby - check last received LSN
		var lsn string
		_ = pool.QueryRow(ctx, "SELECT pg_last_wal_receive_lsn()::text").Scan(&lsn)
		res.WALLSN = lsn
	}

	return res, nil
}

func (r *repository) GetSystemStatus(ctx context.Context) (*model.SystemStatusResponse, error) {
	activeTarget := r.GetActiveTarget()
	pool, err := r.getPool()

	status := &model.SystemStatusResponse{
		ActiveTarget: activeTarget,
		CheckedAt:    time.Now(),
	}

	if err != nil || pool == nil {
		status.DBConnected = false
		return status, nil
	}

	if err := pool.Ping(ctx); err != nil {
		status.DBConnected = false
		return status, nil
	}

	status.DBConnected = true

	if activeTarget == "dc" {
		status.TargetHost = fmt.Sprintf("%s:%s", r.cfg.DCDB.Host, r.cfg.DCDB.Port)
	} else {
		status.TargetHost = fmt.Sprintf("%s:%s", r.cfg.DRCDB.Host, r.cfg.DRCDB.Port)
	}

	var inRecovery bool
	_ = pool.QueryRow(ctx, "SELECT pg_is_in_recovery()").Scan(&inRecovery)
	status.IsRecovery = inRecovery

	var total int
	_ = pool.QueryRow(ctx, "SELECT COUNT(*) FROM application_data").Scan(&total)
	status.TotalData = total

	var last model.ApplicationData
	err = pool.QueryRow(ctx, `
		SELECT id, uuid, title, content, category, source_dc, is_replicated, created_at, updated_at
		FROM application_data
		ORDER BY id DESC LIMIT 1
	`).Scan(&last.ID, &last.UUID, &last.Title, &last.Content, &last.Category, &last.SourceDC, &last.IsReplicated, &last.CreatedAt, &last.UpdatedAt)

	if err == nil {
		status.LastData = &last
	}

	return status, nil
}

func (r *repository) CreateData(ctx context.Context, req model.CreateDataRequest) (*model.ApplicationData, error) {
	pool, err := r.getPool()
	if err != nil {
		return nil, err
	}

	sourceDC := r.GetActiveTarget()
	category := req.Category
	if category == "" {
		category = "general"
	}

	var item model.ApplicationData
	query := `
		INSERT INTO application_data (title, content, category, source_dc)
		VALUES ($1, $2, $3, $4)
		RETURNING id, uuid, title, content, category, source_dc, is_replicated, created_at, updated_at
	`
	err = pool.QueryRow(ctx, query, req.Title, req.Content, category, sourceDC).Scan(
		&item.ID, &item.UUID, &item.Title, &item.Content, &item.Category, &item.SourceDC, &item.IsReplicated, &item.CreatedAt, &item.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("failed to insert data: %w", err)
	}

	_ = r.LogDREvent(ctx, "DATA_INSERT", sourceDC, fmt.Sprintf("Inserted item ID %d: %s", item.ID, item.Title))

	return &item, nil
}

func (r *repository) ListData(ctx context.Context) ([]model.ApplicationData, error) {
	pool, err := r.getPool()
	if err != nil {
		return nil, err
	}

	query := `
		SELECT id, uuid, title, content, category, source_dc, is_replicated, created_at, updated_at
		FROM application_data
		ORDER BY id DESC
	`
	rows, err := pool.Query(ctx, query)
	if err != nil {
		return nil, fmt.Errorf("failed to query data: %w", err)
	}
	defer rows.Close()

	var items []model.ApplicationData
	for rows.Next() {
		var item model.ApplicationData
		if err := rows.Scan(&item.ID, &item.UUID, &item.Title, &item.Content, &item.Category, &item.SourceDC, &item.IsReplicated, &item.CreatedAt, &item.UpdatedAt); err != nil {
			return nil, err
		}
		items = append(items, item)
	}

	return items, nil
}

func (r *repository) GetDataByID(ctx context.Context, id int) (*model.ApplicationData, error) {
	pool, err := r.getPool()
	if err != nil {
		return nil, err
	}

	query := `
		SELECT id, uuid, title, content, category, source_dc, is_replicated, created_at, updated_at
		FROM application_data
		WHERE id = $1
	`
	var item model.ApplicationData
	err = pool.QueryRow(ctx, query, id).Scan(
		&item.ID, &item.UUID, &item.Title, &item.Content, &item.Category, &item.SourceDC, &item.IsReplicated, &item.CreatedAt, &item.UpdatedAt,
	)
	if err != nil {
		return nil, fmt.Errorf("data not found: %w", err)
	}

	return &item, nil
}

func (r *repository) LogDREvent(ctx context.Context, eventType, source, desc string) error {
	pool, err := r.getPool()
	if err != nil {
		return err
	}

	query := `
		INSERT INTO disaster_recovery_logs (event_type, event_source, description)
		VALUES ($1, $2, $3)
	`
	_, err = pool.Exec(ctx, query, eventType, source, desc)
	return err
}

func (r *repository) ListDRLogs(ctx context.Context) ([]model.DRLog, error) {
	pool, err := r.getPool()
	if err != nil {
		return nil, err
	}

	query := `
		SELECT id, event_type, event_source, description, metadata, created_at
		FROM disaster_recovery_logs
		ORDER BY id DESC LIMIT 50
	`
	rows, err := pool.Query(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var logs []model.DRLog
	for rows.Next() {
		var l model.DRLog
		if err := rows.Scan(&l.ID, &l.EventType, &l.EventSource, &l.Description, &l.Metadata, &l.CreatedAt); err != nil {
			return nil, err
		}
		logs = append(logs, l)
	}

	return logs, nil
}

func (r *repository) RecordFailover(ctx context.Context, eventType, fromHost, toHost, initiatedBy string, durationMS int, notes string) error {
	pool, err := r.getPool()
	if err != nil {
		return err
	}

	query := `
		INSERT INTO failover_history (event_type, from_host, to_host, initiated_by, duration_ms, notes)
		VALUES ($1, $2, $3, $4, $5, $6)
	`
	_, err = pool.Exec(ctx, query, eventType, fromHost, toHost, initiatedBy, durationMS, notes)
	return err
}

func (r *repository) Close() {
	if r.dcPool != nil {
		r.dcPool.Close()
	}
	if r.drcPool != nil {
		r.drcPool.Close()
	}
}
