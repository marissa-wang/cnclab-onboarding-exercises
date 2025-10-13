import numpy as np
import pandas as pd
from rich import print

filename = '../circle-noise-data/aggregate/grating2AFC_npz.npz'

def struct_to_dict(obj):
    if isinstance(obj, np.ndarray) and obj.dtype.names:
        return {name: struct_to_dict(obj[name]) for name in obj.dtype.names}
    elif isinstance(obj, np.ndarray) and obj.size == 1:
        return struct_to_dict(obj.item())
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    else:
        return obj

data = np.load(filename, allow_pickle=True)
data = data.f.data
print(data)
print(data.dtype.names)

for name in data.files:
    arr = data[name]
    print(f"Processing {name}...")

    if hasattr(arr, 'dtype') and (arr.dtype == object or arr.dtype.names):
        d = struct_to_dict(arr)
        df = pd.json_normalize(d)
        df.to_csv(f"{name}.csv", index=False)
        print(f"Struct saved to {name}.csv")
    elif np.issubdtype(arr.dtype, np.number):
        np.savetxt(f"{name}.csv", arr, delimiter=',')
        print(f"Numeric array saved to {name}.csv")
    else:
        pd.DataFrame(arr).to_csv(f"{name}.csv", index=False)
        print(f"Saved to {name}.csv")

