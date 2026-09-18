from pytrends.request import TrendReq
import pandas as pd
from datetime import datetime, timezone

KEYWORDS = [
    "n8n workflow",
    "n8n automation",
    "n8n AI agent",
    "n8n Gmail automation",
    "n8n WhatsApp automation",
    "n8n Google Sheets automation",
    "n8n CRM automation",
]

pytrends = TrendReq(
    hl="en-US",
    tz=330
)

records = []

for country in ["US", "IN"]:
    for keyword in KEYWORDS:

        try:
            pytrends.build_payload(
                [keyword],
                cat=0,
                timeframe="today 3-m",
                geo=country,
                gprop=""
            )

            data = pytrends.interest_over_time()

            if data.empty:
                continue

            values = data[keyword]

            current_interest = int(values.iloc[-1])
            average_interest = float(values.mean())

            first_value = float(values.iloc[0])
            last_value = float(values.iloc[-1])

            if first_value > 0:
                growth_percent = (
                    (last_value - first_value)
                    / first_value
                ) * 100
            else:
                growth_percent = 0

            records.append({
                "keyword": keyword,
                "country": country,
                "current_interest": current_interest,
                "average_interest": round(
                    average_interest, 2
                ),
                "growth_percent": round(
                    growth_percent, 2
                ),
                "source_platform": "google_trends",
                "collected_at": datetime.now(
                    timezone.utc
                ).isoformat()
            })

        except Exception as e:
            print(
                f"Failed: {keyword} / {country}: {e}"
            )

df = pd.DataFrame(records)

if not df.empty:
    max_interest = df["current_interest"].max()
    max_average = df["average_interest"].max()

    df["interest_score"] = (
        df["current_interest"] / max_interest * 100
        if max_interest > 0 else 0
    )

    df["average_score"] = (
        df["average_interest"] / max_average * 100
        if max_average > 0 else 0
    )

    # Growth can be negative, so convert it into a non-negative score
    min_growth = df["growth_percent"].min()
    max_growth = df["growth_percent"].max()

    if max_growth != min_growth:
        df["growth_score"] = (
            (df["growth_percent"] - min_growth)
            / (max_growth - min_growth)
            * 100
        )
    else:
        df["growth_score"] = 0

    df["popularity_score"] = (
        df["interest_score"] * 0.50
        + df["average_score"] * 0.30
        + df["growth_score"] * 0.20
    ).round(2)

    df["interest_score"] = df["interest_score"].round(2)
    df["average_score"] = df["average_score"].round(2)
    df["growth_score"] = df["growth_score"].round(2)
    
df.to_json(
    "google_trends_data.json",
    orient="records",
    indent=2
)

print(f"Collected {len(df)} records")
print(df)