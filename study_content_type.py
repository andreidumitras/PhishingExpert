import sys
from email import policy                # import modulul "email", de unde am importat submodulul  "policy"
from email.parser import BytesParser      
    
def show_parts(emlobj):
    if emlobj.is_multipart():
        i = 0
        for part in emlobj.walk():
            content_disp = part.get("Content-Disposition")
            print(f"Part [{i}]: ", content_disp)
            i += 1
    else:
        content_disp = part.get("Content-Disposition")
        print(f"Part [main]: ", content_disp)
    
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 study_content_type.py [list of eml files]")
        exit()
    path = "../Datasets/ham/"
    with open(sys.argv[1], 'r') as filelist:
        files = [f.strip() for f in filelist.readlines()]
    for f in files:
        # if ("2307." not in f):
        #     continue
        with open(path + f, "rb") as eml:
            emlobject = BytesParser(policy = policy.default).parse(eml)
        print(f"---------------------------> {f}")
        show_parts(emlobject)
        print()