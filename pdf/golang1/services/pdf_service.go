package services

import (
	"bytes"

	"github.com/johnfercher/maroto/pkg/consts"
	"github.com/johnfercher/maroto/pkg/pdf"
)

type PdfService interface {
	GetPdf() (bytesBuffer bytes.Buffer, err error)
}

type pdfService struct {
}

func NewPdfService() PdfService {
	return &pdfService{}
}

// https://www.youtube.com/watch?v=jwOy4JgleTU
func (service *pdfService) GetPdf() (bytesBuffer bytes.Buffer, err error) {
	maroto := pdf.NewMaroto(consts.Portrait, consts.A4)
	maroto.SetPageMargins(20, 10, 20)
	// only produces 1 output, if use two output, the other one will produce zero byte
	// err = maroto.OutputFileAndClose("pdfs/pdfA2.pdf")
	bytesBuffer, err = maroto.Output()
	return
}
