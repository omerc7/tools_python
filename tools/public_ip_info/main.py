import json

import requests


def get_public_ip_info():
    response = requests.get("http://ip-api.com/json/?fields=status,message,query,country,regionName,city,zip,lat,lon,timezone,isp,org,as", timeout=10)
    response.raise_for_status()
    data = response.json()

    if data.get("status") != "success":
        raise Exception(f"API error: {data.get('message', 'Unknown error')}")

    print("Public IP Information")
    print("=" * 40)
    print(f"  IP Address:  {data['query']}")
    print(f"  ISP:         {data['isp']}")
    print(f"  Org:         {data['org']}")
    print(f"  AS:          {data['as']}")
    print(f"  Country:     {data['country']}")
    print(f"  Region:      {data['regionName']}")
    print(f"  City:        {data['city']}")
    print(f"  ZIP:         {data['zip']}")
    print(f"  Lat/Lon:     {data['lat']}, {data['lon']}")
    print(f"  Timezone:    {data['timezone']}")
    print("=" * 40)
    print("\nJSON Output:")
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    get_public_ip_info()
