using net9.Models.Requests;

namespace net9.Services;

public interface IImageService
{
    string CheckImage(ImageRequest imageRequest);
}