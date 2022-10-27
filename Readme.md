# S3 Bucket Scrapper

A Subdomain extractor and S3 Bucket scrapper written in Python

## Prerequisite

- Docker
- Bash / Zsh Shell
- Python 3

## Getting Started

Clone the directory and run.

`sudo sh setup.sh`

This will :

- Check if docker is installed
- Install Python dependencies
- Build the docker image for the dashboard frontend

## Running the Scrapper

After setup is successful , run

`sh s3-scrape.sh`

This will :

- Start the python script to generate <b>output.csv</b>
- You will be asked to enter a domain. <b>NOTE : Enter domain without protocol prefix i.e. without https:// or http:// </b>
- You will be asked to enter a limit, this refers to how many subdomains are to be generated for scrapping. Currently we have a list of <b>10000</b> [subdomains](https://github.com/ilulale/SECUREU_Assignment/blob/main/s3-scrape-cli/permutations.json).
- Once the csv is generated the script will spin up a dashboard where you can drop the csv file to visualise the data.

## Stack

The following components were used for this stack :

- Scrapper
  - Python
- Dashboard
  - Reactjs
- Automation / Scripting
  - Docker
  - Bash

## This repo is created as a submission for an assignment at SECUREU
