package services

import (
	"context"
	"fmt"
	"os"

	"github.com/jung-kurt/gofpdf"
	"github.com/pdfcpu/pdfcpu/pkg/api"
)

type FileService interface {
	GeneratePdf(ctx context.Context) (filename string)
}

type fileService struct {
}

func NewFileService() FileService {
	return &fileService{}
}

type row struct {
	Id   int
	Text string
}

func (service *fileService) GeneratePdf(ctx context.Context) (docPdf string) {
	// create merge pdf file
	mergePdf := "pdfs/merge.pdf"
	pdf := gofpdf.New("P", "mm", "A4", "")
	pdf.AddPage()
	pdf.SetFont("Arial", "", 12)
	pdf.Cell(40, 10, "Initial empty PDF")
	err := pdf.OutputFileAndClose(mergePdf)
	if err != nil {
		return err.Error()
	}

	rows := []row{
		{1, "first"},
		{2, "second"},
		{3, "third"},
	}

	for _, row := range rows {
		pdf := gofpdf.New("P", "mm", "A4", "")
		pdf.AddPage()
		pdf.SetFont("Arial", "", 16)
		pdf.Cell(40, 10, fmt.Sprintf("ID: %d", row.Id))
		pdf.Ln(12)
		pdf.Cell(40, 10, row.Text)
		filenamePdf := fmt.Sprintf("pdfs/page_%d.pdf", row.Id)
		err := pdf.OutputFileAndClose(filenamePdf)
		if err != nil {
			return err.Error()
		}

		docPdf = "pdfs/doc.pdf"
		err = api.MergeCreateFile([]string{mergePdf, filenamePdf}, docPdf, false, nil)
		if err != nil {
			return err.Error()
		}
		err = os.Remove(filenamePdf)
		if err != nil {
			return err.Error()
		}
		err = os.Rename(docPdf, mergePdf)
		if err != nil {
			return err.Error()
		}
	}
	err = os.Rename(mergePdf, docPdf)
	if err != nil {
		return err.Error()
	}
	err = api.RemovePagesFile(docPdf, "", []string{"1"}, nil)
	if err != nil {
		return err.Error()
	}
	return
}
