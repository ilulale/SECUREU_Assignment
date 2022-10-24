import os
import sys
import json
import xmltodict
import requests
import validators
from multiprocessing.pool import ThreadPool
import csv


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
        url = "https://" + url
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


def get_permutations(url, limit):
    url = url.replace(".com", "")
    perm_data = open("./permutations.json")
    perm_data = json.load(perm_data)
    perm_data = perm_data["permutations"][0:limit]
    perm_arr = []
    for val in perm_data:
        tmp_val = val.replace("%s", url, 1)
        tmp_val = tmp_val.replace("%s", "s3.amazonaws.com")
        perm_arr.append(tmp_val)
    for val in perm_data:
        tmp_val = val.replace("%s", "s3.amazonaws.com.", 1)
        tmp_val = tmp_val.replace("%s", url)
        tmp_val = tmp_val.replace("-", "")
        tmp_val = tmp_val.replace(f".{url}", f"-{url}")
        tmp_val = tmp_val.replace("com.", "com/")
        perm_arr.append(tmp_val)
    return perm_arr


def main():
    domain = input("[+] Enter a URL :\n> ")
    limit = int(
        input("Enter number of permutations (value will be multiplied by 2) :\n> ")
    )
    domain_permutations = get_permutations(domain, limit)
    pool = ThreadPool()
    print("Fetching for S3 Buckets....\n")
    init_csv()
    result = pool.map(get_s3_status, domain_permutations)

    result = list(filter(lambda item: item is not None, result))
    print(f"Total ({len(result)}) buckets found.")
    print(f"Output is written to > {os.getcwd()}/output.csv")

    # for url in domain_permutations:
    #     get_s3_status(url)


if __name__ == "__main__":
    main()
