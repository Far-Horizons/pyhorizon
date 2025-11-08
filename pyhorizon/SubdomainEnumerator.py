#!/usr/bin/env python3
import subprocess

# This class performs the initial subdomain enumeration using subfinder, dnsx, and ffuf
class SubdomainEnumerator:

    def __init__(self, configuration):
        self.domain_name = ""
        self.config = configuration
    
    def run(self):
        self.setup_domain_name()
        self.collector()
        self.check_alive()
        self.check_responsive()
        self.check_accessible()

    # This function sets up the domain name
    def setup_domain_name(self):
        domainparts = self.config.target.split('.')
        for part in domainparts[:-1]:
            if part == domainparts[-2]:
                self.domain_name += part.lower()
            else:
                self.domain_name += part.lower() + "_"
        

    # This funtion collects the subdomains of the target domain
    def collector(self):
        print(f"running subfinder for {self.config.target}...")
        subprocess.run(
            ["subfinder", "-d", self.config.target, "-o", f"domains-{self.domain_name}.txt", "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        print("\nFinished subdomain collection.\n")


    # This function checks which subdomains are alive
    def check_alive(self):
        print("checking which subdomains are alive...")
        subprocess.run(
            ["dnsx", "-l", f"domains-{self.domain_name}.txt", "-o", f"alive-{self.domain_name}.txt", "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
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

