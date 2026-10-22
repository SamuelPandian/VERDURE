"""
VERDURE Agronomic Prescription & Clinical Pathology Knowledge Base.
Provides scientific pathogen taxonomy, chemical treatment protocols,
organic/biological alternatives, and cultural sanitation practices.
"""

PRESCRIPTION_DB = {
    # Apple
    "Apple_scab": {
        "pathogen": "Venturia inaequalis (Ascomycete Fungus)",
        "symptoms": "Olive-green to velvety brown lesions on leaves and fruit, causing leaf distortion and premature defoliation.",
        "rx_chemical": "Captan 50 WP (2.5 g/L) or Difenoconazole 25 EC (0.5 mL/L)",
        "rx_biological": "Bacillus amyloliquefaciens strain D747 or Liquid Copper Octanoate (2 mL/L)",
        "cultural": "Rake and burn fallen autumn foliage. Prune canopy to promote 360° airflow and reduce leaf wetness duration.",
        "timeline": "Apply at green-tip bud stage; repeat at 10-14 day intervals until petal fall."
    },
    "Black_rot": {
        "pathogen": "Botryosphaeria obtusa (Fungus)",
        "symptoms": "Frog-eye leaf spots with purple margins and brown centers; black mummified fruit.",
        "rx_chemical": "Mancozeb 75 WP (2.5 g/L) or Thiophanate-methyl 70 WP (1.0 g/L)",
        "rx_biological": "Trichoderma harzianum foliar spray + Copper oxychloride 50 WP (2.5 g/L)",
        "cultural": "Prune out dead wood, cankers, and mummified apples hanging from previous season.",
        "timeline": "Knockdown spray at tight cluster; secondary application 14 days later."
    },
    "Cedar_apple_rust": {
        "pathogen": "Gymnosporangium juniperi-virginianae (Rust Fungus)",
        "symptoms": "Brilliant bright orange-yellow foliar spots with small black pycnia on upper leaf surfaces.",
        "rx_chemical": "Myclobutanil 10 WP (0.4 g/L) or Propiconazole 25 EC (0.75 mL/L)",
        "rx_biological": "Sulfur 80 WP (3 g/L) protective barrier spray",
        "cultural": "Remove nearby cedar/juniper galls within 500 meters of the orchard perimeter.",
        "timeline": "Apply from pink-bud stage through second cover spray."
    },
    
    # Corn (Maize)
    "Cercospora_leaf_spot Gray_leaf_spot": {
        "pathogen": "Cercospora zeae-maydis (Fungus)",
        "symptoms": "Rectangular, tan to gray necrotic lesions bounded strictly by leaf veins.",
        "rx_chemical": "Azoxystrobin + Difenoconazole (1 mL/L) or Pyraclostrobin (0.8 mL/L)",
        "rx_biological": "Trichoderma viride bio-fungicide (5 g/L) with sticker agent",
        "cultural": "Practice 2-year crop rotation with non-host crops (soybean/sunflower); deep tillage of residue.",
        "timeline": "Spray at VT-R1 (tasseling to silking) when lesions appear on 3rd leaf below ear."
    },
    "Common_rust_": {
        "pathogen": "Puccinia sorghi (Basidiomycete Fungus)",
        "symptoms": "Golden-brown to cinnamon-brown powdery pustules on both upper and lower leaf surfaces.",
        "rx_chemical": "Tebuconazole 25.9 EC (1.0 mL/L) or Mancozeb 75 WP (2.0 g/L)",
        "rx_biological": "Neem seed kernel extract (NSKE 5%) or Ampelomyces quisqualis hyperparasite",
        "cultural": "Plant rust-resistant hybrids; avoid excess nitrogen fertilizer which causes lush susceptible canopy.",
        "timeline": "Initiate treatment when pustules appear on >50% of plants before tasseling."
    },
    "Northern_Leaf_Blight": {
        "pathogen": "Exserohilum turcicum (Fungus)",
        "symptoms": "Large, cigar-shaped grayish-green to tan lesions (2.5–15 cm long) on foliage.",
        "rx_chemical": "Chlorothalonil 75 WP (2.0 g/L) or Azoxystrobin (1.2 mL/L)",
        "rx_biological": "Pseudomonas fluorescens 1% WP (5 g/L) foliar spray",
        "cultural": "Bury crop residues immediately post-harvest. Use resistant seed varieties with Ht genes.",
        "timeline": "Apply at onset of first lesion; repeat 14 days later if humid conditions persist."
    },

    # Grape
    "Black_rot": {
        "pathogen": "Guignardia bidwellii (Fungus)",
        "symptoms": "Reddish-brown circular leaf spots with dark margins and tiny black specks; shriveled black berries.",
        "rx_chemical": "Mancozeb 75 WP (2.5 g/L) or Kresoxim-methyl 44.3 SC (0.7 mL/L)",
        "rx_biological": "Bordeaux mixture 1% or Copper hydroxide 77 WP (2 g/L)",
        "cultural": "Canopy thinning to maximize UV sunlight penetration; destroy all mummified grape clusters.",
        "timeline": "Spray at bud-break, pre-bloom, and post-bloom intervals."
    },
    "Esca_(Black_Measles)": {
        "pathogen": "Phaeoacremonium / Fomitiporia complex (Fungal Trunk Disease)",
        "symptoms": "'Tiger-stripe' foliar chlorosis and necrosis; dark spotting on berry skin; wood vascular necrosis.",
        "rx_chemical": "Fosetyl-Aluminium (2.5 g/L) trunk drench + wound protectant paste on pruning cuts",
        "rx_biological": "Trichoderma atroviride pruned-wound sealant paint",
        "cultural": "Prune exclusively in dry weather. Disinfect pruning shears in 70% ethanol between vines.",
        "timeline": "Apply wound sealant within 24 hours of pruning; soil drench during active sap flow."
    },
    "Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "pathogen": "Pseudocercospora cladosporioides (Fungus)",
        "symptoms": "Irregular, dark brown to black spots with yellowish halos on foliage, causing early scorch.",
        "rx_chemical": "Carbendazim 50 WP (1.0 g/L) or Propineb 70 WP (2.0 g/L)",
        "rx_biological": "Bacillus subtilis foliar spray (3 g/L)",
        "cultural": "Ensure rapid drainage in vineyard; remove lower trailing leaves within 30 cm of soil surface.",
        "timeline": "Spray at first sign of sporulation after monsoon shower."
    },

    # Citrus
    "Haunglongbing_(Citrus_greening)": {
        "pathogen": "Candidatus Liberibacter asiaticus (Vector: Asian Citrus Psyllid)",
        "symptoms": "Asymmetric blotchy foliar mottle, yellow shoots, small lopsided bitter fruit with aborted seeds.",
        "rx_chemical": "Imidacloprid 17.8 SL (0.5 mL/L) or Thiamethoxam 25 WG (0.3 g/L) to control psyllid vector",
        "rx_biological": "Encarsia lahorensis / Tamarixia radiata parasitoid wasps + Zinc/Manganese nutritional drench",
        "cultural": "Strict quarantine; immediately rogue out and incinerate infected trees. Plant certified disease-free nursery stock.",
        "timeline": "Vector suppression sprays at spring and autumn flush stages."
    },

    # Peach
    "Bacterial_spot": {
        "pathogen": "Xanthomonas arboricola pv. pruni (Bacterium)",
        "symptoms": "Small, angular purple-brown spots that drop out creating 'shot-hole' appearance.",
        "rx_chemical": "Oxytetracycline 200 ppm or Copper sulfate pentahydrate (1.5 g/L)",
        "rx_biological": "Bacillus amyloliquefaciens (3 g/L) preventive spray",
        "cultural": "Avoid excessive nitrogen fertilization; plant windbreaks to minimize wind-driven sand abrasion.",
        "timeline": "Dormant copper spray at leaf fall, followed by low-rate copper from shuck split."
    },

    # Pepper (Bell)
    "Bacterial_spot": {
        "pathogen": "Xanthomonas euvesicatoria (Bacterium)",
        "symptoms": "Small, water-soaked blister-like lesions on foliage becoming necrotic with chlorotic halos.",
        "rx_chemical": "Copper Hydroxide 77 WP (2.0 g/L) + Streptocycline (100 ppm)",
        "rx_biological": "Bacteriophage cocktail (AgriPhage) or Pseudomonas fluorescens (5 g/L)",
        "cultural": "Use certified pathogen-free seeds (hot-water treated 50°C for 25 min). Avoid overhead sprinkler irrigation.",
        "timeline": "Spray at transplanting; repeat every 7 days during warm rainy periods."
    },

    # Potato
    "Early_blight": {
        "pathogen": "Alternaria solani (Fungus)",
        "symptoms": "Characteristic concentric ring lesions ('target-board' pattern) on older lower leaves.",
        "rx_chemical": "Mancozeb 75 WP (2.5 g/L) or Iprodione 50 WP (2.0 g/L) or Difenoconazole",
        "rx_biological": "Trichoderma harzianum (5 g/L) + Potassium bicarbonate spray (3 g/L)",
        "cultural": "Ensure adequate nitrogen and potassium fertility to avoid plant stress. Drip irrigate only.",
        "timeline": "Spray when canopy closes or upon observation of first lower-leaf target spot."
    },
    "Late_blight": {
        "pathogen": "Phytophthora infestans (Oomycete Water Mold)",
        "symptoms": "Rapidly expanding water-soaked black/dark-brown lesions with white fuzzy sporulation on leaf undersides under high humidity.",
        "rx_chemical": "Metalaxyl-M + Mancozeb (2.5 g/L) or Cymoxanil + Mancozeb (2.0 g/L) or Dimethomorph (1.5 g/L)",
        "rx_biological": "Copper hydroxide 77 WP (2.0 g/L) preventive shield + Bio-fermented compost tea",
        "cultural": "Destroy all volunteer potato cull piles. Plant certified seed tubers. Ensure wide row spacing for canopy aeration.",
        "timeline": "Emergency systemic knockdown spray immediately within 24 hours of disease trigger."
    },

    # Squash
    "Powdery_mildew": {
        "pathogen": "Podosphaera xanthii (Fungus)",
        "symptoms": "White talcum-powder-like fungal patches on leaf surfaces, petiole, and stems.",
        "rx_chemical": "Triadimefon 25 WP (1.0 g/L) or Hexaconazole 5 EC (1.0 mL/L)",
        "rx_biological": "Potassium silicate (2 mL/L) or Milk whey 10% solution or Ampelomyces quisqualis",
        "cultural": "Plant resistant cultivars; ensure full sun exposure and avoid dense shading.",
        "timeline": "Apply at first sign of white powdery spots on lower leaves."
    },

    # Strawberry
    "Leaf_scorch": {
        "pathogen": "Diplocarpon earlianum (Fungus)",
        "symptoms": "Irregular purple-to-dark-red blotches covering leaf blades, coalescing into burnt scorch look.",
        "rx_chemical": "Captan 50 WP (2.0 g/L) or Thiophanate-methyl 70 WP (1.0 g/L)",
        "rx_biological": "Copper octanoate (1.5 mL/L) or Bacillus subtilis",
        "cultural": "Renovate strawberry beds immediately after harvest. Rake away infected leaves.",
        "timeline": "Spray during spring vegetative flush and post-harvest renovation."
    },

    # Tomato
    "Bacterial_spot": {
        "pathogen": "Xanthomonas vesicatoria (Bacterium)",
        "symptoms": "Dark greasy angular lesions (<3 mm) surrounded by bright yellow halos; causes blossom drop.",
        "rx_chemical": "Copper Oxychloride 50 WP (2.5 g/L) + Streptocycline (150 ppm)",
        "rx_biological": "Bacillus subtilis strain QST 713 or Copper octanoate",
        "cultural": "Stake plants off bare soil; avoid handling wet plants; rotate with brassicas or corn for 2 years.",
        "timeline": "Weekly foliar sprays starting immediately at seedling transplant."
    },
    "Early_blight": {
        "pathogen": "Alternaria linariae / Alternaria solani",
        "symptoms": "Concentric dark brown rings with chlorotic yellow halo progressing from bottom foliage upward.",
        "rx_chemical": "Chlorothalonil 75 WP (2.0 g/L) or Azoxystrobin (1.0 mL/L)",
        "rx_biological": "Trichoderma asperellum (5 g/L) soil drench & foliar spray",
        "cultural": "Mulch soil with straw to prevent fungal spores splashing from soil onto lower foliage.",
        "timeline": "Spray at first flower cluster; repeat every 10 days."
    },
    "Late_blight": {
        "pathogen": "Phytophthora infestans (Oomycete Pathogen)",
        "symptoms": "Rapidly spreading greasy dark brown water-soaked blotches; white cottony down on leaf underside; stems collapse.",
        "rx_chemical": "Mandipropamid 250 SC (0.8 mL/L) or Metalaxyl + Mancozeb (2.5 g/L)",
        "rx_biological": "Fixed Copper (Copper Hydroxide 2 g/L) + Chitosan oligosaccharide foliar vaccine",
        "cultural": "Prune suckers for maximum air circulation; avoid sprinkler overhead irrigation; destroy cull piles.",
        "timeline": "Emergency application within 12 hours of detection. Re-apply in 5 days if humidity >90%."
    },
    "Leaf_Mold": {
        "pathogen": "Passalora fulva (Cladosporium fulvum)",
        "symptoms": "Pale greenish-yellow foliar spots with velvety olive-brown mold on underside of leaf.",
        "rx_chemical": "Difenoconazole 25 EC (0.5 mL/L) or Maneb 80 WP (2.0 g/L)",
        "rx_biological": "Sulfur-based eco-spray or Trichoderma viride",
        "cultural": "In greenhouse crops, lower relative humidity below 85% with exhaust ventilation and warm air heating.",
        "timeline": "Spray immediately upon spotting fuzzy underside sporulation."
    },
    "Septoria_leaf_spot": {
        "pathogen": "Septoria lycopersici (Fungus)",
        "symptoms": "Numerous circular gray lesions (2-3 mm) with dark margins and tiny black fruiting bodies (pycnidia).",
        "rx_chemical": "Chlorothalonil 75 WP (2.0 g/L) or Mancozeb 75 WP (2.5 g/L)",
        "rx_biological": "Bacillus amyloliquefaciens (3 g/L) foliar spray",
        "cultural": "Remove lower 30 cm of leaves (bottom pruning); mulch heavily beneath plants.",
        "timeline": "Apply preventive fungicide right after transplanting when first true leaves expand."
    },
    "Spider_mites Two-spotted_spider_mite": {
        "pathogen": "Tetranychus urticae (Acarid Pest)",
        "symptoms": "Fine yellow stippling and bronzing on upper leaf surface accompanied by delicate fine silk webbing.",
        "rx_chemical": "Abamectin 1.8 EC (0.5 mL/L) or Spiromesifen 22.9 SC (1.0 mL/L)",
        "rx_biological": "Phytoseiulus persimilis predatory mites or Cold-pressed Neem oil (5 mL/L) + soap emulsifier",
        "cultural": "Maintain adequate soil hydration (mites thrive in drought/dusty conditions); mist foliage lightly.",
        "timeline": "Spray at early threshold (>2 mites per leaf leaflet); repeat in 5 days to kill newly hatched eggs."
    },
    "Target_Spot": {
        "pathogen": "Corynespora cassiicola (Fungus)",
        "symptoms": "Brown circular lesions with subtle target concentric rings, lacking the pronounced yellow halo of Early Blight.",
        "rx_chemical": "Pyraclostrobin + Boscalid (1.0 g/L) or Azoxystrobin (1.2 mL/L)",
        "rx_biological": "Bacillus subtilis + Copper soap",
        "cultural": "Space rows at least 1.5 meters apart to promote canopy drying.",
        "timeline": "Spray every 7-10 days starting at vegetative canopy closure."
    },
    "Tomato_Yellow_Leaf_Curl_Virus": {
        "pathogen": "Tomato Yellow Leaf Curl Geminivirus (Vector: Bemisia tabaci Whitefly)",
        "symptoms": "Severe foliar stunting, upward cupping of leaves, prominent interveinal chlorosis, flower drop.",
        "rx_chemical": "Dinotefuran 20 SG (0.5 g/L) or Acetamiprid 20 SP (0.4 g/L) targeting whitefly vector",
        "rx_biological": "Yellow sticky cards (20 traps/acre) + Beauveria bassiana entomopathogenic fungus (5 g/L)",
        "cultural": "Install 50-mesh insect-proof netting in seedling nurseries. Rogue out infected plants immediately.",
        "timeline": "Vector suppression from germination in nursery through early fruiting."
    },
    "Tomato_mosaic_virus": {
        "pathogen": "Tomato Mosaic Tobamovirus (ToMV)",
        "symptoms": "Mottled light and dark green foliar mosaic, leaf distortion, blister-like raised areas, 'shoestring' leaves.",
        "rx_chemical": "No chemical viricide exists; spray Skim Milk 20% solution as mechanical transmission barrier",
        "rx_biological": "Chitosan bio-elicitor foliar spray to activate systemic acquired resistance (SAR)",
        "cultural": "Workers must wash hands with 20% trisodium phosphate (TSP) or soap before handling plants; never smoke near tomatoes.",
        "timeline": "Sanitize tools between handling plants; remove and bury symptomatic plants."
    },

    # Rice Diseases (rice_diseases.pt & zenodo_rice.pt)
    "Bacterial_leaf_blight": {
        "pathogen": "Xanthomonas oryzae pv. oryzae (Bacterium)",
        "symptoms": "Water-soaked stripes along leaf margins turning yellow-white with wavy edges; milky bacterial ooze beads in early morning.",
        "rx_chemical": "Copper Hydroxide 77 WP (2.0 g/L) + Streptocycline (150 ppm)",
        "rx_biological": "Pseudomonas fluorescens 1% WP (10 g/L) seed treatment and foliar spray",
        "cultural": "Drain paddy field for 3-4 days to arrest bacterial spread. Avoid excess urea nitrogen during tillering.",
        "timeline": "Apply at first appearance of bacterial kresek symptoms or leaf blight lesions."
    },
    "Bacterial_Leaf_Blight": {
        "pathogen": "Xanthomonas oryzae pv. oryzae (Bacterium)",
        "symptoms": "Water-soaked stripes along leaf margins turning yellow-white with wavy edges; milky bacterial ooze beads in early morning.",
        "rx_chemical": "Copper Hydroxide 77 WP (2.0 g/L) + Streptocycline (150 ppm)",
        "rx_biological": "Pseudomonas fluorescens 1% WP (10 g/L) seed treatment and foliar spray",
        "cultural": "Drain paddy field for 3-4 days to arrest bacterial spread. Avoid excess urea nitrogen during tillering.",
        "timeline": "Apply at first appearance of bacterial kresek symptoms or leaf blight lesions."
    },
    "Brown_spot": {
        "pathogen": "Bipolaris oryzae (Cochliobolus miyabeanus - Fungus)",
        "symptoms": "Oval or circular brown lesions with gray/white center and yellow halo across entire leaf blade; causes grain discoloration.",
        "rx_chemical": "Mancozeb 75 WP (2.5 g/L) or Tricyclazole 75 WP (0.6 g/L) or Propiconazole (1 mL/L)",
        "rx_biological": "Trichoderma viride seed coating (4 g/kg seed) + Silicon foliar supplement (2 mL/L)",
        "cultural": "Correct soil nutrient deficiency, particularly Potassium (K) and Silicon (Si); avoid water stress in field.",
        "timeline": "Foliar spray at boot leaf stage and 10 days post-heading."
    },
    "Brown_Spot": {
        "pathogen": "Bipolaris oryzae (Cochliobolus miyabeanus - Fungus)",
        "symptoms": "Oval or circular brown lesions with gray/white center and yellow halo across entire leaf blade; causes grain discoloration.",
        "rx_chemical": "Mancozeb 75 WP (2.5 g/L) or Tricyclazole 75 WP (0.6 g/L) or Propiconazole (1 mL/L)",
        "rx_biological": "Trichoderma viride seed coating (4 g/kg seed) + Silicon foliar supplement (2 mL/L)",
        "cultural": "Correct soil nutrient deficiency, particularly Potassium (K) and Silicon (Si); avoid water stress in field.",
        "timeline": "Foliar spray at boot leaf stage and 10 days post-heading."
    },
    "Leaf_smut": {
        "pathogen": "Entyloma oryzae (Fungus)",
        "symptoms": "Small, angular black raised spots (telia) on both leaf surfaces, leading to premature yellowing and drying.",
        "rx_chemical": "Propiconazole 25 EC (1.0 mL/L) or Hexaconazole 5 SC (2.0 mL/L)",
        "rx_biological": "Copper oxychloride 50 WP (2.5 g/L)",
        "cultural": "Maintain balanced fertility; remove diseased crop stubble following harvest.",
        "timeline": "Single application at late tillering or panicle initiation."
    },
    "Blast": {
        "pathogen": "Magnaporthe oryzae (Pyricularia oryzae - Ascomycete Fungus)",
        "symptoms": "Diamond/spindle-shaped lesions with grayish-white center and brown-red margin; neck blast causing empty panicles.",
        "rx_chemical": "Tricyclazole 75 WP (0.6 g/L) or Isoprothiolane 40 EC (1.5 mL/L) or Kasugamycin (1.5 mL/L)",
        "rx_biological": "Pseudomonas fluorescens (10 g/L) + Chitosan (1.5 mL/L)",
        "cultural": "Avoid excessive nitrogen application; maintain continuous standing water layer (5 cm) during blast-prone weather.",
        "timeline": "Apply preventive spray at early tillering and second spray at heading stage."
    },
    "Tungro": {
        "pathogen": "Rice Tungro Bacilliform Virus (RTBV) & Spherical Virus (RTSV) (Vector: Green Leafhopper)",
        "symptoms": "Yellow-orange foliar discoloration starting from leaf tip; marked plant stunting, reduced tillering, delayed flowering.",
        "rx_chemical": "Thiamethoxam 25 WG (0.2 g/L) or Pymetrozine 50 WG (0.6 g/L) for leafhopper vector suppression",
        "rx_biological": "Neem oil 5% (5 mL/L) vector repellent + Light traps (1 trap/acre)",
        "cultural": "Plough down ratoon rice immediately post-harvest. Practice synchronized community planting.",
        "timeline": "Target vector spray during seedling nursery and 15-30 days after transplanting."
    },
    "Sheath_Blight": {
        "pathogen": "Rhizoctonia solani (Fungus)",
        "symptoms": "Oval, greenish-gray water-soaked lesions on leaf sheath near water line, progressing to irregular banded leaf lesions.",
        "rx_chemical": "Hexaconazole 5 SC (2.0 mL/L) or Validamycin 3L (2.5 mL/L) or Azoxystrobin (1 mL/L)",
        "rx_biological": "Trichoderma harzianum soil and sheath broadcast",
        "cultural": "Widen hill spacing (20x15 cm) to reduce canopy density; skim floating sclerotia during land preparation.",
        "timeline": "Spray directly directed at the base of rice hills at active tillering stage."
    },

    # Healthy fallback
    "healthy": {
        "pathogen": "None (Optically & Biologically Healthy Foliage)",
        "symptoms": "Lush, turgid green vegetative tissue with unblemished vascular venation and intact cuticle layer.",
        "rx_chemical": "No chemical intervention needed. Maintain scheduled nutritional fertilization.",
        "rx_biological": "Preventive prophylactic seaweed extract / humic acid foliar spray (2 mL/L)",
        "cultural": "Continue routine scout monitoring twice weekly. Maintain optimal soil moisture and drip scheduling.",
        "timeline": "Next routine optical diagnostic audit recommended in 7 days."
    },
    "Normal": {
        "pathogen": "None (Normal Agronomic Stand)",
        "symptoms": "Vigorous photosynthetic canopy with balanced chlorophyll absorbance and zero pathological necrosis.",
        "rx_chemical": "No intervention required. Stand meets certified agronomic quality benchmarks.",
        "rx_biological": "Bio-stimulant micronutrient blend (Zinc, Boron, Iron) to sustain yield potential",
        "cultural": "Ensure continuous water regime management; continue standard pest scouting.",
        "timeline": "Routine check scheduled for next growth stage transition."
    }
}

def get_prescription(crop: str, condition: str, is_healthy: bool) -> dict:
    if is_healthy or condition.lower() in ["healthy", "normal"]:
        return PRESCRIPTION_DB["healthy"]
    
    # Try exact match on condition
    cond_clean = condition.replace(" ", "_")
    if cond_clean in PRESCRIPTION_DB:
        return PRESCRIPTION_DB[cond_clean]
    if condition in PRESCRIPTION_DB:
        return PRESCRIPTION_DB[condition]
    
    # Try case-insensitive or partial match
    for k, v in PRESCRIPTION_DB.items():
        if k.lower() == cond_clean.lower() or k.lower() in cond_clean.lower() or cond_clean.lower() in k.lower():
            return v
            
    # Generic fallback for unknown fungal/bacterial defect
    return {
        "pathogen": f"Undifferentiated Foliar Pathogen ({condition})",
        "symptoms": f"Visible chlorotic or necrotic tissue deformation consistent with {condition}.",
        "rx_chemical": "Broad-spectrum Copper Hydroxide 77 WP (2.0 g/L) + Mancozeb 75 WP (2.0 g/L)",
        "rx_biological": "Trichoderma viride (5 g/L) foliar spray + cold-pressed Neem oil (3 mL/L)",
        "cultural": "Isolate affected specimens. Remove symptomatic leaves with sanitized shears and improve aeration.",
        "timeline": "Knockdown application immediately; monitor response after 5 days."
    }
