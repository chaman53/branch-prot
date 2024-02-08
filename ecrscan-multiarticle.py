from json import loads, dumps
import json
import subprocess
import csv

class Vulnurability:
    repo_name: str = ""
    pack_name: str = ""
    pack_version: str = ""
    image_id: str = ""
    title: str = ""
    packageManager: str = ""
    status: str = ""
    severity: str = ""
    description: str = ""
    remediation: str = ""
repos = []
list_critical = []
findings = []


#def get_all_repos():
#    get_repos = subprocess.Popen("aws ecr describe-repositories", stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#    json_repo_result = json.loads(get_repos.stdout.read())
#    repositories = json_repo_result["repositories"]
#    print(f'Number of repos: {len(repositories)}')
#    return repositories

#def get_latest_img_digest(repo_name):
#    get_latest_image_cmd = f"aws ecr describe-images --repository-name pnlp-prod-ml-multiarticle-summarisation-openai --query 'sort_by(imageDetails,& imagePushedAt)[-1].imageDigest'"
#    get_latest_image = subprocess.Popen(get_latest_image_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#    image_Digest = get_latest_image.stdout.read().decode('utf-8')
    #print(f'image_Digest: {image_Digest}')
#    return image_Digest

#def start_scanning(repo_name, image_Digest):
#    start_scan_cmd = f"aws ecr start-image-scan --repository-name pnlp-prod-ml-multiarticle-summarisation-openai --image-id imageDigest=sha256:b1e86b673cf6f5cd68d2f65a125cd1c72b32eee1d04dd09a91a334e031ce7f34"
#    start_scan = subprocess.Popen(start_scan_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#    scan_result = start_scan.stdout.read().decode('utf-8')
    # print(f'scan_result: {scan_result}')
#    return scan_result

#def wait_scan_results(repo_name, image_Digest):
#    wait_scan_cmd = f"aws ecr wait image-scan-complete --repository-name pnlp-prod-ml-multiarticle-summarisation-openai --image-id imageDigest=sha256:b1e86b673cf6f5cd68d2f65a125cd1c72b32eee1d04dd09a91a334e031ce7f34"
#    wait_scan = subprocess.Popen(wait_scan_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
#    wait_scan.stdout.read().decode('utf-8')

def get_scan_result(repo_name, image_Tag):
    cmd_finding = f"aws ecr describe-image-scan-findings --repository-name pnlp-uat-ml-multiarticle-summarisation-openai --image-id imageTag=latest"
    get_findings = subprocess.Popen(cmd_finding, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    result = json.loads(get_findings.stdout.read())
    return result

def finding_vulnerablity(repo_name, json_finding_result):
    print_to_json( json_finding_result['imageScanFindings']['enhancedFindings'])
    for result in json_finding_result['imageScanFindings']['enhancedFindings']:
        item  = Vulnurability()
        item.title = result['title']
        vulnerablePackage = result['packageVulnerabilityDetails']['vulnerablePackages']
        for vuln in vulnerablePackage:
            item.packageManager = vuln["packageManager"]
        item.status = result['status']
        item.severity = result['severity']
        item.description = result['description']
        item.remediation = result['remediation']
        list_critical.append(item)
         #   attributes = result["attributes"]

    #        for att in attributes:
     #           if(att["key"] == "package_name"):
      #              item.pack_name = att["value"]
       #         if(att["key"] == "package_version"):
        #            item.pack_version = att["value"]

def write_to_csv(list_critical):
    if(len(list_critical) > 0):
        csv_columns = ["Name","package_name","severity","description","status","remediation"]
        with open("report-multiarticle.csv", 'w', newline='', encoding='utf8') as f:
            writer = csv.writer(f)
            writer.writerow(csv_columns)
            for ob in list_critical:
                row = [ob.title,ob.packageManager,ob.severity,ob.description,ob.status,ob.remediation]
                writer.writerow(row)

def print_to_json(data):
    with open('data.json', 'w') as f:
        json.dump(data, f)

def main():
    # get all the repos
    #repositories = get_all_repos()

    #for repo in repositories:
        #repo_name = repo["repositoryName"]
        #print(f" --> repo_name: {repo_name}")
        #print (f'------------- Starting scanning : {repo_name}')

        # get latest image for the repo
        #image_Digest = get_latest_img_digest(repo_name)

        #print(f'------------- Started the scanning: {repo_name}')
        #start_scanning(repo_name, image_Digest)

        # waiting scan result
        #print(f'------------- Waiting to finish the scanning: {repo_name}')
        #wait_scan_results(repo_name, image_Digest)

        # get scan results
    json_finding_result = get_scan_result('pnlp-uat-ml-multiarticle-summarisation-openai', 'latest')

    #image_scan = json_finding_result['imageScanFindings']
    status = json_finding_result['imageScanStatus']['status']
    #text_file = open("sample.txt", "w")
    #n = text_file.write(image_scan)
    #text_file.close()
    print(f'Status of scan: {status}', json_finding_result)
    #if(status == "FAILED"):
        #print(f'>>>>>>>>>>>>>>>>>>>Failed to scan the repo: {repo_name}')
        #continue

        # finding vulnarabilities
    finding_vulnerablity('pnlp-uat-ml-multiarticle-summarisation-openai', json_finding_result)

        # write all critical issues to csv file
    write_to_csv(list_critical)

    print(f'Repos with issues: {len(list_critical)}')
    print(f'=====================================================')

if __name__ == "__main__":
    main()
