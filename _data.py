import seaborn as sbs
import pandas as pd
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
    csv = pd.read_csv(sys.argv[1])
    df = pd.DataFrame(data=csv)
    
    sbs.countplot(x="IS PHIS", data=df)
    plt.show()
    