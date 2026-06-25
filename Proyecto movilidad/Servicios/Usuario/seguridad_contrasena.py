import hashlib
import hmac
import secrets


class SeguridadContrasena:
    ALGORITMO = "pbkdf2_sha256"
    ITERACIONES = 260000

    def generar_hash(self, contrasena):
        salt = secrets.token_hex(16)
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            str(contrasena).encode(),
            salt.encode(),
            self.ITERACIONES,
        ).hex()
        return f"{self.ALGORITMO}${self.ITERACIONES}${salt}${digest}"

    def es_hash(self, contrasena):
        return str(contrasena).startswith(f"{self.ALGORITMO}$")

    def verificar(self, contrasena, guardada):
        if not self.es_hash(guardada):
            return hmac.compare_digest(str(guardada), str(contrasena))

        try:
            _, iteraciones, salt, digest = str(guardada).split("$", 3)
        except ValueError:
            return False

        calculado = hashlib.pbkdf2_hmac(
            "sha256",
            str(contrasena).encode(),
            salt.encode(),
            int(iteraciones),
        ).hex()
        return hmac.compare_digest(digest, calculado)
