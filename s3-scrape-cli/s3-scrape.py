import os
import sys
import json
from urllib import response
import xmltodict
import requests
import validators
from multiprocessing.pool import ThreadPool
import csv
import re
from urllib.parse import unquote
from urllib.request import urlopen


def init_csv():
    fields = ["Status", "URL", "Bucket Url"]
    with open("output.csv", "w+") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(fields)


def write_to_csv(val):
    with open("output.csv", "a") as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(val)


def validate_and_fix_url(url):
    url_valid = validators.url(url)
    if url_valid:
        return url
    else:
        url = "https://" + url
        url_valid = validators.url(url)
        if url_valid:
            return url
        else:
            # print("Please enter a valid url.")
            return None
            # sys.exit()


def generate_s3_permutations(url):
    url = url.replace("https://", "")
    url = url.split(".")
    tld = "s3.amazonaws.com"
    url = url[0:2]
    s3_permutations = [f"{url[0]}.{tld}"]
    for i in range(len(url)):
        for j in range(len(url)):
            if i != j:
                s3_permutations.append(f"{url[i]}.{url[j]}.{tld}")
                s3_permutations.append(f"{url[i]}-{url[j]}.{tld}")
    return s3_permutations


UNIQUE_URLS = []


def get_s3_status(url, og_url):
    print(f"[WORKING] {url}")
    url = validate_and_fix_url(url)
    # print(f"Validating {og_url} -> {url}")
    try:
        res = requests.get(url)
        if res.status_code == 200:
            # res_dict = xmltodict.parse(res.content)
            # print(json.dumps(res_dict, indent=2))
            print(f"[FOUND] {og_url}, access : public ")
            write_to_csv(["PUBLIC", og_url, url])
            return ["PUBLIC", og_url, url]
        elif res.status_code == 403:
            print(f"[FOUND] {og_url}, access : private ")
            write_to_csv(["PRIVATE", og_url, url])
            return ["PRIVATE", og_url, url]
        else:
            if og_url not in UNIQUE_URLS:
                UNIQUE_URLS.append(og_url)
                write_to_csv(["Exists", og_url])
            return ["Exists", og_url]
    except:
        pass
        # write_to_csv(["ERROR", url])
        # return ["ERROR", url]

    # regs3 = r"[\w\-\.]+\.s3\.?(?:[\w\-\.]+)?\.amazonaws\.com|(?<!\.)s3\.?(?:[\w\-\.]+)?\.amazonaws\.com\\?\/[\w\-\.]+"
    # html = unquote(str(res.content))
    # print(html)
    # s3 = re.findall(regs3, html)


def hosted_on_s3_check(url):
    # url = validate_and_fix_url(url)
    try:
        res = requests.get(url)
        if "Server" in res.headers:
            if res.headers["Server"] == "AmazonS3":
                print(
                    f"Files hosted on s3 with header Server : {res.headers['Server']} URL : {url}"
                )
                return url
            else:
                return None
        else:
            return None
    except:
        print(f"[ERROR] {url}")


def generate_subdomains(domain, limit):
    f = open("./subdomains.json")
    data = json.load(f)
    data = data[0:limit]
    sub_list = []
    for sub in data:
        sub_list.append(f"{sub}.{domain}")
    return sub_list


def check_site_exits(url):
    url = validate_and_fix_url(url)
    try:
        code = urlopen(url).code
        if code / 100 >= 4:
            return None
        if code / 100 < 3:
            print(f"[VALID] {url}")
            return url
        else:
            return None
    except:
        pass
        # print(f"[ERROR] {url}")


def validate_and_check_s3_status(url):
    url = check_site_exits(url)
    if url is not None:
        s3_status = hosted_on_s3_check(url)
        if s3_status is not None:
            s3_permutations = generate_s3_permutations(s3_status)
            res_val = []
            for perm in s3_permutations:
                check = get_s3_status(perm, s3_status)
                res_val.append(check)
            if len(res_val) >= 1:
                return s3_status
        else:
            write_to_csv(["No S3", url])
    else:
        return None


def main():
    domain = input("[+] Enter a URL :\n> ")
    limit = input("[+] Enter number of subdomain combinations (<10000) :\n> ")
    limit = int(limit)

    subdomains = generate_subdomains(domain, limit)

    valid_subdomains = []
    pool = ThreadPool()
    init_csv()
    print("Validating subdomains and checking S3 status....\n")
    valid_subdomains = pool.map(validate_and_check_s3_status, subdomains)
    valid_subdomains = list(filter(lambda item: item is not None, valid_subdomains))
    print(f"Total ({len(valid_subdomains)}) buckets found.")
    print(f"Output is written to > {os.getcwd()}/output.csv")
    print(f"Go to http://localhost:8080 to visualise data.")


if __name__ == "__main__":
    main()
