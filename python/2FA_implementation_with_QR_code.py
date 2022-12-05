import pyotp
import qrcode
import dill
import hmac
import hashlib


def setup_2FA():
    generated_key = pyotp.random_base32()
    totp_setup = pyotp.TOTP(generated_key)
    totp_uri_setup = pyotp.TOTP(generated_key).provisioning_uri(
        name="Avid", issuer_name="avidbox"
    )
    qrcode.make(totp_uri_setup).save("qrcode_totp.png")
    return totp_setup


def verify_pickle():
    with open("totp_object.pkl", "rb") as inp:
        totp_object = dill.load(inp)
    pickled_data = dill.dumps(totp_object)
    secret_key = "25345-abc456"
    digest = hmac.new(secret_key.encode(), pickled_data,
                      hashlib.sha256).hexdigest()
    with open("saved.txt", "r") as hex:
        saved = hex.read()

    return totp_object if hmac.compare_digest(saved, digest) else False


def login_2FA() -> None:
    totp_object = verify_pickle()
    while totp_object:
        input_decrypt_key: str = input("Enter key: ")
        verified_or_not = totp_object.verify(input_decrypt_key)
        if verified_or_not:
            print("Welcome")
            break
        else:
            print("Wrong key. Try again!")


def input_validator() -> str:
    while True:
        user_input: str = input("Enter Your Choice: ")
        if user_input in ("0", "1", "2"):
            return user_input
        else:
            print("Wrong choice. Try again!")


def entry_menu():
    print("1. Log in")
    print("2. Setup 2FA")
    print("0. Exit")
    choice = input_validator()
    match choice:
        case "1":
            login_2FA()
        case "2":
            secret_key = "25345-abc456"
            totp_object = setup_2FA()
            with open("totp_object.pkl", "wb") as outp:
                dill.dump(totp_object, outp, dill.HIGHEST_PROTOCOL)
            pickled_data = dill.dumps(totp_object)
            digest = hmac.new(secret_key.encode(), pickled_data,
                              hashlib.sha256).hexdigest()
            with open("saved.txt", "w") as f:
                f.write(digest)
            print("QR code saved for setup 2FA")
        case "0":
            exit()


if __name__ == "__main__":
    entry_menu()
