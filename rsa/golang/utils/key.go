package utils

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"log"
	"os"
)

type KeyUtil interface {
	Sign(message string) (signature string, err error)
	Verify(message string, signature string) (isVerify bool, err error)
}

type keyUtil struct {
	privateKey *rsa.PrivateKey
	publicKey  *rsa.PublicKey
}

func NewKeyUtil() KeyUtil {
	var err error
	var ok bool
	privateKeyByte, err := os.ReadFile("../keys/private_key_pkcs8.pem")
	// fmt.Println(string(privateKeyByte))
	if err != nil {
		log.Fatalln("err:", err)
	}
	publicKeyByte, err := os.ReadFile("../keys/public_key.pem")
	if err != nil {
		log.Fatalln("err:", err)
	}

	blockPrivateKey, _ := pem.Decode(privateKeyByte)
	if blockPrivateKey == nil {
		log.Fatalln("not a private key")
	}

	var privateKey *rsa.PrivateKey
	switch blockPrivateKey.Type {
	case "RSA PRIVATE KEY":
		privateKey, err = x509.ParsePKCS1PrivateKey(blockPrivateKey.Bytes)
		if err != nil {
			log.Fatalln(err)
		}
	case "PRIVATE KEY":
		key, err := x509.ParsePKCS8PrivateKey(blockPrivateKey.Bytes)
		if err != nil {
			log.Fatalln(err)
		}
		privateKey, ok = key.(*rsa.PrivateKey)
		if !ok {
			log.Fatalln("key inside PKCS#8 is not RSA")
		}
	default:
		log.Fatalln("unknown private key type")
	}

	blockPublicKey, _ := pem.Decode(publicKeyByte)
	if blockPublicKey == nil {
		log.Fatalln("not a public key")
	}

	var publicKey *rsa.PublicKey
	switch blockPublicKey.Type {
	case "PUBLIC KEY":
		key, err := x509.ParsePKIXPublicKey(blockPublicKey.Bytes)
		if err != nil {
			log.Fatalln(err)
		}
		publicKey, ok = key.(*rsa.PublicKey)
		if !ok {
			log.Fatalln("not an RSA public key")
		}
	case "RSA PUBLIC KEY":
		publicKey, err = x509.ParsePKCS1PublicKey(blockPublicKey.Bytes)
		if err != nil {
			log.Fatalln(err)
		}
	}
	return &keyUtil{
		privateKey: privateKey,
		publicKey:  publicKey,
	}
}

func (util *keyUtil) Sign(message string) (signature string, err error) {
	data := []byte(message)
	hashed := sha256.Sum256(data)
	signatureByte, err := rsa.SignPKCS1v15(rand.Reader, util.privateKey, crypto.SHA256, hashed[:])
	if err != nil {
		return
	}
	signature = base64.StdEncoding.EncodeToString(signatureByte)
	return
}

func (util *keyUtil) Verify(message string, signature string) (isVerify bool, err error) {
	messageBytes := []byte(message)
	hashed := sha256.Sum256(messageBytes)
	signatureBytes, err := base64.StdEncoding.DecodeString(signature)
	if err != nil {
		return
	}
	err = rsa.VerifyPKCS1v15(util.publicKey, crypto.SHA256, hashed[:], signatureBytes)
	if err != nil {
		return
	}
	isVerify = true
	return
}
