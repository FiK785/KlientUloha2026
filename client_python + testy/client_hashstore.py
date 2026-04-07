#!/usr/bin/env python3

import os
import socket

HOST = "127.0.0.1"
PORT = 9000
HASH = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

def metoda_list(sock):
    sock.sendall(b"LIST\n")
    
    header = b""
    #pre istotu to citam po bajtoch
    while not header.endswith(b"\n"):
        header += sock.recv(1)
    print("Server:", header.decode().strip())

    sock.settimeout(1.0)
    data = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
    except:
        pass
    sock.settimeout(None)
    
    print("Zoznam súborov:")
    print(data.decode())

def metoda_upload(sock):
    typ = input("Chces nahrat subor z disku (s) alebo pisat text cez STDIN (t)? ").lower()
    
    if typ == 's':
        nazov = input("Zadaj nazov suboru: ")
        if not os.path.exists(nazov):
            print("Chyba: Subor neexistuje!")
            return
        with open(nazov, "rb") as f:
            data = f.read()
            velkost = len(data)
        popis = f"subor_{nazov}"
    else:
        vstup = input("Napis text, ktory chces nahrat: ")
        nazov_vstupu = input("Zadaj nazov suboru: ")
        data = vstup.encode()
        velkost = len(data)
        popis = nazov_vstupu

    sock.sendall(f"UPLOAD {velkost} {popis}\n".encode())
    sock.sendall(data)
    print("Server:", sock.recv(1024).decode())

def metoda_get(sock):
    h = input("Zadaj hash suboru na stiahnutie: ")
    sock.sendall(f"GET {h}\n".encode())
    
    header = b""
    while not header.endswith(b"\n"):
        header += sock.recv(1)
    print("Server:", header.decode().strip())

    sock.settimeout(1.0)
    data = b""
    try:
        while True:
            chunk = sock.recv(4096)
            if not chunk: break
            data += chunk
    except:
        pass
    sock.settimeout(None)
    
    nazov_suboru = f"down_{h}.txt"
    with open(nazov_suboru, "wb") as f:
        f.write(data)
    print(f"Subor bol ulozeny ako: {nazov_suboru}")

def metoda_delete(sock):
    h = input("Zadaj hash na vymazanie: ")
    sock.sendall(f"DELETE {h}\n".encode())
    print("Server:", sock.recv(1024).decode())

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))
        print("KLIENT SPOJENY SO SERVEROM")

        while True:
            print("\nMOZNOSTI: list, upload, get, delete, koniec")
            prikaz = input("Vyber moznost: ").lower()

            if prikaz == "list": metoda_list(sock)
            elif prikaz == "upload": metoda_upload(sock)
            elif prikaz == "get": metoda_get(sock)
            elif prikaz == "delete": metoda_delete(sock)
            elif prikaz == "koniec": break
            else: print("Neplatny prikaz")

    except Exception as ex:
        print(f"Chyba: {ex}")
    finally:
        sock.close()
        print("Spojenie ukoncene.")

if __name__ == "__main__":
    main()