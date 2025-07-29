package services

import (
	"context"
	modelrequests "note-golang-millisecond/models/requests"
	modelresponses "note-golang-millisecond/models/responses"
	"time"
)

type MillisecondService interface {
	GetByGMTPlus8(ctx context.Context, millisecondRequest modelrequests.MillisecondRequest) (millisecondResponse modelresponses.MillisecondResponse)
	GetByGMTMinus8(ctx context.Context, millisecondRequest modelrequests.MillisecondRequest) (millisecondResponse modelresponses.MillisecondResponse)
}

type millisecondService struct {
}

func NewMillisecondService() MillisecondService {
	return &millisecondService{}
}

func (service *millisecondService) GetByGMTPlus8(ctx context.Context, millisecondRequest modelrequests.MillisecondRequest) (millisecondResponse modelresponses.MillisecondResponse) {
	// Offset -8 jam = -8 * 3600 detik = -28800
	gmtplus8 := time.FixedZone("GMT+08:00", 8*60*60)

	t := time.Date(millisecondRequest.Year, time.Month(millisecondRequest.Month), millisecondRequest.Date, millisecondRequest.Hour, millisecondRequest.Minute, millisecondRequest.Second, 0, gmtplus8)
	millisecondResponse.Datetime = t.String()
	millisecondResponse.Millisecond = t.UnixMilli()
	millisecondResponse.Add1Hour = t.Add(1 * time.Hour).String()
	millisecondResponse.Add1HourMillisecond = t.Add(1 * time.Hour).UnixMilli()
	return
}

func (service *millisecondService) GetByGMTMinus8(ctx context.Context, millisecondRequest modelrequests.MillisecondRequest) (millisecondResponse modelresponses.MillisecondResponse) {
	// Offset -8 jam = -8 * 3600 detik = -28800
	gmtMinus8 := time.FixedZone("GMT-08:00", -8*60*60)
	t := time.Date(millisecondRequest.Year, time.Month(millisecondRequest.Month), millisecondRequest.Date, millisecondRequest.Hour, millisecondRequest.Minute, millisecondRequest.Second, 0, gmtMinus8)
	millisecondResponse.Datetime = t.String()
	millisecondResponse.Millisecond = t.UnixMilli()
	millisecondResponse.Add1Hour = t.Add(1 * time.Hour).String()
	millisecondResponse.Add1HourMillisecond = t.Add(1 * time.Hour).UnixMilli()
	return
}
