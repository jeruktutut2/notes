package modelrequests

type MillisecondRequest struct {
	Year   int `json:"year"`
	Month  int `json:"month"`
	Date   int `json:"date"`
	Hour   int `json:"hour"`
	Minute int `json:"minute"`
	Second int `json:"second"`
}
