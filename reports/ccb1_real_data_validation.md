# CCB-1 real-data validation report

- normalized records: 419199
- inspected records: 100
- inspection mode: deterministic schema validation plus manual review of the listed sample
- duplicate record IDs: 0

## Source counts

| source | records |
|---|---:|
| amazon_esci | 10000 |
| google_convapparel | 175751 |
| wayfair_wands | 233448 |

## Missingness (allowed; not imputed)

| field | missing |
|---|---:|
| amazon_esci.commerciality | 10000 |
| amazon_esci.product_description | 5006 |
| amazon_esci.purchase_stage | 10000 |
| google_convapparel.commerciality | 175751 |
| google_convapparel.purchase_stage | 175751 |
| google_convapparel.relevance | 175751 |
| wayfair_wands.commerciality | 233448 |
| wayfair_wands.product_description | 30784 |
| wayfair_wands.purchase_stage | 233448 |

## Label preservation samples

| source | record_id | original label | canonical relevance | query/context | product |
|---|---|---|---|---|---|
| amazon_esci | 0 | I | irrelevant | revent 80 cfm | Panasonic FV-20VQ3 WhisperCeiling 190 CFM Ceiling Mounted Fan |
| google_convapparel | convapparel:bottoms_bad:0:0:B095PW81M5 |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Vibrant Women's Denim Shorts |
| wayfair_wands | 0 | Exact | exact | salon chair | 21.7 '' w waiting room chair with wood frame |
| amazon_esci | 1 | E | exact | revent 80 cfm | Homewerks 7141-80 Bathroom Fan Integrated LED Light Ceiling Mount Exhaust Ventilation, 1.1 Sones, 80 |
| google_convapparel | convapparel:bottoms_bad:0:0:B08ZYKK17V |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Women's Summer Casual Shorts |
| wayfair_wands | 1 | Irrelevant | irrelevant | salon chair | 22.5 '' wide polyester side chair |
| amazon_esci | 2 | E | exact | revent 80 cfm | Homewerks 7140-80 Bathroom Fan Ceiling Mount Exhaust Ventilation, 1.5 Sones, 80 CFM, White |
| google_convapparel | convapparel:bottoms_bad:0:0:B08DXVT1YN |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | rosewear Denim Shorts |
| wayfair_wands | 2 | Exact | exact | salon chair | 24.4 '' w metal lounge chair with metal frame |
| amazon_esci | 3 | E | exact | revent 80 cfm | Delta Electronics RAD80L BreezRadiance 80 CFM Heater/Fan/Light Combo White (Renewed) |
| google_convapparel | convapparel:bottoms_bad:0:0:B07MFDDWCW |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Womens High Waist Summer Shorts |
| wayfair_wands | 3 | Exact | exact | salon chair | 25 '' wide faux leather manual swivel standard recliner |
| amazon_esci | 4 | E | exact | revent 80 cfm | Panasonic FV-08VRE2 Ventilation Fan with Recessed LED (Renewed) |
| google_convapparel | convapparel:bottoms_bad:0:0:B0BVJ14WSY |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Women's Denim Shorts |
| wayfair_wands | 4 | Exact | exact | salon chair | 27.6 '' w antimicrobial leather seat waiting room chair with metal frame |
| amazon_esci | 5 | E | exact | revent 80 cfm | Panasonic FV-0511VQ1 WhisperCeiling DC Ventilation Fan, Speed Selector, SmartFlow Technology, Quiet, |
| google_convapparel | convapparel:bottoms_bad:0:0:B08DHVGML2 |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Women's Summer Beach Floral Shorts |
| wayfair_wands | 5 | Exact | exact | salon chair | 31.6 '' wide faux leather manual swivel ergonomic recliner |
| amazon_esci | 6 | E | exact | revent 80 cfm | Panasonic FV-0510VSL1 WhisperValue DC Ventilation Fan with Light, 50-80-100 CFM |
| google_convapparel | convapparel:bottoms_bad:0:0:B0C231ZCY1 |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Womens Summer Comfy Shorts |
| wayfair_wands | 6 | Irrelevant | irrelevant | salon chair | 46 '' w mesh seat tandem seating with metal frame |
| amazon_esci | 7 | E | exact | revent 80 cfm | Panasonic FV-0510VS1 WhisperValue DC Ventilation Fan, 50-80-100 CFM |
| google_convapparel | convapparel:bottoms_bad:0:0:B0B8Y9NQHZ |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Denim Jean Shorts |
| wayfair_wands | 7 | Irrelevant | irrelevant | salon chair | 63 '' w waiting room chair with metal frame |
| amazon_esci | 8 | E | exact | revent 80 cfm | Aero Pure ABF80 L5 W ABF80L5 Ceiling Mount 80 CFM w/LED Light/Nightlight, Energy Star Certified, Whi |
| google_convapparel | convapparel:bottoms_bad:0:0:B09VG8NKY1 |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | MOREFEEL Biker Shorts 3 Pack |
| wayfair_wands | 8 | Irrelevant | irrelevant | salon chair | 69 '' w leather seat tandem seating with metal frame |
| amazon_esci | 9 | E | exact | revent 80 cfm | Delta Electronics (Americas) Ltd. RAD80 Delta BreezRadiance Series 80 CFM Fan with Heater, 10.5W, 1. |
| google_convapparel | convapparel:bottoms_bad:0:0:B07Q5S5H5P |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Milumia Denim Shorts |
| wayfair_wands | 9 | Irrelevant | irrelevant | salon chair | 69 '' w metal seat tandem seating with metal frame |
| amazon_esci | 10 | I | irrelevant | revent 80 cfm | Aero Pure AP120H-SL W Slim Fit 120 CFM Bathroom Fan with LED Light and Humidity Sensor, White Finish |
| google_convapparel | convapparel:bottoms_bad:0:0:B07PGT945B |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Women's Summer Shorts |
| wayfair_wands | 10 | Exact | exact | salon chair | 69 '' w metal seat waiting room chair with metal frame |
| amazon_esci | 11 | E | exact | revent 80 cfm | Panasonic FV-0811VF5 WhisperFit EZ Retrofit Ventilation Fan, 80 or 110 CFM |
| google_convapparel | convapparel:bottoms_bad:0:0:B0767YDQXH |  |  | I am looking for shorts to wear this summer. I prefer denim shorts but am open to other options as well. | Denim Shorts |
| wayfair_wands | 11 | Irrelevant | irrelevant | salon chair | 70.87 '' w stackable metal seat waiting room chair with metal frame |
| amazon_esci | 12 | E | exact | revent 80 cfm | Aero Pure AP80RVLW Super Quiet 80 CFM Recessed Fan/Light Bathroom Ventilation Fan with White Trim Ri |
| google_convapparel | convapparel:bottoms_bad:0:1:B09SXLH75V |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Vintage Carpenter Denim Short |
| wayfair_wands | 12 | Irrelevant | irrelevant | salon chair | abel curved arm chair in clear |
| amazon_esci | 13 | E | exact | revent 80 cfm | Delta BreezSignature VFB25ACH 80 CFM Exhaust Bath Fan with Humidity Sensor |
| google_convapparel | convapparel:bottoms_bad:0:1:B00UA3258M |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Miss Me Denim Short |
| wayfair_wands | 13 | Irrelevant | irrelevant | salon chair | abernethy 27.2 '' wide club chair |
| amazon_esci | 14 | E | exact | revent 80 cfm | Broan Very Quiet Ceiling Bathroom Exhaust Fan, ENERGY STAR Certified, 0.3 Sones, 80 CFM |
| google_convapparel | convapparel:bottoms_bad:0:1:B0BVJ14WSY |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Women's Denim Shorts |
| wayfair_wands | 14 | Exact | exact | salon chair | adjustable hydraulic barber salon reclining massage chair |
| amazon_esci | 15 | E | exact | revent 80 cfm | Delta Electronics (Americas) Ltd. GBR80HLED Delta BreezGreenBuilder Series 80 CFM Fan/Dimmable H, LE |
| google_convapparel | convapparel:bottoms_bad:0:1:B095PW81M5 |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Vibrant Women's Denim Shorts |
| wayfair_wands | 15 | Partial | unknown | salon chair | aliandra fashion casual lift chair office work beauty salon task chair |
| amazon_esci | 16 | I | irrelevant | !awnmower tires without rims | RamPro 10" All Purpose Utility Air Tires/Wheels with a 5/8" Diameter Hole with Double Sealed Bearing |
| google_convapparel | convapparel:bottoms_bad:0:1:B0767YDQXH |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Denim Shorts |
| wayfair_wands | 16 | Exact | exact | salon chair | all purpose hydraulic salon barber massage chair |
| amazon_esci | 17 | E | exact | !awnmower tires without rims | MaxAuto 2-Pack 13x5.00-6 2PLY Turf Mower Tractor Tire with Yellow Rim, (3" Centered Hub, 3/4" Bushin |
| google_convapparel | convapparel:bottoms_bad:0:1:B0742KPVD6 |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Wax Basic Denim Shorts |
| wayfair_wands | 17 | Exact | exact | salon chair | all purpose salon hydraulic barber massage chair |
| amazon_esci | 18 | I | irrelevant | !awnmower tires without rims | NEIKO 20601A 14.5 inch Steel Tire Spoon Lever Iron Tool Kit \| Professional Tire Changing Tool for M |
| google_convapparel | convapparel:bottoms_bad:0:1:B07Q13G8H7 |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Denim Jean Shorts |
| wayfair_wands | 18 | Partial | unknown | salon chair | almuth fashion office beauty salon task chair |
| amazon_esci | 19 | S | substitute | !awnmower tires without rims | 2PK 13x5.00-6 13x5.00x6 13x5x6 13x5-6 2PLY Turf Mower Tractor Tire with Gray Rim |
| google_convapparel | convapparel:bottoms_bad:0:1:B08DXVT1YN |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | rosewear Denim Shorts |
| wayfair_wands | 19 | Irrelevant | irrelevant | salon chair | anette salon anti-fatigue mat |
| amazon_esci | 20 | E | exact | !awnmower tires without rims | (Set of 2) 15x6.00-6 Husqvarna/Poulan Tire Wheel Assy .75" Bearing |
| google_convapparel | convapparel:bottoms_bad:0:1:B00Y1U7M9C |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Seven7 Dark Denim Shorts |
| wayfair_wands | 20 | Partial | unknown | salon chair | arianny simple fashion casual beauty salon conference chair |
| amazon_esci | 21 | E | exact | !awnmower tires without rims | MaxAuto 2 Pcs 16x6.50-8 Lawn Mower Tire for Garden Tractors Ridings, 4PR, Tubeless |
| google_convapparel | convapparel:bottoms_bad:0:1:B09XTDQP6L |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | Finevalue Denim Patchwork Shorts |
| wayfair_wands | 21 | Partial | unknown | salon chair | ariany fashion casual beauty salon conference chair |
| amazon_esci | 22 | C | complement | !awnmower tires without rims | Dr.Roc Tire Spoon Lever Dirt Bike Lawn Mower Motorcycle Tire Changing Tools with Durable Bag 3 Tire  |
| google_convapparel | convapparel:bottoms_bad:0:1:B09N9D6FT8 |  |  | I like the dark wash denim shorts suggestion. May I see more in a similar style? | KINGFEN Women's Summer Linen Shorts |
| wayfair_wands | 22 | Exact | exact | salon chair | ayda 25.6 '' w leather seat waiting room chair with metal frame |
| amazon_esci | 23 | E | exact | !awnmower tires without rims | MARASTAR 21446-2PK 15x6.00-6" Front Tire Assembly Replacement-Craftsman Mower, Pack of 2 |
| google_convapparel | convapparel:bottoms_bad:0:2:B09XTDQP6L |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Finevalue Denim Patchwork Shorts |
| wayfair_wands | 23 | Partial | unknown | salon chair | bar salon task chair |
| amazon_esci | 24 | S | substitute | !awnmower tires without rims | 15x6.00-6" Front Tire Assembly Replacement for 100 and 300 Series John Deere Riding Mowers - 2 pack |
| google_convapparel | convapparel:bottoms_bad:0:2:B083M65X7K |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Women Linen Shorts |
| wayfair_wands | 24 | Irrelevant | irrelevant | salon chair | barber beauty salon spa equipment kids chair |
| amazon_esci | 25 | I | irrelevant | !awnmower tires without rims | Honda HRR Wheel Kit (2 Front 44710-VL0-L02ZB, 2 Back 42710-VE2-M02ZE) |
| google_convapparel | convapparel:bottoms_bad:0:2:B0928MQT4M |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Womens Denim Shorts |
| wayfair_wands | 25 | Exact | exact | salon chair | barber salon reclining massage chair |
| amazon_esci | 26 | E | exact | !awnmower tires without rims | Honda 42710-VE2-M02ZE (Replaces 42710-VE2-M01ZE) Lawn Mower Rear Wheel Set of 2 |
| google_convapparel | convapparel:bottoms_bad:0:2:B074662GJQ |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Womens Summer Linen Shorts |
| wayfair_wands | 26 | Exact | exact | salon chair | barber shampoo salon reclining massage chair |
| amazon_esci | 27 | S | substitute | !awnmower tires without rims | Honda 44710-VG3-010 Front Wheels, (Set of 2) |
| google_convapparel | convapparel:bottoms_bad:0:2:B0BVJ14WSY |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Women's Denim Shorts |
| wayfair_wands | 27 | Exact | exact | salon chair | barberpub hydraulic reclining massage chair |
| amazon_esci | 28 | E | exact | !awnmower tires without rims | Carlisle Turf Saver Lawn & Garden Tire - 15X6-6 A |
| google_convapparel | convapparel:bottoms_bad:0:2:B083M638YY |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Women Linen Shorts |
| wayfair_wands | 28 | Exact | exact | salon chair | barberpub hydraulic salon spa reclining massage chair with ottoman |
| amazon_esci | 29 | E | exact | !awnmower tires without rims | Oregon 72-107 Universal Wheel 7X150 Diamond Plastic |
| google_convapparel | convapparel:bottoms_bad:0:2:B08ZSKPJSB |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Denim Distressed Jean Shorts |
| wayfair_wands | 29 | Exact | exact | salon chair | barberpub salon massage chair |
| amazon_esci | 30 | I | irrelevant | !awnmower tires without rims | American Lawn Mower Company 1204-14 14-Inch 4-Blade Push Reel Lawn Mower, Red |
| google_convapparel | convapparel:bottoms_bad:0:2:B08B67K8FW |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | KINGFEN Womens Summer Shorts |
| wayfair_wands | 30 | Irrelevant | irrelevant | salon chair | barberpub shampoo reclining massage chair |
| amazon_esci | 31 | I | irrelevant | !awnmower tires without rims | Craftsman 532403111 Mower Front Drive Wheels (Pack of 2) |
| google_convapparel | convapparel:bottoms_bad:0:2:B09QZYCYZ7 |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Denim Jean Shorts |
| wayfair_wands | 31 | Partial | unknown | salon chair | beauty salon ergonomic task chair |
| amazon_esci | 32 | I | irrelevant | !qscreen fence without holes | FOTMISHU 6Pcs Greenhouse Hoops Rust-Free Grow Tunnel Tunnel, 4ft Long Steel with Plastic Coated Plan |
| google_convapparel | convapparel:bottoms_bad:0:2:B07CPQRY1X |  |  | Please only suggest women's shorts. I like the summer linen shorts, as well as the denim patchwork shorts. I would like  | Womens Summer Linen Shorts |
| wayfair_wands | 32 | Partial | unknown | salon chair | beauty salon task chair |
| amazon_esci | 33 | I | irrelevant | !qscreen fence without holes | Zippity Outdoor Products ZP19028 Unassembled Madison Vinyl Gate Kit with Fence Wings, White |

## Review checklist

- [x] Every sample record passed Pydantic validation.
- [x] Original source IDs and labels remain present in metadata/source fields.
- [x] Missing fields remain null/empty; no LLM inference was used during normalization.
- [x] Product/query joins were performed only on source-provided keys.
- [x] ConvApparel records keep recommendation relevance unknown unless the source provides an explicit label.
- [ ] Human reviewer sign-off: required before CCB-1 gold promotion.
