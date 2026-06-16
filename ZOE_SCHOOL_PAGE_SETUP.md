# Zoe School Page — Full Setup Guide
## Target: `kendi-ng.com/zoe-school`
## Repo: `https://github.com/hkkendi/kendi-ng-dev.git`

---

## STEP 1 — Create the page file

Create the file at:
```
/zoe-school/index.html
```
(or `/pages/zoe-school.tsx` if your site is Next.js — adjust path to match your framework)

Paste the full HTML below into that file.

---

## STEP 2 — Create the data file (update dates here)

Create:
```
/zoe-school/data/schools.json
```

Paste this JSON — **this is the file you update when dates are confirmed**:

```json
{
  "lastUpdated": "2026-05-28",
  "child": {
    "name": "Zoe",
    "dob": "2024-02-21",
    "dobDisplay": "21 Feb 2024"
  },
  "timeline": [
    {
      "date": "Jul–Aug 2026",
      "zh": "各校開放日 / 簡介會，建議出席",
      "en": "School open days & info sessions — strongly recommended to attend"
    },
    {
      "date": "Sep 2026",
      "zh": "主要K1申請期：嘉諾撒聖心、堅道真光、大坑真光、聖保祿、培正、九龍真光、沙田培正等。同步向教育局申請「幼稚園入學註冊證」",
      "en": "Main K1 application window: SHCK, True Light, SPK, Pui Ching, Maryknoll KG, Heep Yunn KG, etc. Apply to EDB for Kindergarten Registration Certificate at same time."
    },
    {
      "date": "Oct 2026",
      "zh": "聖士提反幼稚園申請；拔萃女幼稚園、德望幼稚園、嘉諾撒聖方濟各等申請期；各校陸續安排面試",
      "en": "SSGS KG, DGS KG, GSKD KG, Canossian SFX application windows open. Schools begin scheduling interviews."
    },
    {
      "date": "Nov 2026",
      "zh": "各校進行面試，陸續公佈取錄結果",
      "en": "Interviews held at most schools; rolling admission results released."
    },
    {
      "date": "Dec 2026",
      "zh": "各校正式公佈取錄結果",
      "en": "Official admission results announced by all schools."
    },
    {
      "date": "8–10 Jan 2027",
      "zh": "教育局統一註冊日期，辦理正式註冊（只可選一所學校）",
      "en": "EDB Unified Registration Date — complete registration at ONE chosen school only."
    }
  ],
  "schools": [
    {
      "id": "spk",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "聖保祿幼稚園 SPK",
      "nameEn": "St. Paul's Kindergarten",
      "address": "銅鑼灣禮頓道 Leighton Rd, CWB",
      "feederZh": "聖保祿學校（小學部）",
      "feederEn": "St. Paul's Co-ed Primary",
      "rankingZh": "全港小學排名 #2",
      "rankingEn": "Primary Rank #2 HK-wide",
      "rankingSource": "HappySeeds/LeadingEd 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online 網上",
      "website": "https://www.spk.edu.hk",
      "estAppPeriod": "Mid-Sep to Early Oct 2026 / 預計2026年9月中至10月初",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. mid-Sep 2026",
      "status": "pending"
    },
    {
      "id": "ssgs",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "聖士提反女子中學附屬幼稚園",
      "nameEn": "SSGS Affiliated KG",
      "address": "中環柏道 Park Rd, Central",
      "feederZh": "聖士提反附屬小學",
      "feederEn": "SSGS Affiliated Primary",
      "rankingZh": "全港小學排名 約#15-20",
      "rankingEn": "Primary Rank ~#15-20 HK-wide",
      "rankingSource": "SundayKiss/Toby 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online (eClass) 網上",
      "website": "https://www.ssgckg.edu.hk",
      "estAppPeriod": "Oct 1–15, 2026 / 預計2026年10月1-15日",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. Oct 1–15, 2026",
      "status": "pending"
    },
    {
      "id": "shck",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "嘉諾撒聖心幼稚園 SHCK",
      "nameEn": "Sacred Heart Canossian KG",
      "address": "中環羅便臣道 Robinson Rd, Central",
      "feederZh": "嘉諾撒聖心學校",
      "feederEn": "Sacred Heart Canossian Primary",
      "rankingZh": "全港小學排名 約#10-15",
      "rankingEn": "Primary Rank ~#10-15 HK-wide",
      "rankingSource": "HKeTIME/Toby 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online 網上",
      "website": "https://www.shck.edu.hk",
      "estAppPeriod": "Late Sep 2026, ~1 week / 預計2026年9月下旬約一週",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. late Sep 2026",
      "status": "pending"
    },
    {
      "id": "truelight_caine",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "香港真光幼稚園（堅道）",
      "nameEn": "True Light KG (Caine Rd)",
      "address": "中環堅道 Caine Rd, Central",
      "feederZh": "香港真光中學附屬小學",
      "feederEn": "True Light Primary HK",
      "rankingZh": "全港小學排名 約#20-30",
      "rankingEn": "Primary Rank ~#20-30 HK-wide",
      "rankingSource": "Toby/NoteSity 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "In-person / Post 親身/郵寄",
      "website": "https://www.truelightk-c.edu.hk",
      "estAppPeriod": "Sep 15–26, 2026 / 預計2026年9月15-26日",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. Sep 15–26, 2026",
      "status": "pending"
    },
    {
      "id": "truelight_taihang",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "大坑真光幼稚園",
      "nameEn": "True Light KG (Tai Hang)",
      "address": "大坑道50號 50 Tai Hang Rd",
      "feederZh": "香港真光中學附屬小學",
      "feederEn": "True Light Primary HK",
      "rankingZh": "全港小學排名 約#20-30",
      "rankingEn": "Primary Rank ~#20-30 HK-wide",
      "rankingSource": "Toby/NoteSity 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Call 2577 3569",
      "website": "https://www.tlmshkps.edu.hk/kindergarten",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC — call 2577 3569",
      "status": "pending"
    },
    {
      "id": "sfx",
      "district": "hki",
      "districtLabel": "Hong Kong Island 香港島",
      "nameZh": "嘉諾撒聖方濟各學校幼稚園",
      "nameEn": "Canossian School KG (SFX)",
      "address": "堅尼地城薄扶林道 Pok Fu Lam Rd, Kennedy Town",
      "feederZh": "嘉諾撒聖方濟各學校（小學部）",
      "feederEn": "Canossian School Primary Section",
      "rankingZh": "全港小學排名 約#10-18",
      "rankingEn": "Primary Rank ~#10-18 HK-wide",
      "rankingSource": "Toby/HKeTIME 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online 網上",
      "website": "https://www.sfxcanossian.edu.hk",
      "estAppPeriod": "Late Sep–Oct 2026 / 預計2026年9月下旬至10月",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. late Sep–Oct 2026",
      "status": "pending"
    },
    {
      "id": "puiching_kln",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "培正幼稚園",
      "nameEn": "Pui Ching KG",
      "address": "九龍城培正道 Pui Ching Rd, Kowloon City",
      "feederZh": "香港培正小學",
      "feederEn": "Pui Ching Primary School HK",
      "rankingZh": "全港小學排名 約#8-12",
      "rankingEn": "Primary Rank ~#8-12 HK-wide",
      "rankingSource": "HKeTIME/Toby 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online (eClass) 網上",
      "website": "https://www.pcps.edu.hk/kg",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    },
    {
      "id": "lasalle",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "喇沙幼稚園",
      "nameEn": "La Salle KG",
      "address": "九龍城喇沙利道 La Salle Rd, Kowloon City",
      "feederZh": "喇沙小學",
      "feederEn": "La Salle Primary School",
      "rankingZh": "全港小學排名 #2男校 / 約#4-5全港",
      "rankingEn": "Primary Rank #2 (Boys) / ~#4-5 HK-wide",
      "rankingSource": "HappySeeds/LeadingEd 2025-26",
      "session": "Full Day",
      "sessionZh": "全日班",
      "appMethod": "Online / In-person 網上/親身",
      "website": "https://www.lasallek.edu.hk",
      "estAppPeriod": "Late Sep–Oct 2026 / 預計2026年9月下旬至10月",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. late Sep–Oct 2026",
      "status": "pending"
    },
    {
      "id": "dgs",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "拔萃女幼稚園",
      "nameEn": "DGS KG",
      "address": "九龍塘牛津道 Oxford Rd, Kowloon Tong",
      "feederZh": "拔萃女小學",
      "feederEn": "Diocesan Girls' Junior School",
      "rankingZh": "全港小學排名 #1女校 / 全港第一",
      "rankingEn": "Primary Rank #1 (Girls) / #1 HK-wide",
      "rankingSource": "HappySeeds/ParentingHeadline 2025-26",
      "session": "Full Day",
      "sessionZh": "全日班",
      "appMethod": "Online 網上",
      "website": "https://www.dgskg.edu.hk",
      "estAppPeriod": "Oct 2026, TBC / 預計2026年10月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026. Register early — fills within hours.",
      "appDateConfirmed": null,
      "appDateNote": "Est. Oct 2026",
      "status": "pending"
    },
    {
      "id": "truelight_kln",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "九龍真光幼稚園",
      "nameEn": "KL True Light KG",
      "address": "九龍塘真光里 Kowloon Tong",
      "feederZh": "九龍真光中學附屬小學",
      "feederEn": "KL True Light Primary",
      "rankingZh": "全港小學排名 約#25-35",
      "rankingEn": "Primary Rank ~#25-35 HK-wide",
      "rankingSource": "NoteSity 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "In-person / Post 親身/郵寄",
      "website": "https://www.kltkps.edu.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    },
    {
      "id": "gskd",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "德望幼稚園",
      "nameEn": "Good Hope School KG",
      "address": "九龍塘筆架山道 Beacon Hill Rd, Kowloon Tong",
      "feederZh": "德望學校（小學部）",
      "feederEn": "Good Hope School Primary",
      "rankingZh": "全港小學排名 約#5-8",
      "rankingEn": "Primary Rank ~#5-8 HK-wide",
      "rankingSource": "HappySeeds/Toby 2025-26",
      "session": "Full Day",
      "sessionZh": "全日班",
      "appMethod": "Online 網上",
      "website": "https://www.gskd.edu.hk",
      "estAppPeriod": "Mid-Sep–Oct 2026 / 預計2026年9月中至10月",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "Est. mid-Sep–Oct 2026",
      "status": "pending"
    },
    {
      "id": "maryknoll",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "瑪利諾修院學校幼稚園",
      "nameEn": "Maryknoll Convent School KG",
      "address": "九龍城農圃道 Farm Rd, Kowloon City",
      "feederZh": "瑪利諾修院學校（小學部）",
      "feederEn": "Maryknoll Convent School Primary",
      "rankingZh": "全港小學排名 #2-3女校 / 約#3全港",
      "rankingEn": "Primary Rank #2-3 (Girls) / ~#3 HK-wide",
      "rankingSource": "HappySeeds/ParentingHeadline 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班，無全日班）",
      "appMethod": "Online 網上",
      "website": "https://www.mcsps.edu.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    },
    {
      "id": "heepyunn",
      "district": "kln",
      "districtLabel": "Kowloon 九龍區",
      "nameZh": "協恩中學附屬幼稚園",
      "nameEn": "Heep Yunn School Private KG",
      "address": "九龍城農圃道1號 1 Farm Rd, Kowloon City",
      "feederZh": "協恩中學附屬小學",
      "feederEn": "Heep Yunn School Primary Section",
      "rankingZh": "全港小學排名 約#4-6女校 ⚠️ 逾2000人爭60位",
      "rankingEn": "Primary Rank ~#4-6 (Girls) HK-wide ⚠️ 2,000+ applicants for 60 places",
      "rankingSource": "HK01/HappySeeds 2025-26",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班，無全日班）",
      "appMethod": "Online 網上",
      "website": "https://www.hykg.edu.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026. Register ASAP — extremely oversubscribed.",
      "appDateConfirmed": null,
      "appDateNote": "TBC — check website from Jul 2026",
      "status": "pending"
    },
    {
      "id": "puiching_st",
      "district": "sha",
      "districtLabel": "Shatin 沙田區",
      "nameZh": "沙田培正幼稚園",
      "nameEn": "ST Pui Ching KG",
      "address": "沙田源禾路 Yuen Wo Rd, Shatin",
      "feederZh": "沙田培正小學",
      "feederEn": "ST Pui Ching Primary School",
      "rankingZh": "全港小學排名 約#15-20",
      "rankingEn": "Primary Rank ~#15-20 HK-wide",
      "rankingSource": "Toby/NoteSity 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online 網上",
      "website": "https://www.stpcps.edu.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    },
    {
      "id": "yunchuen",
      "district": "sha",
      "districtLabel": "Shatin 沙田區",
      "nameZh": "雲泉學校附屬幼稚園",
      "nameEn": "Yun Chuen Affiliated KG",
      "address": "沙田 Shatin",
      "feederZh": "道聯會雲泉學校",
      "feederEn": "Yun Chuen School",
      "rankingZh": "沙田區優質津貼小學 全港約#40-60",
      "rankingEn": "Quality aided primary, Shatin. HK-wide ~#40-60",
      "rankingSource": "NoteSity district ranking 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online / In-person 網上/親身",
      "website": "https://www.yunchuen.edu.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    },
    {
      "id": "lingliang",
      "district": "sha",
      "districtLabel": "Shatin 沙田區",
      "nameZh": "靈糧堂幼稚園",
      "nameEn": "Ling Liang KG",
      "address": "沙田瀝源邨 Lek Yuen Estate, Shatin",
      "feederZh": "靈糧堂劉梅軒中學（直屬小學）",
      "feederEn": "Ling Liang Affiliated Primary",
      "rankingZh": "沙田區優質津貼小學 全港約#50-70",
      "rankingEn": "Quality aided primary, Shatin. HK-wide ~#50-70",
      "rankingSource": "NoteSity district ranking 2026",
      "session": "Half Day",
      "sessionZh": "半日班（上午及下午班）",
      "appMethod": "Online 網上",
      "website": "https://www.lingliang.org.hk",
      "estAppPeriod": "Sep 2026, TBC / 預計2026年9月，待公佈",
      "openDay": null,
      "openDayNote": "Usually Saturday, Jul–Aug 2026",
      "appDateConfirmed": null,
      "appDateNote": "TBC",
      "status": "pending"
    }
  ]
}
```

---

## STEP 3 — Create the page HTML

Create `/zoe-school/index.html` with this content:

```html
<!DOCTYPE html>
<html lang="zh-HK">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Zoe's K1 School Tracker 2027/28 | kendi-ng.com</title>
  <style>
    :root {
      --hki: #1A5276;
      --kln: #1E8449;
      --sha: #B7770D;
      --bg: #f8f9fa;
      --card: #ffffff;
      --text: #1a1a1a;
      --muted: #6c757d;
      --border: #dee2e6;
      --confirmed: #0f6e56;
      --pending: #856404;
      --warning: #c0392b;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif; background: var(--bg); color: var(--text); font-size: 14px; }

    /* ── Header ── */
    .page-header { background: #2C3E50; color: white; padding: 32px 24px 24px; }
    .page-header h1 { font-size: 22px; font-weight: 600; margin-bottom: 4px; }
    .page-header .sub { font-size: 13px; opacity: 0.75; }
    .page-header .zoe-badge { display: inline-block; margin-top: 10px; background: rgba(255,255,255,0.15); border-radius: 20px; padding: 4px 14px; font-size: 12px; }

    /* ── Nav tabs ── */
    .tabs { display: flex; background: white; border-bottom: 1px solid var(--border); padding: 0 16px; overflow-x: auto; }
    .tab { padding: 12px 16px; font-size: 13px; font-weight: 500; cursor: pointer; border-bottom: 3px solid transparent; white-space: nowrap; color: var(--muted); transition: all 0.2s; }
    .tab.active { border-bottom-color: #2C3E50; color: var(--text); }

    /* ── Main ── */
    .container { max-width: 1100px; margin: 0 auto; padding: 20px 16px; }
    .section { display: none; }
    .section.active { display: block; }

    /* ── District group ── */
    .district-header { padding: 10px 14px; border-radius: 8px 8px 0 0; color: white; font-weight: 600; font-size: 13px; margin-top: 24px; }
    .district-hki { background: var(--hki); }
    .district-kln { background: var(--kln); }
    .district-sha { background: var(--sha); }

    /* ── School cards (table on desktop, cards on mobile) ── */
    .school-table { width: 100%; border-collapse: collapse; background: white; border-radius: 0 0 8px 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.08); margin-bottom: 4px; }
    .school-table th { font-size: 11px; font-weight: 600; text-align: left; padding: 8px 12px; background: #f1f3f4; color: var(--muted); border-bottom: 1px solid var(--border); }
    .school-table td { padding: 10px 12px; border-bottom: 1px solid var(--border); font-size: 12px; vertical-align: top; }
    .school-table tr:last-child td { border-bottom: none; }
    .school-table tr:hover td { background: #fafbfc; }

    .school-name-zh { font-weight: 600; font-size: 13px; }
    .school-name-en { color: var(--muted); font-size: 11px; margin-top: 1px; }
    .school-address { color: var(--muted); font-size: 11px; margin-top: 2px; }

    .badge { display: inline-block; font-size: 10px; padding: 2px 7px; border-radius: 4px; font-weight: 500; }
    .badge-full { background: #d5f5e3; color: #1e8449; }
    .badge-half { background: #e8f4fc; color: #1a5276; }
    .badge-confirmed { background: #d5f5e3; color: var(--confirmed); }
    .badge-pending { background: #fff3cd; color: var(--pending); }
    .badge-tbc { background: #f1f3f4; color: var(--muted); }

    .rank-main { font-size: 12px; font-weight: 500; }
    .rank-source { font-size: 10px; color: var(--muted); margin-top: 2px; }

    .tracker-date { font-weight: 500; color: var(--confirmed); }
    .tracker-note { font-size: 11px; color: var(--muted); margin-top: 2px; }
    .tracker-tbc { color: var(--pending); font-style: italic; font-size: 11px; }

    /* ── Timeline ── */
    .timeline { position: relative; padding-left: 24px; }
    .timeline::before { content: ''; position: absolute; left: 7px; top: 0; bottom: 0; width: 2px; background: var(--border); }
    .tl-item { position: relative; margin-bottom: 20px; }
    .tl-item::before { content: ''; position: absolute; left: -21px; top: 4px; width: 10px; height: 10px; border-radius: 50%; background: #2C3E50; border: 2px solid white; box-shadow: 0 0 0 2px #2C3E50; }
    .tl-date { font-weight: 600; font-size: 13px; margin-bottom: 4px; }
    .tl-body { background: white; border-radius: 8px; padding: 10px 14px; border: 1px solid var(--border); font-size: 12px; line-height: 1.6; }
    .tl-zh { margin-bottom: 4px; }
    .tl-en { color: var(--muted); }

    /* ── Notes ── */
    .notes-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 12px; }
    .note-card { background: white; border: 1px solid var(--border); border-radius: 8px; padding: 14px 16px; }
    .note-card h3 { font-size: 12px; font-weight: 600; color: var(--muted); margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.04em; }
    .note-card p { font-size: 13px; line-height: 1.6; }

    /* ── Last updated ── */
    .last-updated { font-size: 11px; color: var(--muted); text-align: right; margin-top: 24px; padding-top: 12px; border-top: 1px solid var(--border); }

    /* ── Responsive ── */
    @media (max-width: 700px) {
      .school-table thead { display: none; }
      .school-table tr { display: block; padding: 12px; border-bottom: 1px solid var(--border); }
      .school-table td { display: block; padding: 2px 0; border: none; }
      .school-table td::before { content: attr(data-label); font-weight: 600; font-size: 10px; color: var(--muted); display: block; margin-bottom: 2px; text-transform: uppercase; }
    }
  </style>
</head>
<body>

<div class="page-header">
  <h1>🏫 Zoe's K1 Dragon School Tracker</h1>
  <div class="sub">各幼稚園 2027/28年度 K1 申請追蹤</div>
  <div class="zoe-badge">👶 Zoe · Born 21 Feb 2024 · ✅ Age-eligible for 2027/28 K1</div>
</div>

<div class="tabs">
  <div class="tab active" onclick="showTab('schools')">🏫 Schools 學校 (16)</div>
  <div class="tab" onclick="showTab('tracker')">📅 Open Day & Application Tracker</div>
  <div class="tab" onclick="showTab('timeline')">🗓 Timeline 時間線</div>
  <div class="tab" onclick="showTab('notes')">📋 Notes 備註</div>
</div>

<div class="container">

  <!-- SCHOOLS TAB -->
  <div id="tab-schools" class="section active">
    <div id="school-list"></div>
  </div>

  <!-- TRACKER TAB -->
  <div id="tab-tracker" class="section">
    <p style="color:var(--muted);font-size:12px;margin-bottom:16px;">Open days are typically on Saturdays in Jul–Aug 2026. Check back here — dates will be updated as schools announce them. 開放日通常在2026年7-8月的星期六舉行，確認後將更新。</p>
    <table class="school-table" style="border-radius:8px;">
      <thead>
        <tr>
          <th>School 學校</th>
          <th>District 地區</th>
          <th>Open Day 開放日</th>
          <th>Application Date 申請日期</th>
          <th>Status 狀態</th>
          <th>Website 網址</th>
        </tr>
      </thead>
      <tbody id="tracker-list"></tbody>
    </table>
  </div>

  <!-- TIMELINE TAB -->
  <div id="tab-timeline" class="section">
    <div class="timeline" id="timeline-list"></div>
  </div>

  <!-- NOTES TAB -->
  <div id="tab-notes" class="section">
    <div class="notes-grid" id="notes-list"></div>
  </div>

  <div class="last-updated" id="last-updated"></div>
</div>

<script>
// ── Load data ──────────────────────────────────────────────────────────
fetch('/zoe-school/data/schools.json')
  .then(r => r.json())
  .then(data => init(data))
  .catch(() => {
    // fallback: inline data for local dev
    init(INLINE_DATA);
  });

// ── Tab switching ──────────────────────────────────────────────────────
function showTab(name) {
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', ['schools','tracker','timeline','notes'][i] === name);
  });
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.getElementById('tab-' + name).classList.add('active');
}

// ── Render ─────────────────────────────────────────────────────────────
function districtColor(d) {
  return d === 'hki' ? 'district-hki' : d === 'kln' ? 'district-kln' : 'district-sha';
}
function districtLabel(d, schools) {
  return schools.find(s => s.district === d)?.districtLabel || d;
}
function statusBadge(s) {
  if (!s || s === 'pending') return '<span class="badge badge-pending">Pending 待確認</span>';
  if (s === 'confirmed') return '<span class="badge badge-confirmed">✅ Confirmed 已確認</span>';
  return '<span class="badge badge-tbc">TBC</span>';
}

function init(data) {
  // Last updated
  document.getElementById('last-updated').textContent = 'Last updated: ' + data.lastUpdated + ' | Data source: school websites, EDB, HappySeeds, Toby, NoteSity (2025-26)';

  // ── Schools tab ──
  const districts = [...new Set(data.schools.map(s => s.district))];
  let schoolHTML = '';
  districts.forEach(d => {
    const group = data.schools.filter(s => s.district === d);
    schoolHTML += `<div class="district-header ${districtColor(d)}">${districtLabel(d, data.schools)} — ${group.length} schools</div>`;
    schoolHTML += `<table class="school-table"><thead><tr>
      <th>Kindergarten 幼稚園</th>
      <th>Feeder Primary 關連小學</th>
      <th>Primary Ranking 小學排名</th>
      <th>Session 上課時段</th>
      <th>Est. Application 預計申請</th>
      <th>Method 方式</th>
      <th>Website</th>
    </tr></thead><tbody>`;
    group.forEach(s => {
      schoolHTML += `<tr>
        <td data-label="Kindergarten">
          <div class="school-name-zh">${s.nameZh}</div>
          <div class="school-name-en">${s.nameEn}</div>
          <div class="school-address">${s.address}</div>
        </td>
        <td data-label="Feeder Primary">
          <div>${s.feederZh}</div>
          <div style="color:var(--muted);font-size:11px">${s.feederEn}</div>
        </td>
        <td data-label="Ranking">
          <div class="rank-main">${s.rankingZh}</div>
          <div class="rank-source">${s.rankingEn}</div>
          <div class="rank-source">Src: ${s.rankingSource}</div>
        </td>
        <td data-label="Session">
          <span class="badge ${s.session === 'Full Day' ? 'badge-full' : 'badge-half'}">${s.sessionZh}</span>
        </td>
        <td data-label="Est. Application" style="font-size:11px">${s.estAppPeriod}</td>
        <td data-label="Method" style="font-size:11px">${s.appMethod}</td>
        <td data-label="Website"><a href="${s.website}" target="_blank" style="font-size:11px;color:#1a5276">${s.website.replace('https://','')}</a></td>
      </tr>`;
    });
    schoolHTML += '</tbody></table>';
  });
  document.getElementById('school-list').innerHTML = schoolHTML;

  // ── Tracker tab ──
  let trackerHTML = '';
  data.schools.forEach(s => {
    trackerHTML += `<tr>
      <td data-label="School">
        <div style="font-weight:600;font-size:12px">${s.nameZh}</div>
        <div style="color:var(--muted);font-size:11px">${s.nameEn}</div>
      </td>
      <td data-label="District"><span style="font-size:11px">${s.districtLabel}</span></td>
      <td data-label="Open Day">
        ${s.openDay
          ? `<div class="tracker-date">📅 ${s.openDay}</div>`
          : `<div class="tracker-tbc">TBC</div>`}
        <div class="tracker-note">${s.openDayNote}</div>
      </td>
      <td data-label="Application Date">
        ${s.appDateConfirmed
          ? `<div class="tracker-date">📝 ${s.appDateConfirmed}</div>`
          : `<div class="tracker-tbc">TBC</div>`}
        <div class="tracker-note">${s.appDateNote}</div>
      </td>
      <td data-label="Status">${statusBadge(s.status)}</td>
      <td data-label="Website"><a href="${s.website}" target="_blank" style="font-size:11px;color:#1a5276">🔗 Visit</a></td>
    </tr>`;
  });
  document.getElementById('tracker-list').innerHTML = trackerHTML;

  // ── Timeline tab ──
  let tlHTML = '';
  data.timeline.forEach(t => {
    tlHTML += `<div class="tl-item">
      <div class="tl-date">${t.date}</div>
      <div class="tl-body">
        <div class="tl-zh">${t.zh}</div>
        <div class="tl-en">${t.en}</div>
      </div>
    </div>`;
  });
  document.getElementById('timeline-list').innerHTML = tlHTML;

  // ── Notes tab ──
  const notes = [
    { title: "Zoe's Date of Birth", body: "21 Feb 2024 (2024年2月21日)<br>✅ Eligible for 2027/28 K1 (born on/before 31 Dec 2024)" },
    { title: "What is a Dragon School 龍校?", body: "A through-train school (龍校) links KG → Primary → Secondary, eliminating competitive entry at each transition. Zoe would stay in the same school network from age 3 to 18." },
    { title: "EDB Registration Certificate 入學註冊證", body: "Apply to EDB Sep–Nov 2026. Takes 6–8 weeks. Required for subsidised KG registration." },
    { title: "Unified Registration Date 統一註冊日期", body: "8–10 Jan 2027. Only ONE kindergarten can be chosen for final registration." },
    { title: "Documents Required 所需文件", body: "• Birth certificate 出生證明書<br>• Parents' HKID 父母身份證<br>• Vaccination records 防疫注射記錄<br>• Stamped return envelope 回郵信封<br>• Recent photos 近照<br>• Baptism certificate (some schools) 領洗紙" },
    { title: "Ranking Sources 排名來源", body: "Rankings reference: HappySeeds, LeadingEducationCentre, ParentingHeadline, Toby, NoteSity, HKeTIME (2025-26). Rankings change yearly — for reference only." }
  ];
  document.getElementById('notes-list').innerHTML = notes.map(n =>
    `<div class="note-card"><h3>${n.title}</h3><p>${n.body}</p></div>`
  ).join('');
}

// ── Inline fallback data (same as schools.json, paste here too) ────────
const INLINE_DATA = null; // set to null; page requires the JSON file
</script>

</body>
</html>
```

---

## STEP 4 — GitHub Actions: Auto-check school websites

Create `.github/workflows/school-checker.yml`:

```yaml
name: School Website Checker

on:
  schedule:
    - cron: '0 1 * * 1'   # Every Monday 9am HKT (1am UTC)
  workflow_dispatch:        # Allow manual trigger

jobs:
  check-schools:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install requests beautifulsoup4

      - name: Run school checker
        run: python .github/scripts/check_schools.py

      - name: Send summary to email (optional)
        if: always()
        run: echo "Check complete — see output above for any changes detected"
```

---

## STEP 5 — Create the checker script

Create `.github/scripts/check_schools.py`:

```python
import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

SCHOOLS = [
    {"id": "spk",           "url": "https://www.spk.edu.hk",                  "keywords": ["open day", "開放日", "簡介會", "k1", "admission", "申請"]},
    {"id": "ssgs",          "url": "https://www.ssgckg.edu.hk",               "keywords": ["open day", "開放日", "簡介會", "k1", "admission", "申請"]},
    {"id": "shck",          "url": "https://www.shck.edu.hk",                 "keywords": ["open day", "開放日", "簡介會", "k1", "admission", "申請"]},
    {"id": "truelight_c",   "url": "https://www.truelightk-c.edu.hk",         "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "truelight_th",  "url": "https://www.tlmshkps.edu.hk/kindergarten","keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "sfx",           "url": "https://www.sfxcanossian.edu.hk",         "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "puiching_kln",  "url": "https://www.pcps.edu.hk/kg",              "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "lasalle",       "url": "https://www.lasallek.edu.hk",             "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "dgs",           "url": "https://www.dgskg.edu.hk",               "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "truelight_kln", "url": "https://www.kltkps.edu.hk",              "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "gskd",          "url": "https://www.gskd.edu.hk",               "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "maryknoll",     "url": "https://www.mcsps.edu.hk",              "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "heepyunn",      "url": "https://www.hykg.edu.hk",              "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "puiching_st",   "url": "https://www.stpcps.edu.hk",             "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "yunchuen",      "url": "https://www.yunchuen.edu.hk",           "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
    {"id": "lingliang",     "url": "https://www.lingliang.org.hk",          "keywords": ["open day", "開放日", "k1", "admission", "申請"]},
]

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; ZoeSchoolBot/1.0)"}

def check_school(school):
    try:
        r = requests.get(school["url"], headers=HEADERS, timeout=15)
        soup = BeautifulSoup(r.text, "html.parser")
        text = soup.get_text(separator=" ").lower()
        hits = [kw for kw in school["keywords"] if kw.lower() in text]
        # Look for date patterns near keywords
        date_pattern = re.findall(r'(202[6-7][年\-\/]\d{1,2}[月\-\/]\d{1,2})', r.text)
        return {
            "id": school["id"],
            "url": school["url"],
            "status": "ok",
            "keyword_hits": hits,
            "dates_found": list(set(date_pattern[:5])),
            "checked_at": datetime.now().isoformat()
        }
    except Exception as e:
        return {"id": school["id"], "url": school["url"], "status": "error", "error": str(e)}

print(f"\n{'='*60}")
print(f"Zoe School Checker — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
print(f"{'='*60}\n")

changes_detected = []
for school in SCHOOLS:
    result = check_school(school)
    if result["status"] == "ok" and result.get("dates_found"):
        print(f"⚠️  {result['id']}: Dates found on website → {result['dates_found']}")
        changes_detected.append(result)
    elif result["status"] == "error":
        print(f"❌  {result['id']}: Error — {result.get('error')}")
    else:
        print(f"✅  {result['id']}: No new dates detected")

print(f"\n{'='*60}")
print(f"Summary: {len(changes_detected)} school(s) with potential date updates")
if changes_detected:
    print("⚠️  Ask Claude to check and update schools.json for:")
    for c in changes_detected:
        print(f"   - {c['id']}: {c['dates_found']}")
print(f"{'='*60}\n")
```

---

## STEP 6 — File structure summary

Your repo should look like this after setup:

```
kendi-ng-dev/
├── zoe-school/
│   ├── index.html          ← the page (Step 3)
│   └── data/
│       └── schools.json    ← data file you update (Step 2)
├── .github/
│   ├── workflows/
│   │   └── school-checker.yml   ← auto weekly check (Step 4)
│   └── scripts/
│       └── check_schools.py     ← checker script (Step 5)
└── ... (rest of your site)
```

---

## STEP 7 — Mac terminal commands to deploy

```bash
# Clone your repo (if not already)
git clone https://github.com/hkkendi/kendi-ng-dev.git
cd kendi-ng-dev

# Create directories
mkdir -p zoe-school/data
mkdir -p .github/workflows
mkdir -p .github/scripts

# Then paste the files above into the correct paths
# Once files are in place:

git add .
git commit -m "Add Zoe K1 school tracker page with auto-checker"
git push origin main
```

---

## HOW TO UPDATE DATES (when schools announce)

When you come back and ask me to check, I will:
1. Search each school website
2. Tell you what to update in `schools.json`
3. You update the `openDay`, `appDateConfirmed`, and `status` fields:

```json
"openDay": "Sat 18 Jul 2026",
"appDateConfirmed": "15 Sep 2026",
"status": "confirmed"
```

That's it — the page will automatically show the confirmed dates in green.

---

*Generated: 2026-05-28 | For Zoe (born 21 Feb 2024) | kendi-ng.com/zoe-school*
