import xerox
import argparse
from blueprints import *

belts = ["transport-belt", "fast-transport-belt", "express-transport-belt"]
undies = ["underground-belt", "fast-underground-belt","express-underground-belt"]
splitter = ["splitter", "fast-splitter", "express-splitter"]

inserter = ["burner-inserter", "inserter", "fast-inserter", "stack-inserter"]

assembler = ["assembling-machine-1","assembling-machine-2","assembling-machine-3"]

def upgrade(blueprint, b, i, a):
    if "blueprint_book" in blueprint.data:
        for x in blueprint.data["blueprint_book"]["blueprints"]:
                if "blueprint" in x:
                    upgradeblueprint(x["blueprint"],b,i,a)
        blueprint = BlueprintBook(data=blueprint.data,version_byte=blueprint.version_byte)
    elif "blueprint" in blueprint.data:
        upgradeblueprint(blueprint.data["blueprint"],b,i,a)
        blueprint = Blueprint(data=blueprint.data,version_byte=blueprint.version_byte)
    return blueprint
        
def upgradeblueprint(blueprint, b, i, a):
    b_cnt, i_cnt, a_cnt = 0,0,0
    for x in blueprint["entities"]:
        b_cnt +=  possiblyreplace(x, b, belts[:])
        b_cnt += possiblyreplace(x, b, undies[:])
        b_cnt += possiblyreplace(x, b, splitter[:])
        i_cnt += possiblyreplace(x, i, inserter[:])
        a_cnt += possiblyreplace(x, a, assembler[:])
    info(b_cnt, i_cnt, a_cnt)

def possiblyreplace(x, n, d):
    if(n<=0):
        return 0
    n-=1
    replacement = d[n]
    d.remove(d[n])
    if(x["name"] in d):
        x["name"] = replacement
        return 1
    return 0

def info(b, i, a):
    if(b>0):
        print("replaced {} belts".format(b))
        print("replaced {} inserter".format(i))
        print("replaced {} assembler".format(a))

def main():
    parser = argparse.ArgumentParser(description="Change items in factorio blue prints")
    parser.add_argument("-b, --belts", type=int, default=0, dest="b")
    parser.add_argument("-i, --inserter", type=int, default=0, dest="i")
    parser.add_argument("-a, --assembler", type=int, default=0, dest="a")
    parser.add_argument("-P --disable_paste", action="store_true", default=False, dest="disablePaste")
    parser.add_argument("-d --display", default=False, action="store_true", dest="display", help="only print the read blueprint dont change anything")
    parser.add_argument("-q --quiet", default=False, action="store_true", dest="silent")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-c, --clipboard", help="read string from clipboard (this is the default)", action="store_true", default=True, dest="clipboard")
    group.add_argument("-s, --string", help="the string is given here", dest="string", default=None)
    group.add_argument("-r --read", help="read from stdin", action="store_true", dest="readstdin", default=False)
    args = parser.parse_args()
    string = ""
    if args.readstdin :
        string = raw_input("reading...")
    elif args.string != None:
        string = args.string
    elif args.clipboard == True:
        string = xerox.paste()
    else:
        ArgumentParser.error("<no input>")
   
    blueprint = Blueprint.from_exchange_string(string)

    if(args.display):
        print(blueprint.to_json_string(indent=4))        
    else:
        upgraded = upgrade(blueprint, args.b, args.i, args.a)
        exchangeString = upgraded.to_exchange_string()
        if not args.disablePaste:
            xerox.copy(exchangeString)
        if not args.silent:
            print(exchangeString)

if __name__ == "__main__":
        main()
