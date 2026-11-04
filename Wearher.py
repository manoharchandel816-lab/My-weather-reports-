import datetime
import requests

today = datetime.date.today()
tomorrow = today + datetime.timedelta(days=1)

print(f"📅 आज की तारीख: {today} | कल की तारीख: {tomorrow}")
print(
    "=========================================================================================="
)
print(
    "  मध्य, पश्चिम एवं दक्षिण भारत - आज और कल का विस्तृत बहु-मॉडल मौसम"
    " पूर्वानुमान"
)
print(
    "==========================================================================================\n"
)

regions = {
    # --- मध्य प्रदेश ---
    "इंदौर/मालवा (मप्र)": {"lat": 22.7196, "lon": 75.8577},
    "भोपाल/मध्य (मप्र)": {"lat": 23.2599, "lon": 77.4126},
    "जबलपुर/महाकौशल (मप्र)": {"lat": 23.1815, "lon": 79.9864},
    "ग्वालियर/चंबल (मप्र)": {"lat": 26.2183, "lon": 78.1828},
    "रीवा/विंध्य (मप्र)": {"lat": 24.5362, "lon": 81.3037},
    "सागर/बुंदेलखंड (मप्र)": {"lat": 23.8388, "lon": 78.7378},
    "खरगोन/निमाड़ (मप्र)": {"lat": 21.8217, "lon": 75.6101},
    # --- राजस्थान ---
    "जयपुर (राजस्थान)": {"lat": 26.9124, "lon": 75.7873},
    "जोधपुर (राजस्थान)": {"lat": 26.2389, "lon": 73.0243},
    "कोटा (राजस्थान)": {"lat": 25.2138, "lon": 75.8648},
    # --- महाराष्ट्र एवं गुजरात ---
    "मुंबई (महाराष्ट्र)": {"lat": 19.0760, "lon": 72.8777},
    "पुणे (महाराष्ट्र)": {"lat": 18.5204, "lon": 73.8567},
    "नागपुर (महाराष्ट्र)": {"lat": 21.1458, "lon": 79.0882},
    "अहमदाबाद (गुजरात)": {"lat": 23.0225, "lon": 72.5714},
    "रायपुर (छत्तीसगढ़)": {"lat": 21.2514, "lon": 81.6296},
    # --- दक्षिण भारत ---
    "बेंगलुरू (कर्नाटक)": {"lat": 12.9716, "lon": 77.5946},
    "चेन्नई (तमिलनाडु)": {"lat": 13.0827, "lon": 80.2707},
    "हैदराबाद (तेलंगाना)": {"lat": 17.3850, "lon": 78.4867},
    "कोची (केरल)": {"lat": 9.9312, "lon": 76.2673},
    "विशाखापत्तनम (आंध्र प्रदेश)": {"lat": 17.6868, "lon": 83.2185},
}

models = {
    "GFS": "gfs_seamless",
    "ECMWF": "ecmwf_ifs025",
    "ICON": "icon_seamless",
    "ACCESS-G": "access_global",
}


def get_status_text(rain):
  if rain >= 1.5:
    return "वर्षा की संभावना है 🌧️"
  elif rain > 0.1:
    return "हल्की फुहारें संभव हैं 🌦️"
  else:
    return "मौसम मुख्य रूप से साफ और सूखा रहेगा ☀️"


for region_name, coords in regions.items():
  print(f"📌 *{region_name}*")

  day_data = {
      "today": {
          "rains": [],
          "winds": [],
          "clouds": [],
          "temps_min": [],
          "temps_max": [],
      },
      "tomorrow": {
          "rains": [],
          "winds": [],
          "clouds": [],
          "temps_min": [],
          "temps_max": [],
      },
  }

  for model_label, model_code in models.items():
    url = f"https://api.open-meteo.com/v1/forecast?latitude={coords['lat']}&longitude={coords['lon']}&daily=precipitation_sum,wind_speed_10m_max,cloud_cover_mean,temperature_2m_min,temperature_2m_max&models={model_code}&forecast_days=2"

    try:
      res = requests.get(url).json()
      daily = res.get("daily", {})

      rain_list = daily.get("precipitation_sum", [0, 0])
      wind_list = daily.get("wind_speed_10m_max", [0, 0])
      cloud_list = daily.get("cloud_cover_mean", [0, 0])
      min_t_list = daily.get("temperature_2m_min", [0, 0])
      max_t_list = daily.get("temperature_2m_max", [0, 0])

      r0 = rain_list[0] if (rain_list and rain_list[0] is not None) else 0.0
      day_data["today"]["rains"].append(max(0.0, r0))
      day_data["today"]["winds"].append(wind_list[0] or 0.0)
      day_data["today"]["clouds"].append(cloud_list[0] or 0.0)
      day_data["today"]["temps_min"].append(min_t_list[0] or 0.0)
      day_data["today"]["temps_max"].append(max_t_list[0] or 0.0)

      if len(rain_list) > 1:
        r1 = (
            rain_list[1] if (rain_list and rain_list[1] is not None) else 0.0
        )
        day_data["tomorrow"]["rains"].append(max(0.0, r1))
        day_data["tomorrow"]["winds"].append(wind_list[1] or 0.0)
        day_data["tomorrow"]["clouds"].append(cloud_list[1] or 0.0)
        day_data["tomorrow"]["temps_min"].append(min_t_list[1] or 0.0)
        day_data["tomorrow"]["temps_max"].append(max_t_list[1] or 0.0)

    except Exception as e:
      pass

  # गणना
  t_rain = (
      sum(day_data["today"]["rains"]) / len(day_data["today"]["rains"])
      if day_data["today"]["rains"]
      else 0.0
  )
  t_wind = (
      sum(day_data["today"]["winds"]) / len(day_data["today"]["winds"])
      if day_data["today"]["winds"]
      else 0.0
  )
  t_cloud = (
      sum(day_data["today"]["clouds"]) / len(day_data["today"]["clouds"])
      if day_data["today"]["clouds"]
      else 0.0
  )
  t_min_t = (
      sum(day_data["today"]["temps_min"]) / len(day_data["today"]["temps_min"])
      if day_data["today"]["temps_min"]
      else 0.0
  )
  t_max_t = (
      sum(day_data["today"]["temps_max"]) / len(day_data["today"]["temps_max"])
      if day_data["today"]["temps_max"]
      else 0.0
  )

  tm_rain = (
      sum(day_data["tomorrow"]["rains"]) / len(day_data["tomorrow"]["rains"])
      if day_data["tomorrow"]["rains"]
      else 0.0
  )
  tm_wind = (
      sum(day_data["tomorrow"]["winds"]) / len(day_data["tomorrow"]["winds"])
      if day_data["tomorrow"]["winds"]
      else 0.0
  )
  tm_cloud = (
      sum(day_data["tomorrow"]["clouds"]) / len(day_data["tomorrow"]["clouds"])
      if day_data["tomorrow"]["clouds"]
      else 0.0
  )
  tm_min_t = (
      sum(day_data["tomorrow"]["temps_min"])
      / len(day_data["tomorrow"]["temps_min"])
      if day_data["tomorrow"]["temps_min"]
      else 0.0
  )
  tm_max_t = (
      sum(day_data["tomorrow"]["temps_max"])
      / len(day_data["tomorrow"]["temps_max"])
      if day_data["tomorrow"]["temps_max"]
      else 0.0
  )

  today_status = get_status_text(t_rain)
  tomorrow_status = get_status_text(tm_rain)

  print(f"   📅 *आज ({today})*:")
  print(
      f"      • स्थिति: {today_status} (अनुमानित वर्षा: ~{t_rain:.1f} मिमी)"
  )
  print(
      f"      • तापमान: {t_min_t:.1f}°C से {t_max_t:.1f}°C | बादल आच्छादन:"
      f" {t_cloud:.0f}% | हवा: {t_wind:.1f} किमी/घंटा"
  )

  print(f"   📅 *कल ({tomorrow})*:")
  print(
      f"      • स्थिति: {tomorrow_status} (अनुमानित वर्षा: ~{tm_rain:.1f} मिमी)"
  )
  print(
      f"      • तापमान: {tm_min_t:.1f}°C से {tm_max_t:.1f}°C | बादल आच्छादन:"
      f" {tm_cloud:.0f}% | हवा: {tm_wind:.1f} किमी/घंटा"
  )

  if t_rain < 0.1 and tm_rain >= 0.1:
    print(
        "   💡 *निष्कर्ष*: आज मौसम मुख्य रूप से साफ रहेगा, लेकिन कल से हल्की"
        " फुहारें शुरू हो सकती हैं।"
    )
  elif t_rain >= 0.1 and tm_rain < 0.1:
    print(
        "   💡 *निष्कर्ष*: आज हल्की फुहारों की संभावना है, परंतु कल से मौसम"
        " पूरी तरह साफ हो जाएगा।"
    )
  elif t_rain >= 0.1 and tm_rain >= 0.1:
    print(
        "   💡 *निष्कर्ष*: आज और कल दोनों दिन बादलों के साथ हल्की फुहारों की"
        " स्थिति बनी रहेगी।"
    )
  else:
    print(
        "   💡 *निष्कर्ष*: आज और कल दोनों दिन मौसम मुख्य रूप से साफ व सूखा"
        " रहेगा।"
    )

  print("=" * 85 + "\n")
