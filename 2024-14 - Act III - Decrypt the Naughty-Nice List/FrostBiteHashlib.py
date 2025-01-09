import traceback
import binascii

class Frostbyte128:
    def __init__(self, file_bytes: bytes, filename_bytes: bytes, nonce_bytes: bytes, hash_length: int = 16):
        self.file_bytes = file_bytes
        self.filename_bytes = filename_bytes
        self.filename_bytes_length = len(self.filename_bytes)
        self.nonce_bytes = nonce_bytes
        self.nonce_bytes_length = len(self.nonce_bytes)
        self.hash_length = hash_length
        self.hash_result = self._compute_hash()

    def _compute_hash(self) -> bytes:
        hash_result = bytearray(self.hash_length)
        count = 0

        for i in range(len(self.file_bytes)):
            xrd = self.file_bytes[i] ^ self.nonce_bytes[i % self.nonce_bytes_length]
            hash_result[count % self.hash_length] = hash_result[count % self.hash_length] ^ xrd
            count += 1

        for i in range(len(self.filename_bytes)):
            count_mod = count % self.hash_length
            count_filename_mod = count % self.filename_bytes_length
            count_nonce_mod = count % self.nonce_bytes_length
            xrd = self.filename_bytes[count_filename_mod] ^ self.nonce_bytes[count_nonce_mod]
            hash_result[count_mod] = hash_result[count_mod] & xrd
            count += 1

        return bytes(hash_result)

    def digest(self) -> bytes:
        """Returns the raw binary hash result."""
        return self.hash_result

    def hexdigest(self) -> str:
        """Returns the hash result as a hexadecimal string."""
        return binascii.hexlify(self.hash_result).decode()

    def update(self, file_bytes: bytes = None, filename_bytes: bytes = None, nonce_bytes: bytes = None):
        """Updates the internal state with new bytes and recomputes the hash."""
        if file_bytes is not None:
            self.file_bytes = file_bytes
        if filename_bytes is not None:
            self.filename_bytes = filename_bytes
        if nonce_bytes is not None:
            self.nonce_bytes = nonce_bytes

        self.hash_result = self._compute_hash()

    def validate(self, hex_string: str):
        """Validates if the provided hex string matches the computed hash."""
        try:
            decoded_bytes = binascii.unhexlify(hex_string)
            if decoded_bytes == self.digest():
                return True, None
        except Exception as e:
            stack_trace = traceback.format_exc()
            return False, f"{stack_trace}"
        return False, None
