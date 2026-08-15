package mapreduce

import "net/rpc"

// TaskType membedakan pekerjaan yang diberikan Master
type TaskType int

const (
	TaskTypeMap TaskType = iota
	TaskTypeReduce
	TaskTypeWait
	TaskTypeExit
)

// Pekerjaan yang dikirim dari Master ke Worker
type Task struct {
	Type     TaskType
	TaskID   int
	Filename string // Untuk Map: nama file yang harus diolah
}

// Laporan hasil kerja dari Worker ke Master
type TaskResult struct {
	Type   TaskType
	TaskID int
}

// Master RPC Service API
type MasterRPC struct{}

// GetTask dipanggil oleh Worker untuk meminta pekerjaan dari Master
func CallGetTask() Task {
	args := struct{}{}
	reply := Task{}
	call("MasterRPC.GetTask", &args, &reply)
	return reply
}

// ReportTask dipanggil oleh Worker untuk melaporkan pekerjaan selesai
func CallReportTask(args *TaskResult) {
	reply := struct{}{}
	call("MasterRPC.ReportTask", args, &reply)
}

// Wrapper untuk melakukan pemanggilan RPC ke localhost:1234
func call(rpcname string, args interface{}, reply interface{}) bool {
	c, err := rpc.DialHTTP("tcp", "127.0.0.1:1234")
	if err != nil {
		return false
	}
	defer c.Close()

	err = c.Call(rpcname, args, reply)
	if err == nil {
		return true
	}
	return false
}
