#!/usr/bin/env python3
import subprocess

# This class performs the initial subdomain enumeration using subfinder, dnsx, and ffuf
class SubdomainEnumerator:

    def __init__(self, configuration):
        self.domain_name = ""
        self.config = configuration
    
    def run(self):
        self.setup_domain_name()
        if self.config.source in ["all", "subfinder"]:
            self.collector_subfinder()
        if self.config.source in ["all", "findomain"]:
            self.collector_findomain()
        self.merge_all_sources()
        self.check_alive()
        self.check_responsive()
        self.check_accessible()

    # This method sets up the domain name
    def setup_domain_name(self):
        domainparts = self.config.target.split('.')
        for part in domainparts[:-1]:
            if part == domainparts[-2]:
                self.domain_name += part.lower()
            else:
                self.domain_name += part.lower() + "_"
        

    # This method collects the subdomains of the target domain using Subfinder
    def collector_subfinder(self):
        self._print_non_silent(f"running subfinder for {self.config.target}...")
        subprocess.run(
            ["subfinder", "-d", self.config.target, "-o", f"domains_subfinder-{self.domain_name}.txt", "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        self._print_non_silent("\nFinished subdomain collection with subfinder.\n")

    # This method collects the subdomains of the target domain using Findomain
    def collector_findomain(self):
        self._print_non_silent(f"running findomain for {self.config.target}...")
        subprocess.run(
            ["findomain", "-t", self.config.target, "-u", f"domains_findomain-{self.domain_name}.txt", "-q"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        self._print_non_silent("\nFinished subdomain collection with findomain.\n")

    def merge_all_sources(self):
        self._print_non_silent("merging subdomain lists from all sources...")
        if self.config.source == "all":
            self.merge_lists(f"domains_subfinder-{self.domain_name}.txt",
                             f"domains_findomain-{self.domain_name}.txt",
                             f"domains_all-{self.domain_name}.txt"
                             )
            if not self.config.keep_temp:
                subprocess.run(
                    ["rm", f"domains_subfinder-{self.domain_name}.txt", f"domains_findomain-{self.domain_name}.txt"],
                    check=True
                )
        elif self.config.source == "subfinder":
            if not self.config.keep_temp:
                subprocess.run(
                    ["mv", f"domains_subfinder-{self.domain_name}.txt", f"domains_all-{self.domain_name}.txt"],
                    check=True
                )
            else:
                subprocess.run(
                    ["cp", f"domains_subfinder-{self.domain_name}.txt", f"domains_all-{self.domain_name}.txt"],
                    check=True
                )
        elif self.config.source == "findomain":
            if not self.config.keep_temp:
                subprocess.run(
                    ["mv", f"domains_findomain-{self.domain_name}.txt", f"domains_all-{self.domain_name}.txt"],
                    check=True
                )
            else:
                subprocess.run(
                    ["cp", f"domains_findomain-{self.domain_name}.txt", f"domains_all-{self.domain_name}.txt"],
                    check=True
                )
        self._print_non_silent("\nFinished merging subdomain lists.\n")



    # This method checks which subdomains are alive
    def check_alive(self):
        self._print_non_silent("checking which subdomains are alive...")
        subprocess.run(
            ["dnsx", "-l", f"domains_all-{self.domain_name}.txt", "-o", f"alive-{self.domain_name}.txt", "-silent"],
            check=True,
            stdout=subprocess.DEVNULL
        )
        self._print_non_silent("\nFinished checking alive subdomains.\n")


    # This method checks which subdomains are responsive
    def check_responsive(self):
        self._print_non_silent("checking which subdomains are responsive...")
        with open(f"responsive-{self.domain_name}.txt", "w") as responsive_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ", "-w", f"alive-{self.domain_name}.txt", "-s"],
                check=True,
                stdout=responsive_file,
                stderr=subprocess.STDOUT
            )
        self._print_non_silent("\nFinished checking responsive subdomains.\n")


    # This method checks which subdomains are accessible
    def check_accessible(self):
        self._print_non_silent("checking which subdomains are accessible...")
        with open(f"accessible-{self.domain_name}.txt", "w") as accessible_file:
            subprocess.run(
                ["ffuf", "-u", "https://FUZZ", "-w", f"alive-{self.domain_name}.txt", "-s", "-fc", "404,403,401"],
                check=True,
                stdout=accessible_file,
                stderr=subprocess.STDOUT
            )
        self._print_non_silent("\nFinished checking accessible subdomains.\n")


    #helper methods===============================================================================

    # helper method to print only if not in silent mode
    def _print_non_silent(self, stringtoprint):
        if self.config.verbosity >= 0:
            print(stringtoprint)

    # helper method for normalizing URLS, to a format like "subdomain.subdomain.domain.extension"
    def _normalize_domain(self, domain):
        if not domain:
            return None
        d = domain.strip()
        d = d.split("://", 1)[-1] # remove http(s)://
        d = d.split("/", 1)[0] # remove trailing / or entire paths
        if d.startswith("*."): # remove wildcard prefix
            d = d[2:]
        d = d.lower()

        # sanity checks:
        if not d:       # empty domain
            return None
        if " " in d:    # domain with spaces
            return None
        if d.count(".") < 1:  # domain without extension
            return None
        if d.count("..") > 0: # domain with double dots
            return None
        
        return d
    
    def merge_lists(self, filename1, filename2, output_filename):
        unique_domains = set()

        # Read domains from the first file
        with open(filename1, 'r') as file1:
            for line in file1:
                normalized_domain = self._normalize_domain(line)
                if normalized_domain:
                    unique_domains.add(normalized_domain)

        # Read domains from the second file
        with open(filename2, 'r') as file2:
            for line in file2:
                normalized_domain = self._normalize_domain(line)
                if normalized_domain:
                    unique_domains.add(normalized_domain)

        # Write the unique domains to the output file
        with open(output_filename, 'w') as output_file:
            for domain in sorted(unique_domains):
                output_file.write(domain + '\n')
