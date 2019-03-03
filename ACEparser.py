#ACEParser by Sketchymoose (@sk3tchymoos3)
#requires acefile and Python3

import os, acefile, hashlib, argparse
cwd = os.getcwd()
parser = argparse.ArgumentParser()
parser.add_argument("working_directory", help="Provide directory with potential ACE RAR files")
args = parser.parse_args()

working_path = args.working_directory
extraction_path = os.path.join(working_path,"extracted")
os.mkdir(extraction_path)

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda : f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()

if (os.path.isdir(working_path) == False): 
    print("[!] Directory does not exist, please check and rerun!")
    exit
else:
    file_listing = os.listdir(working_path)
    output = open(os.path.join(extraction_path,"output.txt"),'w+')
    for filename in file_listing:
        full_path = os.path.join(working_path,filename) 
        #if a file
        if os.path.isfile(full_path):
            #ok now if its an ACE file
            if acefile.is_acefile(full_path):
                output.write(full_path + "\n")
                with acefile.open(full_path) as f:
                    #grab creation date
                    created_on = str(f.datetime)
                    print("Filename: {}".format(filename))
                    print("\tCreated on {}".format(created_on))
                    output.write("\tCreated on: " + created_on + "\n")
                    #ok lets grab all the files
                    toot = f.getmembers()
                    for member in toot:
                        fn = member.filename
                        print("\tName: {}".format(fn))
                        of = os.path.join(extraction_path,member.filename)
                        print("\tSaving as {}".format(of))
                        try:
                            f.extract(member,path=extraction_path)
                        except:
                            continue
                        hash_256 = sha256sum(of)
                        print("\t\tSHA256 of file: {}".format(hash_256))
                        #output to file
                        output.write("\tFilename: "+fn + "\n")
                        output.write("\t\tWritten to Disk: "+of + "\n")
                        output.write("\t\tHash: "+ hash_256 + "\n")
            else:
                continue
    output.close()




