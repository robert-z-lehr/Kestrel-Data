import pandas as pd
import numpy as np
import os
import re
import json

DATA_DIR = "Data"
OUTPUT_DIR = "Data/web"

os.makedirs(OUTPUT_DIR, exist_ok=True)

def extract_lat_lon(coord_string):
    if pd.isna(coord_string):
        return None, None
    
    match = re.search(r"query=([-0-9.]+),([-0-9.]+)", coord_string)
    if match:
        return float(match.group(1)), float(match.group(2))
    
    return None, None

def load_kestrel_file(filepath):
    df = pd.read_csv(filepath, skiprows=[0, 1, 2, 4])

    for col in df.columns:
        try:
            df[col] = pd.to_numeric(df[col])
        except Exception:
            pass

    return df

def summarize_session(filepath):
    try:
        df = load_kestrel_file(filepath)
        
        # Extract coordinates
        coord_string = df["Location coordinates"].iloc[0]
        lat, lon = extract_lat_lon(coord_string)
        
        if lat is None or lon is None:
            return None
        
        summary = {
            "file_name": os.path.basename(filepath),
            "lat": lat,
            "lon": lon,
        }
        
        numeric_cols = [
            "Temperature",
            "Globe Temperature",
            "Relative Humidity",
            "Wind Speed",
            "Wet Bulb Globe Temperature",
            "TWL"
        ]
        
        for col in numeric_cols:
            if col in df.columns:
                values = pd.to_numeric(df[col], errors='coerce').dropna()
                if len(values) > 0:
                    summary[f"{col}__mean"] = values.mean()
                    summary[f"{col}__min"] = values.min()
                    summary[f"{col}__max"] = values.max()
                    summary[f"{col}__std"] = values.std()
        
        summary["n_points"] = len(df)
        
        return summary
    
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return None

def build_all_sessions():
    summaries = []
    
    for file in os.listdir(DATA_DIR):
        if file.endswith(".csv"):
            path = os.path.join(DATA_DIR, file)
            result = summarize_session(path)
            if result:
                summaries.append(result)
    
    return pd.DataFrame(summaries)

def build_geojson(df):
    features = []
    
    for _, row in df.iterrows():
        props = row.to_dict()
        lat = props.pop("lat")
        lon = props.pop("lon")
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [lon, lat]
            },
            "properties": props
        }
        
        features.append(feature)
    
    return {
        "type": "FeatureCollection",
        "features": features
    }

def main():
    df = build_all_sessions()
    
    csv_path = os.path.join(OUTPUT_DIR, "session_summary.csv")
    geojson_path = os.path.join(OUTPUT_DIR, "sessions.geojson")
    
    df.to_csv(csv_path, index=False)
    
    geojson = build_geojson(df)
    with open(geojson_path, "w") as f:
        json.dump(geojson, f, indent=2)
    
    print("Done. Files written to Data/web/")

if __name__ == "__main__":
    main()