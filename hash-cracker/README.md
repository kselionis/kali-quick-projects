# MD5 Dictionary Cracker (Demo)
Εκπαιδευτικό script που προσπαθεί να ανακτήσει MD5 hash με wordlist.

## Χρήση
```bash
python3 md5_cracker.py --hash <md5hex> --wordlist /usr/share/wordlists/rockyou.txt

Kali tip: Το rockyou.txt συχνά έρχεται gz. Ξεζίπαρέ το:

```bash
sudo gzip -d /usr/share/wordlists/rockyou.txt.gz

Παράδειγμα δοκιμής (με δικό σου hash)

```bash
echo -n "password123" | md5sum

# πάρε το 32-hex και μετά:
```bash
python3 md5_cracker.py --hash <το-hex> --wordlist /usr/share/wordlists/rockyou.txt
Νομιμότητα: Χρήση μόνο με ρητή άδεια/σε δικά σου δεδομένα.
