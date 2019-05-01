from random import randint
from random import randrange
from sys import exit

###############################################################################


def text_to_decimal(original_message):

    ttd_translation = "1"
    ttd_original_text_list = list(original_message)
    i = 0

    while i < len(ttd_original_text_list):
        char_temp = str(ord(ttd_original_text_list[i]))
        while len(char_temp) < 3:
            char_temp = "0" + char_temp
        ttd_translation += char_temp
        i += 1

    return(ttd_translation)


def miller_rabin(n):

    """

    *** This code has minor edits ***

    Title: Python implementation of the Miller-Rabin Primality Test
    Author: Ayrx
    Date: 2013
    Code Version: 1.0
    Availability: https://gist.github.com/Ayrx/5884790

    """

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See "http://stackoverflow.com/questions/6325576/how-many-iterations
    # -of-rabin-miller-should-i-use-for-cryptographic-safe-primes"
    # for justification

    # If number is even, it's a composite number

    k = 64

    if n == 2 or n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, s, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def create_lprime(order):
    if order == 1:
        order_string = "first"
    elif order == 2:
        order_string = "second"
    lprime = randint((10 ** 399), ((10 ** 400) - 1))
    if lprime % 2 == 0:
        lprime += 1
    while miller_rabin(lprime) is not True:
        lprime += 2
    print("\nThe " + order_string + " prime number is: " + str(lprime))
    return lprime


def create_public_key(totient):
    public_key_start = 65537
    while ((totient % public_key_start == 0) or
            (miller_rabin(public_key_start) is not True)):
        public_key_start += 2
    return public_key_start


def create_private_key(totient, public_key):

    """

    *** This code has minor edits ***

    Title: Iterative algorithm, Modular inverse
    Author: wikibooks
    Date: 2019
    Code Version: 1.0
    Availability:
    "https://en.wikibooks.org/wiki/Algorithm_Implementation
    /Mathematics/Extended_Euclidean_algorithm#Extended_2"

    """

    # source for below info -->
    # http://www-math.ucdenver.edu/~wcherowi/courses/m5410/exeucalg.html
    # private_key is the inverse of public_key mod totient

    # The algorithm starts by "dividing" n by x. If the last non-zero
    # remainder occurs
    # at step k, then if this remainder is 1, x has an inverse and it is
    # pk+2.

    # (If the remainder is not 1, then x does not have an inverse.)

    def xgcd(a, b):
        """return (g, x, y) such that a*x + b*y = g = gcd(a, b)"""
        x0, x1, y0, y1 = 0, 1, 1, 0
        while a != 0:
            q, b, a = b // a, a, b % a
            y0, y1 = y1, y0 - q * y1
            x0, x1 = x1, x0 - q * x1
        return b, x0, y0

    def mulinv(public_key, totient):
        """return x such that (x * a) % b == 1"""
        g, x, _ = xgcd(public_key, totient)
        if g == 1:
            return x % totient

    return mulinv(public_key, totient)


def create_cipher(decimal_message, public_key, modulus):
    cipher = (int(decimal_message) ** public_key) % modulus
    return cipher


def encrypt_main():

    original_message = input("What is the message that you want to send? ")
    decimal_message = text_to_decimal(original_message)
    print("\nThe encoded string is: " + str(decimal_message))

    prime_one_p = create_lprime(1)
    prime_two_q = create_lprime(2)
    modulus = prime_one_p * prime_two_q
    totient = (prime_one_p - 1) * (prime_two_q - 1)
    public_key = create_public_key(totient)
    private_key = create_private_key(totient, public_key)
    cipher = create_cipher(decimal_message, public_key, modulus)

    print("\nThe modulus is: " + str(modulus))
    print("\nThe totient is: " + str(totient))
    print("\nThe public key is: " + str(public_key))
    print("\nThe private key is: " + str(private_key))
    print("\nThe encrypted message is: " + str(cipher) + "\n")
    main_menu()


###############################################################################


def decrypt_main():

    def decimal_to_text(encoded_message):
        no_one = encoded_message[1:]
        number_split = list(no_one)
        i = 0
        dtt_translation = ""
        dtt_temp = ""

        while i < len(number_split):
            if ((len(dtt_temp) + 1) % 3) == 0:
                dtt_temp += number_split[i]
                dtt_translation += chr(int(dtt_temp))
                dtt_temp = ""
            else:
                dtt_temp += str(number_split[i])
            i += 1

        return dtt_translation

    def decryption(encrypted_message, private_key, modulus):
        decrypted = pow(encrypted_message, private_key, modulus)
        return decrypted

    encrypted_message = int(input("\nWhat is the encrypted message that \
you have obtained? "))

    private_key = int(input("\nWhat is the private key you were given when \
you encrypted the message? "))
    modulus = int(input("\nWhat is the modulus you were given? "))

    decrypted = str(decryption(encrypted_message, private_key, modulus))
    decoded = decimal_to_text(decrypted)

    print(str(decrypted))
    print("\n\n\nThe unencoded message is: " + str(decoded) + "\n\n\n")
    main_menu()

###############################################################################


print("\n")

print("/////////////////////////////////////////////////////////////////////////////////////\n")
print("/////////////     /////   /////     ///////////       /////////////       /////////  ")
print("////     ////     /////   /////     ////     ////     ////              ////     ////")
print("/////////////     /////////////     /////////////     /////////////     /////////////")
print("////                  /////         ////     ////              ////     ////     ////")
print("////                  /////         ////     ////     /////////////     ////     ////")
print("\n/////////////////////////////////////////////////////////////////////////////////////")

print("\nThis encrypts or decrypts RSA information in Python 3")


def main_menu():
    crypt_choice = ((input("Do you need to encrypt or decrypt RSA infor" +
                           "mation? 'E' for encrypt, 'D' for decrypt, " +
                           "'END' to end the program: ")).strip()).upper()
    choice_cor = False

    while choice_cor is not True:
        if crypt_choice == 'E':
            encrypt_main()
            choice_cor = True
        elif crypt_choice == 'D':
            decrypt_main()
            choice_cor = True
        elif crypt_choice == 'END':
            print("\nThank you for using rsa_ed.py!")
            freeze = input("")
            exit()
        else:
            crypt_choice = ((input("You need to input either 'E' to encrypt" +
                                   " or 'D' to decrypt. Please input" +
                                   " 'E', 'D', or 'end': ")).strip()).upper()


main_menu()
