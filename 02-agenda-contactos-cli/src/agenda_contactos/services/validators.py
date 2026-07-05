TOKEN_MISSING = {"", "na", "null", "none"}


class Validators:
    @staticmethod
    def _validate_name(name: str) -> str:
        n = str(name).strip().lower()
        if not n or n in TOKEN_MISSING:
            raise ValueError("nombre_requerido")
        return n

    @staticmethod
    def _validate_telephone(phone: str) -> str:
        ph = str(phone).strip()
        if not ph or ph.lower() in TOKEN_MISSING:
            raise ValueError("telefono_requerido")
        if (not ph.isdigit()) or (not 7 <= len(ph) <= 10):
            raise ValueError("telefono_invalido")
        return ph

    @staticmethod
    def _validate_email(email: str | None) -> str | None:
        if email is None:
            return None

        em = str(email).strip().lower()
        if not em:
            return None

        if "@" not in em:
            raise ValueError("email_invalido")

        local, _, domain = em.partition("@")
        if not local or "." not in domain:
            raise ValueError("email_invalido")

        return em
