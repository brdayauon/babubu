import hashlib

def main():
    sMock = "1369717378de013f81171bb0b1aa279e" # This is the expected MD5 hash for tMock and client_key_value
    tMock = "1747006120" # Example timestamp for mock testing
    client_key_value = "nw3b089qrgw9m7b7i"

    # TRY WITH beginning and NO KEYVAL: 
    withBeginningAndTime = "{}W_ak^moHpMla" + str(tMock)  #+ "," + client_key_value
    x_sign_hash_mock = hashlib.md5(withBeginningAndTime.encode('utf-8')).hexdigest() # This is the MD5 hash
    print(x_sign_hash_mock + " sMock: " + sMock)

    withBeginningAndTimeAndClientKey = "{}W_ak^moHpMla" + str(tMock) + "," + client_key_value
    x_sign_hash_mock2 = hashlib.md5(withBeginningAndTimeAndClientKey.encode('utf-8')).hexdigest() # This is the MD5 hash
    print(x_sign_hash_mock2 + " sMock: " + sMock)


main()