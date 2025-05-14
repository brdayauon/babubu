import struct

class _MD5_Processor:
    def __init__(self):
        # These are the initial hash values (RFC uses A, B, C, D).
        # Mapping from the JS snippet's s, c, f, d:
        # JS 's' corresponds to A
        # JS 'c' corresponds to B
        # JS 'f' corresponds to C
        # JS 'd' corresponds to D
        self.A = 0x67452301  # JS s = 1732584193
        self.B = 0xefcdab89  # JS c = -271733879
        self.C = 0x98badcfe  # JS f = -1732584194
        self.D = 0x10325476  # JS d = 271733878

        # T-constants (K values in RFC). These are derived from sine function.
        # The JS code passes these as direct integer arguments.
        # Example: -680876936 (JS) & 0xFFFFFFFF = 0xd76aa478
        self.T = [
            0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee,
            0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501,
            0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be,
            0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821,
            0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa,
            0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8,
            0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed,
            0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a,
            0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c,
            0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70,
            0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05,
            0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665,
            0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039,
            0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1,
            0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1,
            0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391
        ]

        # Shift amounts (S values in RFC)
        self.S = [
            7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  7, 12, 17, 22,  # Round 1 (_ff)
            5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  5,  9, 14, 20,  # Round 2 (_gg)
            4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  4, 11, 16, 23,  # Round 3 (_hh)
            6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21,  6, 10, 15, 21   # Round 4 (_ii)
        ]
        
        # Corresponding T constant indices for the JS code's hardcoded values
        # This mapping is based on the sequence of constants in the JS code
        self.JS_T_INDICES = [
             0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, # p / _ff
            16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, # v / _gg
            32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, # m / _hh
            48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63  # y / _ii
        ]


    def _rotate_left(self, x, n):
        return ((x << n) | (x >> (32 - n))) & 0xFFFFFFFF

    # Round functions F, G, H, I
    # In JS: u._ff, u._gg, u._hh, u._ii
    # Parameters: a, b, c, d are the current hash registers.
    # x_k is a word from the current message block.
    # s_val is the shift amount.
    # t_i is the additive T-constant.
    def _ff(self, a, b, c, d, x_k, s_val, t_i):
        # F(B,C,D) = (B & C) | (~B & D)
        val = a + ((b & c) | (~b & d)) + x_k + t_i
        return (self._rotate_left(val & 0xFFFFFFFF, s_val) + b) & 0xFFFFFFFF

    def _gg(self, a, b, c, d, x_k, s_val, t_i):
        # G(B,C,D) = (B & D) | (C & ~D)
        val = a + ((b & d) | (c & ~d)) + x_k + t_i
        return (self._rotate_left(val & 0xFFFFFFFF, s_val) + b) & 0xFFFFFFFF

    def _hh(self, a, b, c, d, x_k, s_val, t_i):
        # H(B,C,D) = B ^ C ^ D
        val = a + (b ^ c ^ d) + x_k + t_i
        return (self._rotate_left(val & 0xFFFFFFFF, s_val) + b) & 0xFFFFFFFF

    def _ii(self, a, b, c, d, x_k, s_val, t_i):
        # I(B,C,D) = C ^ (B | ~D)
        val = a + (c ^ (b | ~d)) + x_k + t_i
        return (self._rotate_left(val & 0xFFFFFFFF, s_val) + b) & 0xFFFFFFFF

    def _bytes_to_words_little_endian(self, byte_data):
        words = []
        for i in range(0, len(byte_data), 4):
            words.append(struct.unpack('<I', byte_data[i:i+4])[0])
        return words

    def _words_to_bytes_little_endian(self, words_array):
        byte_data = b''
        for word in words_array:
            byte_data += struct.pack('<I', word)
        return byte_data
        
    def hash_message(self, message_input, options=None):
        # Corresponds to the main JS function `u(e, t)`
        if options is None:
            options = {}

        # 1. Input processing (JS `e` -> `message_bytes`)
        if isinstance(message_input, str):
            encoding = options.get("encoding", "utf-8") # Default to utf-8
            if encoding == "binary":
                message_bytes = message_input.encode('latin-1') # Common for "binary"
            else:
                message_bytes = message_input.encode(encoding)
        elif isinstance(message_input, (bytes, bytearray)):
            message_bytes = bytes(message_input)
        elif isinstance(message_input, list) and all(isinstance(x, int) for x in message_input):
            # Assuming list of byte values
            message_bytes = bytes(x & 0xFF for x in message_input)
        else:
            message_bytes = str(message_input).encode('utf-8')

        original_bit_len = len(message_bytes) * 8

        # 2. Create word array and apply padding as per JS logic
        # The JS code seems to work on a word array `n` directly for padding.
        # `l = 8 * e.length` (length of `message_bytes` here)
        # `n = r.bytesToWords(e)`
        
        # First, convert the initial message to words (little-endian).
        # The JS line `n[h] = (n[h] << 8 | n[h] >>> 24) & 16711935 | (n[h] << 24 | n[h] >>> 8) & 4278255360;`
        # ensures words in `n` are little-endian. `_bytes_to_words_little_endian` does this directly.
        
        # Determine total number of words after padding
        # Padded length in bytes must be a multiple of 64.
        # Length field is 8 bytes (64 bits), but JS only uses 4 bytes (32 bits).
        num_message_bytes = len(message_bytes)
        
        # Calculate total length for padding: append 0x80, then pad with 0x00
        # until length is 56 mod 64. Then append 8 bytes for length.
        # JS only uses 4 bytes for length field based on `n[... + 14] = l`.
        final_len_bytes = ((num_message_bytes + 8) // 64 + 1) * 64 # +8 for 0x80 and first part of length field
        if (num_message_bytes % 64) >= 56 : # if not enough space for 0x80 and length field
             final_len_bytes = ((num_message_bytes // 64) + 2) * 64
        else:
             final_len_bytes = ((num_message_bytes // 64) + 1) * 64


        padded_words = [0] * (final_len_bytes // 4)

        # Copy message bytes into word array
        for i in range(num_message_bytes):
            word_idx = i // 4
            byte_shift = (i % 4) * 8
            padded_words[word_idx] |= (message_bytes[i] << byte_shift)

        # Apply JS-style padding to the word array `padded_words` (which is `n` in JS)
        # `l` in JS is `original_bit_len`
        # `n[l >>> 5] |= 128 << (l % 32)`
        word_idx_for_0x80 = original_bit_len >> 5  # original_bit_len // 32
        bit_offset_in_word = original_bit_len % 32
        if word_idx_for_0x80 < len(padded_words): # Ensure index is within bounds
             padded_words[word_idx_for_0x80] |= (0x80 << bit_offset_in_word)
        else: # This case implies message was empty and padding needs word 0
             if original_bit_len == 0 and len(padded_words)>0: # Empty message
                  padded_words[0] |= 0x80


        # `n[(l + 64 >>> 9 << 4) + 14] = l;`
        # This stores the lower 32 bits of original_bit_len at the 14th word
        # (0-indexed) of the *last* 16-word block.
        # The total number of words in padded_words is `final_len_bytes // 4`.
        # The 14th word of the last block is at index `(final_len_bytes // 4) - 2`.
        idx_len_low = (final_len_bytes // 4) - 2
        padded_words[idx_len_low] = original_bit_len & 0xFFFFFFFF
        # The JS code does not seem to store the high part of the length.
        # For a full 64-bit length, it would be:
        # padded_words[(final_len_bytes // 4) - 1] = (original_bit_len >> 32) & 0xFFFFFFFF
        # We will keep it as per JS, so the high word remains 0 from initialization.


        # Initialize hash registers for this computation run
        A = self.A
        B = self.B
        C = self.C
        D = self.D

        # Process message in 16-word (64-byte) chunks
        # `h` in JS is `chunk_offset_words`
        for chunk_offset_words in range(0, len(padded_words), 16):
            M = padded_words[chunk_offset_words : chunk_offset_words + 16]

            # Save current hash values for this block
            # JS: g = s, _ = c, b = f, w = d
            AA = A
            BB = B
            CC = C
            DD = D

            # Round 1 (p / _ff function in JS) - 16 operations
            # JS: s = p(s, c, f, d, n[h + i], shift, T_const) which maps to
            # A = _ff(A, B, C, D, M[i], S[k], T[k])
            # D = _ff(D, A, B, C, M[i], S[k], T[k])
            # C = _ff(C, D, A, B, M[i], S[k], T[k])
            # B = _ff(B, C, D, A, M[i], S[k], T[k])
            # and cycle.
            
            # Order of message words M[k] for Round 1
            m_indices_r1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
            for i in range(16):
                k = m_indices_r1[i]
                s_idx = i
                t_idx = self.JS_T_INDICES[i] # Use the original constants from JS implicit order
                if i % 4 == 0:
                    A = self._ff(A, B, C, D, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 1:
                    D = self._ff(D, A, B, C, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 2:
                    C = self._ff(C, D, A, B, M[k], self.S[s_idx], self.T[t_idx])
                else: # i % 4 == 3
                    B = self._ff(B, C, D, A, M[k], self.S[s_idx], self.T[t_idx])
            
            # Round 2 (v / _gg function in JS) - 16 operations
            m_indices_r2 = [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12]
            for i in range(16):
                k = m_indices_r2[i]
                s_idx = 16 + i
                t_idx = self.JS_T_INDICES[16 + i]
                if i % 4 == 0:
                    A = self._gg(A, B, C, D, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 1:
                    D = self._gg(D, A, B, C, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 2:
                    C = self._gg(C, D, A, B, M[k], self.S[s_idx], self.T[t_idx])
                else: # i % 4 == 3
                    B = self._gg(B, C, D, A, M[k], self.S[s_idx], self.T[t_idx])

            # Round 3 (m / _hh function in JS) - 16 operations
            m_indices_r3 = [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2]
            for i in range(16):
                k = m_indices_r3[i]
                s_idx = 32 + i
                t_idx = self.JS_T_INDICES[32 + i]
                if i % 4 == 0:
                    A = self._hh(A, B, C, D, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 1:
                    D = self._hh(D, A, B, C, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 2:
                    C = self._hh(C, D, A, B, M[k], self.S[s_idx], self.T[t_idx])
                else: # i % 4 == 3
                    B = self._hh(B, C, D, A, M[k], self.S[s_idx], self.T[t_idx])
            
            # Round 4 (y / _ii function in JS) - 16 operations
            m_indices_r4 = [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]
            for i in range(16):
                k = m_indices_r4[i]
                s_idx = 48 + i
                t_idx = self.JS_T_INDICES[48 + i]
                if i % 4 == 0:
                    A = self._ii(A, B, C, D, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 1:
                    D = self._ii(D, A, B, C, M[k], self.S[s_idx], self.T[t_idx])
                elif i % 4 == 2:
                    C = self._ii(C, D, A, B, M[k], self.S[s_idx], self.T[t_idx])
                else: # i % 4 == 3
                    B = self._ii(B, C, D, A, M[k], self.S[s_idx], self.T[t_idx])

            # Add current chunk's hash to result so far
            # JS: s = s + g >>> 0, etc. (>>> 0 ensures unsigned 32-bit)
            A = (A + AA) & 0xFFFFFFFF
            B = (B + BB) & 0xFFFFFFFF
            C = (C + CC) & 0xFFFFFFFF
            D = (D + DD) & 0xFFFFFFFF
            
        # Final result (JS `r.endian([s, c, f, d])`)
        # The JS variables s, c, f, d correspond to our A, B, C, D
        # The `endian` function likely packs them into little-endian bytes.
        return self._words_to_bytes_little_endian([A, B, C, D])


# Wrapper function to mimic the outer JS module's export
def md5_string_processor(input_data, options=None):
    """
    Calculates the MD5 hash of the input_data.
    This function attempts to replicate the behavior of the provided JavaScript snippet.

    Args:
        input_data: The data to hash (string, bytes, list of ints).
        options (dict, optional): A dictionary for options.
                                  Supported: {"encoding": "utf-8" or "binary"}
                                  for string inputs. Defaults to "utf-8".

    Returns:
        str: The MD5 hash as a hexadecimal string.
             (The JS `e.exports` allowed various formats; this defaults to hex)
    """
    processor = _MD5_Processor()
    hashed_bytes = processor.hash_message(input_data, None)
    
    # The original JS `e.exports` could return asBytes, asString (binary), or hex.
    # We'll default to hex as it's most common for MD5.
    output_format = options.get("output_format", "hex") if options else "hex"

    if output_format == "bytes":
        return hashed_bytes
    elif output_format == "binary_string":
        return hashed_bytes.decode('latin-1') # Mimics JS binary string
    else: # hex
        return hashed_bytes.hex()


if __name__ == '__main__':
    # --- Test cases to verify ---
    print("Running test cases...")

    # Expected values can be obtained using standard MD5 tools or Python's hashlib
    # import hashlib
    # hashlib.md5(b"").hexdigest() -> d41d8cd98f00b204e9800998ecf8427e
    # hashlib.md5(b"The quick brown fox jumps over the lazy dog").hexdigest() -> 9e107d9d372bb6826bd81d3542a419d6
    # hashlib.md5(b"Test vector from RFC 1321").hexdigest() -> Not directly, but can test parts.

    test_vectors = [
        ("", "d41d8cd98f00b204e9800998ecf8427e"),
        ("a", "0cc175b9c0f1b6a831c399e269772661"),
        ("abc", "900150983cd24fb0d6963f7d28e17f72"),
        ("message digest", "f96b697d7cb7938d525a2f31aaf161d0"),
        ("abcdefghijklmnopqrstuvwxyz", "c3fcd3d76192e4007dfb496cca67e13b"),
        ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789", "d174ab98d277d9f5a5611c2c9f419d9f"),
        ("The quick brown fox jumps over the lazy dog", "9e107d9d372bb6826bd81d3542a419d6"),
        ("12345678901234567890123456789012345678901234567890123456789012345678901234567890", # 80 chars
         "57edf4a22be3c955ac49da2e2107b67a"),
        #  ('{}W_ak^moHpMla1747006120', '1369717378de013f81171bb0b1aa279e')
        ('{}W_ak^moHpMla,nw3b089qrgw9m7b7i', '7a60edbfa9906d61d4dbfc9ca9ddb226')

    ]

    all_passed = True
    for i, (test_str, expected_hex) in enumerate(test_vectors):
        # Test with string input (default UTF-8)
        # Ensure input_data is bytes for direct comparison if using hashlib
        # Our function handles string to bytes conversion internally
        calculated_hex = md5_string_processor(test_str)
        if calculated_hex == expected_hex:
            print(f"Test {i+1} ('{test_str[:20]}...') with str: PASSED")
        else:
            print(f"Test {i+1} ('{test_str[:20]}...') with str: FAILED")
            print(f"  Expected: {expected_hex}")
            print(f"  Got:      {calculated_hex}")
            all_passed = False

        # Test with bytes input
        calculated_hex_bytes_input = md5_string_processor(test_str.encode('utf-8'))
        if calculated_hex_bytes_input == expected_hex:
            print(f"Test {i+1} ('{test_str[:20]}...') with bytes: PASSED")
        else:
            print(f"Test {i+1} ('{test_str[:20]}...') with bytes: FAILED")
            print(f"  Expected: {expected_hex}")
            print(f"  Got:      {calculated_hex_bytes_input}")
            all_passed = False
            
    # Test "binary" encoding option if applicable (e.g. for specific byte sequences)
    # This tests if the string 'hello\x80world' is treated as those exact bytes
    # Python's hashlib.md5(b'hello\x80world').hexdigest()
    binary_test_str = "hello\x80world" # A string that might be treated as binary
    # Standard MD5 of these bytes:
    import hashlib
    expected_binary_md5 = hashlib.md5(binary_test_str.encode('latin-1')).hexdigest()
    calculated_binary_md5 = md5_string_processor(binary_test_str, options={"encoding": "binary"})

    if calculated_binary_md5 == expected_binary_md5:
        print(f"Test 'binary' encoding: PASSED")
    else:
        print(f"Test 'binary' encoding: FAILED")
        print(f"  Expected: {expected_binary_md5}")
        print(f"  Got:      {calculated_binary_md5}")
        all_passed = False

    if all_passed:
        print("\nAll specific test cases passed!")
    else:
        print("\nSome tests FAILED.")


# md5Processor = _MD5_Processor()
hashedValueHex = md5_string_processor("{}W_ak^moHpMla,nw3b089qrgw9m7b7i", {})
print(hashedValueHex + " expected: " + "7a60edbfa9906d61d4dbfc9ca9ddb226")