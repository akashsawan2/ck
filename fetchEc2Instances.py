import boto3

def ec2_instance_types(region_name, input_vcpus, input_memory_gib):
    ec2 = boto3.client("ec2", region_name=region_name)
    describe_args = {}

    while True:
        describe_result = ec2.describe_instance_types(**describe_args)

        for instance_type in describe_result.get("InstanceTypes", []):
            vcpus = instance_type["VCpuInfo"]["DefaultVCpus"]
            memory_gib = instance_type["MemoryInfo"]["SizeInMiB"]/1024 


            if vcpus == input_vcpus and memory_gib == input_memory_gib:
                yield {
                    "InstanceType": instance_type["InstanceType"],
                    "vCPUs": vcpus,
                    "Memory(GiB)": memory_gib
                }

        if "NextToken" in describe_result:
            describe_args["NextToken"] = describe_result["NextToken"]
        else:
            break

def main():
    region_name = 'us-east-1'
    vcpus = 2
    memory_gib = 8

    output_file = "ec2_instance_types.txt"

    with open(output_file, "w") as file:
        found = False
        for instance in ec2_instance_types(region_name, vcpus, memory_gib):
            file.write(f"{instance}\n")
            found = True

    if found:
        print(f"Matching EC2 instances saved to {output_file}")
    else:
        print("No matching EC2 instances found.")

if __name__ == "__main__":
    main()
