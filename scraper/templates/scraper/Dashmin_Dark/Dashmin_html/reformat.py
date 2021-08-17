from pathlib import Path
import re
from pprint import pprint

def change_static_path():
    data = Path("index.html").read_text()
    static = re.compile(r'"assets/[a-zA-Z0-9\./-]+"')
    x = static.findall(data)
    for i in x:
        print(i)
        data = data.replace(i, f'''"{{% static  {i.replace('"',"'")} %}}"''')
        
    Path("index2.html").write_text(data)


    #pprint(data)

change_static_path()

