package migrations

import "embed"

// FS meng-embed semua file SQL migration ke dalam binary Go.
// Ini memungkinkan migration dijalankan tanpa perlu file terpisah di disk.
//
// Struktur yang di-embed:
//
//	sql/
//	  ├── 000001_create_users_table.up.sql
//	  ├── 000001_create_users_table.down.sql
//	  ├── 000002_add_email_to_users.up.sql
//	  ├── 000002_add_email_to_users.down.sql
//	  ├── ...dst
//
//go:embed sql/*.sql
var FS embed.FS
