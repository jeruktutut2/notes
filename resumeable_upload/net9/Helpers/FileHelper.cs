using System.Text;

namespace net9.Helpers;

public static class FileHelper
{
    public static string DetectFileExtensionFromStream(Stream stream)
    {
        byte[] buffer = new byte[20];
        stream.Seek(0, SeekOrigin.Begin);
        // stream.Read(buffer, 0, buffer.Length);
        stream.ReadExactly(buffer);

        // PNG
        if (buffer.Take(8).SequenceEqual(new byte[] { 0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A }))
            return ".png";

        // JPG / JPEG
        if (buffer[0] == 0xFF && buffer[1] == 0xD8)
            return ".jpg";

        // GIF
        if (Encoding.ASCII.GetString(buffer, 0, 3) == "GIF")
            return ".gif";

        // PDF
        if (Encoding.ASCII.GetString(buffer, 0, 4) == "%PDF")
            return ".pdf";

        // ZIP (can be DOCX, XLSX, PPTX too)
        if (buffer[0] == 0x50 && buffer[1] == 0x4B)
            return ".zip";

        // RAR
        if (buffer[0] == 0x52 && buffer[1] == 0x61 && buffer[2] == 0x72 && buffer[3] == 0x21)
            return ".rar";

        // 7z
        if (buffer.Take(6).SequenceEqual(new byte[] { 0x37, 0x7A, 0xBC, 0xAF, 0x27, 0x1C }))
            return ".7z";

        // MP3
        if (buffer[0] == 0x49 && buffer[1] == 0x44 && buffer[2] == 0x33)
            return ".mp3";

        // MP4
        if (buffer[4] == 0x66 && buffer[5] == 0x74 && buffer[6] == 0x79 && buffer[7] == 0x70)
            return ".mp4";

        // MKV (Matroska)
        if (buffer.Take(4).SequenceEqual(new byte[] { 0x1A, 0x45, 0xDF, 0xA3 }))
            return ".mkv";

        // WEBM
        if (buffer.Take(4).SequenceEqual(new byte[] { 0x1A, 0x45, 0xDF, 0xA3 }))
            return ".webm"; // same signature as MKV, but need deeper check for real use

        // EXE
        if (buffer[0] == 0x4D && buffer[1] == 0x5A)
            return ".exe";

        // BMP
        if (buffer[0] == 0x42 && buffer[1] == 0x4D)
            return ".bmp";

        // TIFF (little endian)
        if (buffer[0] == 0x49 && buffer[1] == 0x49 && buffer[2] == 0x2A && buffer[3] == 0x00)
            return ".tif";

        // TIFF (big endian)
        if (buffer[0] == 0x4D && buffer[1] == 0x4D && buffer[2] == 0x00 && buffer[3] == 0x2A)
            return ".tif";

        // WAV
        if (Encoding.ASCII.GetString(buffer, 0, 4) == "RIFF" &&
            Encoding.ASCII.GetString(buffer, 8, 4) == "WAVE")
            return ".wav";

        // AVI
        if (Encoding.ASCII.GetString(buffer, 0, 4) == "RIFF" &&
            Encoding.ASCII.GetString(buffer, 8, 4) == "AVI ")
            return ".avi";

        // FLAC
        if (Encoding.ASCII.GetString(buffer, 0, 4) == "fLaC")
            return ".flac";

        // MOV
        if (Encoding.ASCII.GetString(buffer, 4, 4) == "moov" ||
            Encoding.ASCII.GetString(buffer, 4, 4) == "ftyp")
            return ".mov";

        // DOCX, XLSX, PPTX (all use ZIP as base)
        if (buffer[0] == 0x50 && buffer[1] == 0x4B)
            return ".docx"; // bisa juga .xlsx atau .pptx → butuh pengecekan internal

        return "";
}
}