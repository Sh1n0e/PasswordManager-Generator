import json, hashlib, getpass, os, pyperclip, sys
from cryptography.fernet import Fernet

# Function to hash master password
def hashPWD(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode())
    return sha256.hexdigest()

#Secret key
def gen_key():
    return Fernet.generate_key()

#initialize Fernet cipher
def initialize_cipher(key):
    return Fernet(key)

#Encrypting a password
def encrypt_PWD(cipher, password):
    return cipher.encrypt(password.encode()).decode()

#Decrypting password
def decrypt(cipher, encrypted_pwd):
    return cipher.decrypt(encrypted_pwd.encode()).decode()

#Master registration
def register(user, masterpwd):
    #encrypion before storage
    hashed_master_pwd = hashPWD(masterpwd)
    user_data = {'username': user, 'MasterPW': hashed_master_pwd}
    file_name = 'user_data.json'
    #Automated creation of json file to store data
    if os.path.exists(file_name) and os.path.getsize(file_name) == 0:
        with open(file_name, 'w') as file:
            json.dump(user_data, file)
            print("\n[+] You have been registered!")
    else:
        with open(file_name, 'x') as file:
            json.dump(user_data, file)
            print("\n[+] You have been registered!")


#Function to log a user in
def login(username, enterpwd):
    try:
        with open ('user_data.json', 'r') as file:
            user_data = json.load(file)
        #compares the hash of the master pwd to the entered one
        stored_pwd_hash = user_data.get('master_password')
        entered_pwd_hash = user_data.get(enterpwd)
        #Condition if its true
        if entered_pwd_hash == stored_pwd_hash and username == user_data.get('username'):
            print("\n[+] Login Success!\n")
        else:
            print("\n[-] Invalid login, please enter the proper credentials.\n")
            sys.exit()
    except Exception:
        print("\n[-] You have not registered yet, please do it right away.\n")
        sys.exit()


#Function to view websites saved with credentials
def websites_viewed():
    try:
        with open('passwords.json', 'r') as data:
            view = json.load(data)
            print("\nWebsites saved\n")
            for x in view:
                print(x['website'])
            print('\n')
    except FileNotFoundError:
        print("\n[-] You have not saved any passwords.\n")

#Loading/Generating encryption key
key_filename = 'encryption_key.key'
if os.path.exists(key_filename):
   with open(key_filename, 'rb') as key_file:
       key = key_file.read()
else:
   key = gen_key()
   with open(key_filename, 'wb') as key_file:
       key_file.write(key)

cipher = initialize_cipher(key)


#Function to add (and save) passwords
def add_pwd(website, password):
    #check if passwords.json exists
    if not os.path.exists('passwords.json'):
        #initializes an empty list if it doesnt exist
        data = []
    else:
        #Loads current data from passwords
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            #Considers case that json file is empty OR it is an invalid json
            data = []
    #Encrypt pasowrd
    encrypted_pw = encrypt_PWD(cipher, password)
    #Make dictionary for storage
    password_entry = {'website': website, 'password': encrypted_pw}
    data.append(password_entry)
    #Save list back into the json
    with open('passwords.json', 'w') as file:
        json.dump(data, file, indent=4)


# Retrieving saved passwords
def get_pass(website):
    #check if json exists
    if not os.path.exists('passwords.json'):
        return None
    #load existing json
    try:
        with open('passwords.json', 'r') as file:
            data = json.load(file)
    except json.JSONDecodeError:
        data = []

    #loop through all websites to see if required one exists
    for entry in data:
        if entry['website'] == website:
            #decrypt and return password
            decrypted = decrypt(cipher, entry['password'])
            return decrypted
    return None


