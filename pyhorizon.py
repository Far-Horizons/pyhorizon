#!/usr/bin/env python3
import subprocess

# This class performs the initial subdomain enumeration using subfinder, dnsx, and ffuf
class SubdomainEnumerator:

    def __init__(self):
        self.target_domain = ""
        self.domain_name = ""
    
    def run(self):
        self.target_domain = input("Please input the target domain: ").strip()
        self.setup_domain_name()
        self.collector()
        self.check_alive()
        self.check_responsive()
        self.check_accessible()

    # This function sets up the domain name
    def setup_domain_name(self):
        domainparts = self.target_domain.split('.')
        for part in domainparts[:-1]:
            if part == domainparts[-2]:
                self.domain_name += part.lower()
            else:
                self.domain_name += part.lower() + "_"
        

    # This funtion collects the subdomains of the target domain
    def collector(self):
        print(f"running subfinder for {self.target_domain}...")
        subprocess.run(
            ["subfinder", "-d", self.target_domain, "-o", f"domains-{self.domain_name}.txt"],
            check=True
        )
        print("\nFinished subdomain collection.\n")


    # This function checks which subdomains are alive
    def check_alive(self):
        print("checking which subdomains are alive...")
        subprocess.run(
            ["dnsx", "-l", f"domains-{self.domain_name}.txt", "-o", f"alive-{self.domain_name}.txt"],
            check=True
        )
        print("\nFinished checking alive subdomains.\n")


    # This function checks which subdomains are responsive
    def check_responsive(self):
        print("checking which subdomains are responsive...")
        with open(f"responsive-{self.domain_name}.txt", "w") as responsive_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ", "-w", f"alive-{self.domain_name}.txt", "-s"],
                check=True,
                stdout=responsive_file,
                stderr=subprocess.STDOUT
            )
        print("\nFinished checking responsive subdomains.\n")


    # This function checks which subdomains are accessible
    def check_accessible(self):
        print("checking which subdomains are accessible...")
        with open(f"accessible-{self.domain_name}.txt", "w") as accessible_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ", "-w", f"alive-{self.domain_name}.txt", "-s", "-fc", "404,403,401"],
                check=True,
                stdout=accessible_file,
                stderr=subprocess.STDOUT
            )
        print("\nFinished checking accessible subdomains.\n")



if __name__ == "__main__":
    enumerator = SubdomainEnumerator()
    enumerator.run()