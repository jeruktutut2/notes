package modelresponses

type MillisecondResponse struct {
	Datetime            string `json:"datetime"`
	Millisecond         int64  `json:"millisecond"`
	Add1Hour            string `json:"add1Hour"`
	Add1HourMillisecond int64  `json:"add1HourMillisecond"`
}

func GetMillisecondResponse(datetime string, millisecond int64, add1Hour string, add1HourMillisecond int64) MillisecondResponse {
	return MillisecondResponse{
		Datetime:            datetime,
		Millisecond:         millisecond,
		Add1Hour:            add1Hour,
		Add1HourMillisecond: add1HourMillisecond,
	}
}
