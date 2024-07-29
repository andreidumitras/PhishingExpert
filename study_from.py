import sys
from email import policy                # import modulul "email", de unde am importat submodulul  "policy"
from email.parser import BytesParser      

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: python3 study_from.py [list of eml files]")
        exit()
    path = "../Datasets/phishing/"
    with open(sys.argv[1], 'r') as filelist:
        files = [f.strip() for f in filelist.readlines()]
    for f in files:
        # if ("2307." not in f):
        #     continue
        with open(path + f, "rb") as eml:
            emlobject = BytesParser(policy = policy.default).parse(eml)
        print(f"---------------------------> {f}")
        print(emlobject.get("To"))
        print()