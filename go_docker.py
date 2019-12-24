import os
import sys

def generate_app_name(input_app_name):
    if input_app_name == "":
        return get_root_path()
    return input_app_name

def get_root_path():
    cwd = os.getcwd()
    
    # handle windows path
    if sys.platform == "win32":
        cwds = cwd.split("\\")
    else:
        cwds = cwd.split("/")

    return cwds.pop()

input_app_name = input("> please input app name, default will be root folder name :")
generated_name = generate_app_name(input_app_name)
main_file_path = input("> please input main file path:")
if main_file_path == "":
    print("main file path can't be empty")
    exit
port_num = input("> plesase input exposed port (if any):")

f = open("Dockerfile", "w")
f.write("FROM golang:alpine AS builder\n\n")
f.write("WORKDIR /app\n")
f.write("ADD . /app\n")
f.write("RUN cd /app & go mod download\n")
f.write(f"RUN cd /app & go build -o {generated_name} {main_file_path}\n\n")
f.write("FROM alpine\n")
f.write("RUN apk update && apk add ca-certificates && rm -rf /var/cache/apk/*\n")
f.write("WORKDIR /app\n")
f.write(f"COPY --from=builder /app/{generated_name} /app\n\n")
if port_num != "":
    f.write(f"EXPOSE {port_num}\n")
f.write(f"ENTRYPOINT ./{generated_name}")