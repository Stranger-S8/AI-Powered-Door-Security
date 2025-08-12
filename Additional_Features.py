import hashlib
import os.path


class Features:
    def __init__(self):
        pass_path = "data/password.txt"
        if os.path.exists(pass_path):
            with open(pass_path, "r") as f:
                self.file_pass = f.read()


    def generate_password(self, password, filename="password.txt"):
        hashed = hashlib.sha256(password.encode()).hexdigest()

        with open(f"data/{filename}", "w") as f:
            f.write(hashed)

        print("Password Saved Successfully")

    def verify_password(self, password):
        if password is not None:
            hashed = hashlib.sha256(password.encode()).hexdigest()
            return hashed == self.file_pass

if __name__ == "__main__":
    A = Features()
    # A.generate_password("stranger")
    print(A.verify_password("stranger"))
