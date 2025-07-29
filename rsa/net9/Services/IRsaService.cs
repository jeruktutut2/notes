using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public interface IRsaService
{
    SignResponse Sign(SignRequest signRequest);
    VerifyResponse Verify(VerifyRequest verifyRequest);
}