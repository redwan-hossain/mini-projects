import pyotp
import qrcode
import dill


def setup_2FA():
    generated_key = pyotp.random_base32()
    totp_setup = pyotp.TOTP(generated_key)
    totp_uri_setup = pyotp.TOTP(generated_key).provisioning_uri(
        name="Avid", issuer_name="avidbox"
    )
    qrcode.make(totp_uri_setup).save("qrcode_totp.png")
    return totp_setup


def login_2FA() -> None:
    while True:
        input_decrypt_key: str = input("Enter key: ")
        with open("company_data.pkl", "rb") as inp:
            totp_object = dill.load(inp)
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
            totp_object = setup_2FA()
            with open("company_data.pkl", "wb") as outp:
                dill.dump(totp_object, outp, dill.HIGHEST_PROTOCOL)
        case "0":
            exit()


if __name__ == "__main__":
    entry_menu()
