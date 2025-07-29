# PDF

## library
    dotnet add package QuestPDF
    dotnet add package PdfSharpCore --version 1.3.67
    dotnet add package PdfSharpCore.Extensions --version 0.1.2.4 (optional manipulasi ekstra)
    dotnet add package PdfiumViewer.Updated --version 2.14.5 (optional for advanced rendering)
    dotnet add package PdfLibNet.VbPackage --version 11.0.0.10 (optional for advanced rendering)

## error
     PdfSharpCore tidak mendukung streaming halaman PDF satu per satu dari disk tanpa memuat seluruh file ke memori terlebih dahulu. Ini adalah batasan internal dari PdfSharp.