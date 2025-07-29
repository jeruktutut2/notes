
using System.Security.Cryptography;
using System.Security.Cryptography.X509Certificates;
using System.Text;

namespace net9.Helpers;

public class KeyHelper: IKeyHelper
{
    private readonly RSA _privateKey;
    private readonly RSA _publicKey;
    public KeyHelper()
    {
        var pemPrivateKey = File.ReadAllText("../Keys/private_key_pkcs8.pem");
        // Console.WriteLine(pemPrivateKey);
        _privateKey = RSA.Create();

        if (pemPrivateKey.Contains("-----BEGIN PRIVATE KEY-----"))
        {
            _privateKey.ImportFromPem(pemPrivateKey.ToCharArray()); // pksc#8
        }
        else if (pemPrivateKey.Contains("-----BEGIN RSA PRIVATE KEY-----"))
        {
            _privateKey.ImportRSAPrivateKey(PemToBytes(pemPrivateKey), out _);
        }
        else
        {
            throw new Exception("Unsupported private key format.");
        }

        var pemPublicKey = File.ReadAllText("../Keys/public_key.pem");
        // Console.WriteLine(pemPublicKey);
        _publicKey = RSA.Create();
        if (pemPublicKey.Contains("-----BEGIN PUBLIC KEY-----"))
        {
            _publicKey.ImportFromPem(pemPublicKey.ToCharArray()); // PKCS#8 public
        }
        else
        {
            throw new Exception("Unsupported public key or certificate format.");
        }

        // Console.WriteLine(_privateKey);
        // Console.WriteLine(_publicKey);
    }

    private static byte[] PemToBytes(string pem)
    {
        var lines = pem.Split('\n')
                       .Where(line => !line.StartsWith("-----"))
                       .ToArray();
        return Convert.FromBase64String(string.Join("", lines));
    }

    public string Sign(string message)
    {
        var bytes = Encoding.UTF8.GetBytes(message);
        var signatureBytes = _privateKey.SignData(bytes, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        var signature = Convert.ToBase64String(signatureBytes);
        return signature;
    }

    public bool Verify(string message, string base64Signature)
    {
        var messageBytes = Encoding.UTF8.GetBytes(message);
        var signatureBytes = Convert.FromBase64String(base64Signature);
        bool isVerified = _publicKey.VerifyData(messageBytes, signatureBytes, HashAlgorithmName.SHA256, RSASignaturePadding.Pkcs1);
        return isVerified;
    }
}
