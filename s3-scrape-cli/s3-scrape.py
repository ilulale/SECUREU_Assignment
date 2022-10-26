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


def init_csv():
    fields = ["Status", "URL", "RES Code"]
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
        url = "http://" + url
        url_valid = validators.url(url)
        if url_valid:
            return url
        else:
            # print("Please enter a valid url.")
            return None
            # sys.exit()


def get_s3_status(url):
    og_url = url
    url = validate_and_fix_url(url)
    # print(f"Validating {og_url} -> {url}")
    try:
        res = requests.get(url)
        if res.status_code == 200:
            # res_dict = xmltodict.parse(res.content)
            # print(json.dumps(res_dict, indent=2))
            print(f"[FOUND] {url}, access : public ")
            write_to_csv(["PUBLIC", url, res.status_code])
            return ["PUBLIC", url, res.status_code]
        elif res.status_code == 403:
            print(f"[FOUND] {url}, access : private ")
            write_to_csv(["PRIVATE", url, res.status_code])
            return ["PRIVATE", url, res.status_code]
        else:
            pass
            # write_to_csv(["DOES NOT EXIST", url, res.status_code])
            # return ["DOES NOT EXIST", url, res.status_code]
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
                write_to_csv(["Exists", url])
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
        res = requests.get(url)
        if res.status_code == 200:
            return url
        else:
            return None
    except:
        print(f"Error in {url}")


def main():
    domain = input("[+] Enter a URL :\n> ")

    subdomains = generate_subdomains(domain, 1000)

    valid_subdomains = []
    pool = ThreadPool()
    print("Validating subdomains....\n")
    valid_subdomains = pool.map(check_site_exits, subdomains)
    valid_subdomains = list(filter(lambda item: item is not None, valid_subdomains))
    print(valid_subdomains)

    # pool = ThreadPool()
    # print("Fetching for S3 Buckets....\n")
    # init_csv()
    # result = pool.map(hosted_on_s3_check, domains)
    # result = list(filter(lambda item: item is not None, result))
    # print(result)
    # print(f"Total ({len(result)}) buckets found.")
    # print(f"Output is written to > {os.getcwd()}/output.csv")


if __name__ == "__main__":
    main()
