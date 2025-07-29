using net9.Helpers;
using net9.Models.Requests;
using net9.Models.Responses;

namespace net9.Services;

public class RsaService: IRsaService
{
    private readonly IKeyHelper _keyhelper;
    public RsaService(IKeyHelper keyHelper)
    {
        _keyhelper = keyHelper;
    }

    public SignResponse Sign(SignRequest signRequest)
    {
        var signature = _keyhelper.Sign(signRequest.Message);
        return new SignResponse { Message = signRequest.Message, Signature = signature };
    }

    public VerifyResponse Verify(VerifyRequest verifyRequest)
    {
        var isVerified = _keyhelper.Verify(verifyRequest.Message, verifyRequest.Signature);
        return new VerifyResponse { Message = verifyRequest.Message, Signature = verifyRequest.Signature, IsVerified = isVerified };
    }
}