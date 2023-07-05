from django.core.management.utils import get_random_secret_key

def main():
    with open("SSLP_Analyzer\\.env","w") as file:
        file.write(f'DJANGO_SECRET_KEY={get_random_secret_key()}\nDATABASE_JSON_FILE = "haplotypes.json"\n')
        
        
main()