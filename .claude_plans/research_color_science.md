# Advanced Color Grading Research for Aerial/Drone Footage
## Research Date: 2026-02-21

---

## 1. TIME-OF-DAY PRESETS

### 1.1 golden_hour

**Visual Description:**
Warm amber-orange light that rakes across the landscape at a low angle, casting long soft shadows. Highlights glow with golden warmth while shadows retain rich detail and subtle cool undertones for complementary contrast. The sky transitions from pale yellow near the horizon to saturated orange-red.

**Specific Adjustments:**
- **Temperature shift**: +200 to +500K warmer (shift B channel in LAB toward positive/yellow)
- **Exposure**: +0.2 to +0.5 stops
- **Highlights**: Pull down -40 to -60 to prevent blow-out and reveal sky gradients
- **Shadows**: Lift +30 to +50 to reveal ground detail
- **Contrast**: +15 to +25 (gentle S-curve)
- **Vibrance**: +20 to +40 (boosts muted colors without over-saturating already-warm tones)
- **Saturation overall**: +10 to +15 (conservative to avoid garish look)
- **HSV/HSL Orange**: Hue +5 toward red, Saturation +20, Luminance +15
- **HSV/HSL Yellow**: Saturation +15, Luminance +10
- **HSV/HSL Blue**: Saturation -10, Luminance -5 (suppress competing cool tones)
- **Split toning**: Highlights → warm orange (LAB b-channel: +8 to +12), Shadows → neutral-to-cool (LAB b: -3 to -5, LAB a: -2)
- **LAB L-curve**: Gentle S-curve, lift toe slightly for golden shadow glow
- **Film grain**: 15-25% fine grain for organic feel

**OpenCV/NumPy Approximation:**
```python
# Convert to LAB
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
# Warm highlights: shift b-channel in bright zones
mask_highlights = lab[:,:,0] > 180
lab[:,:,2][mask_highlights] += 8  # push b toward yellow/warm
# Cool shadows: slight blue shift in dark zones
mask_shadows = lab[:,:,0] < 80
lab[:,:,2][mask_shadows] -= 4
# Increase saturation of a/b channels
lab[:,:,1] *= 1.08  # slight warm-red boost
lab[:,:,2] *= 1.10  # warm-yellow boost
lab = np.clip(lab, 0, 255)
```

**Best Footage Type:** Coastlines, mountains, open fields, desert landscapes shot at sunrise/sunset
**Implementation Complexity:** Medium — requires range-masked LAB adjustments

---

### 1.2 blue_hour

**Visual Description:**
Deep indigo-blue atmosphere with a cool, ethereal quality. The sky transitions from dark navy overhead to soft purple-blue near the horizon. Any artificial lights (cities, boats) glow warmly as complementary accents. Shadows are deep blue-purple, highlights are neutral-to-cool.

**Specific Adjustments:**
- **Temperature shift**: -300 to -500K (shift b-channel in LAB toward negative/blue)
- **Blue Saturation**: +25 to +40 in HSL
- **Blue Luminance**: -10 to -20 (deepen sky, prevent washed-out blues)
- **Cyan Saturation**: +15 (enhance atmospheric depth)
- **Orange/Red Saturation**: +20 to +30 (warm light sources pop against cool bg)
- **Exposure**: -0.3 to 0 (keep it moody and dark)
- **Shadows**: Lift minimally +10 to +20 (retain detail without washing out darkness)
- **LAB a-channel**: -3 to -5 in shadows (push toward green-cool)
- **LAB b-channel**: -8 to -15 globally (blue shift)
- **Split toning**: Shadows → deep blue (LAB b: -10 to -15), Highlights → neutral or very slight warm
- **Vignette**: Apply 30-50% edge darkening to enhance atmospheric effect

**OpenCV/NumPy Approximation:**
```python
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
# Global blue shift
lab[:,:,2] -= 10  # shift entire image toward blue
# Deepen shadows further
mask_shadows = lab[:,:,0] < 100
lab[:,:,2][mask_shadows] -= 5  # additional blue in shadows
# Boost blue saturation channel (proxy via absolute b-channel deviation)
lab[:,:,2] = lab[:,:,2] * 1.15 - 5
lab = np.clip(lab, 0, 255)
```

**Best Footage Type:** Cityscapes, harbors, mountain reflections, urban architecture
**Implementation Complexity:** Medium — primarily global LAB b-channel adjustment with shadow masking

---

### 1.3 harsh_midday

**Visual Description:**
High-contrast scene with blown-out highlights and deep harsh shadows. Colors appear desaturated and bleached in direct sun. Blues in sky are oversaturated. Greens look fluorescent. Requires aggressive dynamic range recovery and color restoration.

**Specific Adjustments:**
- **Highlights**: -80 to -100 (critical for sky/cloud recovery)
- **Whites**: -50
- **Shadows**: +60 to +80 (rescue underexposed shadow zones)
- **Blacks**: +30
- **Vibrance**: +40 to +60 (restore washed-out colors)
- **HSL Blue**: Saturation +30 (restore sky depth)
- **HSL Orange/Red**: Saturation +25 (warm tones washed by harsh light)
- **HSL Green**: Saturation -10 to -20, Hue +5 toward yellow (prevent neon green)
- **Contrast**: -10 (midday naturally too contrasty — bring down slightly)
- **Clarity/Texture**: +15 (micro-contrast to add depth without global contrast)
- **LAB L-curve**: Compress highlights sharply (bring top 20% toward midtone)

**Best Footage Type:** Desert plains, beach/ocean with flat light, architectural rooftops
**Implementation Complexity:** High — requires aggressive tone mapping and per-channel HSL work

---

### 1.4 overcast

**Visual Description:**
Soft, diffused light with minimal shadows. Colors are muted and slightly cool. Sky is flat white-gray. Excellent for revealing texture detail in landscapes without harsh shadows. Overall low-contrast, naturalistic, documentary feel.

**Specific Adjustments:**
- **Temperature**: -50 to -100K (slightly cool to match gray sky)
- **Tint**: -5 to -8 (slight green to counteract magenta overcast cast)
- **Contrast**: +5 to +10 (add back removed by flat light)
- **Clarity**: +20 to +30 (boost local contrast/microdetail)
- **Saturation**: -5 to -10 global (muted palette)
- **Vibrance**: +10 (boost just the least-saturated areas selectively)
- **HSL Green**: Saturation +10 (greens go flat under cloud cover)
- **HSL Sky/Blue**: Saturation -15 (grey sky looks odd with boosted blue)
- **Split toning**: None or very subtle — overcast look is neutral
- **De-haze**: +10 to +20 (often haze builds under cloud cover)
- **LAB L**: Mild compression of highlight range (sky is already diffuse)

**Best Footage Type:** Forests, greenery, waterfalls, moody coastlines
**Implementation Complexity:** Low-Medium — mostly conservative global adjustments

---

### 1.5 night_city

**Visual Description:**
Deep black shadows with isolated pools of warm artificial light. City lights in orange, yellow, red, and neon blue/purple create dramatic color contrast against dark sky. High contrast with rich blacks. Slight halation/glow around light sources.

**Specific Adjustments:**
- **Exposure**: -0.5 to -1.0 (deepen overall image)
- **Shadows**: 0 to +10 only (keep blacks rich)
- **Highlights**: +20 to +40 (allow artificial lights to breathe)
- **Contrast**: +30 to +50 (high contrast night look)
- **HSL Orange**: Saturation +30, Luminance +10 (sodium vapor streetlights)
- **HSL Yellow**: Saturation +20
- **HSL Blue/Cyan**: Saturation +25 (neon signs, LED accents)
- **Noise reduction**: Heavy luminance NR for dark areas
- **Vignette**: 40-60% (draw focus to lit areas)
- **LAB b-channel**: -5 in shadows (push dark areas toward blue-black)
- **Split toning**: Highlights → warm orange-amber, Shadows → deep blue-black
- **Halation simulation**: Slight 2px Gaussian blur on highlight-only mask, blended 10-15%

**Best Footage Type:** Urban/city flyovers, stadium events, highway patterns, bridge architecture
**Implementation Complexity:** High — requires multi-layer compositing for halation, careful NR

---

## 2. TERRAIN-AWARE GRADING

### 2.1 ocean_coastal

**Color Challenges:**
Teal/cyan water tends to compete with warm sand tones; sky and water merge confusingly in color space; green underwater zones appear muddy; horizon line can be difficult to read.

**Specific Adjustments:**
- **HSL Cyan**: Hue shift -5 toward blue (cleaner ocean blue), Saturation +20, Luminance -10
- **HSL Blue**: Saturation +15, Luminance -15 (deepen sky-water contrast)
- **HSL Orange/Yellow**: Saturation +25, Luminance +10 (sand/beach warmth)
- **Highlights**: -30 (recover specular on water surface)
- **Shadows**: +20 (restore shadow detail in wave troughs)
- **Teal-Orange split**: Shadows → teal (LAB a: -3, b: +5), Highlights → warm (b: +8)
- **De-haze**: +15 to +25 (maritime atmosphere)
- **Temperature**: Neutral to +100K (preserve natural water blue)
- **Contrast**: +15

**OpenCV HSV Approximation (OpenCV HSV: H 0-179, S 0-255):**
```python
# Boost cyan/teal water (H around 85-100 in OpenCV)
# Boost warm sand (H around 10-20 in OpenCV)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
# Teal range mask
mask_teal = (hsv[:,:,0] >= 85) & (hsv[:,:,0] <= 100)
hsv[:,:,1][mask_teal] = np.clip(hsv[:,:,1][mask_teal] * 1.2, 0, 255)
hsv[:,:,2][mask_teal] = np.clip(hsv[:,:,2][mask_teal] * 0.9, 0, 255)
```

**Best Footage Type:** Beach/coastline, island, sailing, seascape
**Implementation Complexity:** Medium

---

### 2.2 forest_jungle

**Color Challenges:**
Green balance is critical — greens easily go "electric neon" or "muddy yellow-brown." Shadows under canopy are very deep. Dappled light creates extreme dynamic range. Foliage compresses into uniform green mass from altitude.

**Specific Adjustments:**
- **HSL Green**: Hue -5 toward cyan (less neon), Saturation -10 to -15, Luminance -5
- **HSL Yellow-Green**: Saturation -15 (oversaturation culprit)
- **HSL Aqua/Cyan**: Saturation +10 (forest shadow depth)
- **Shadows**: +40 (canopy shadows are deep, lift for detail)
- **Clarity**: +25 (differentiate leaf texture from altitude)
- **S-Curve**: Gentle, pull midtones down slightly (forests compress brightness)
- **LAB a-channel**: Slight push toward red (+3) to warm greens naturally
- **Vibrance**: +15 (selective boost for the less-saturated shadow areas)
- **Temperature**: +100K (slight warm to counteract cool canopy shadow)

**Best Footage Type:** Rainforest, national park, jungle, temperate woodland
**Implementation Complexity:** Medium — careful HSL work to avoid neon greens

---

### 2.3 urban_city

**Color Challenges:**
Mix of concrete gray, glass reflections, neon signs, and sky competes for color story. Harsh shadow/highlight contrast from buildings. Concrete looks flat and lifeless without help. Neon can clip easily.

**Specific Adjustments:**
- **HSL Orange/Red**: Saturation +20 (brick, terracotta facades)
- **HSL Blue/Cyan**: Saturation +15 (glass reflections, sky)
- **Contrast**: +25 to +35 (urban = high contrast)
- **Blacks**: -20 (deepen to add edge)
- **Clarity**: +20 (architecture texture)
- **Split toning**: Shadows → cool blue (LAB b: -8), Highlights → warm neutral
- **De-haze**: +10 (urban pollution/atmosphere)
- **Teal-orange look**: Popular for cityscapes — shadows teal, warm highlights
- **Vignette**: 20-30% subtle edge darkening
- **Neon control**: HSL luminance cap on cyans/blues/magentas to prevent clipping

**Best Footage Type:** Downtown flyover, architecture, street-level perspective, rooftop views
**Implementation Complexity:** Medium-High — split toning + neon management

---

### 2.4 desert_arid

**Color Challenges:**
Orange/red earth tones can over-saturate quickly. Sand highlights easily blow out. Sky contrast with warm ground is central to the look. Colors become monochromatic and flat without careful saturation management.

**Specific Adjustments:**
- **HSL Orange**: Saturation -10 to -15 (prevent blown-out terra cotta), Luminance +5
- **HSL Red**: Saturation -5 to -10
- **HSL Yellow**: Luminance +10 (sand highlights)
- **Highlights**: -50 to -70 (sand/rock face highlights)
- **Shadows**: +20 to +30
- **Blue (sky)**: Saturation +20, Luminance -15 (deepen sky contrast with warm ground)
- **Cyan**: Slight saturation in shadow zones for atmospheric scatter
- **Temperature**: +200K (accentuate natural warmth)
- **Contrast**: +20
- **De-haze**: +20 (desert heat haze)
- **LAB b-channel**: +5 global (overall warmth push)

**Signature Color Reference:** Sedona Red #D2691E, Canyon Tan #CD853F, Arizona Blue #4169E1

**Best Footage Type:** Southwest USA, Middle East, Saharan, Australian outback
**Implementation Complexity:** Medium — primarily HSL luminance and saturation management

---

### 2.5 snow_mountain

**Color Challenges:**
Snow is inherently colorless — camera meters toward gray. Blue channel dominance from sky reflection on snow. Shadow areas turn cold blue-purple. Risk of magenta or cyan color casts. High altitude = stronger UV/blue scatter.

**Specific Adjustments:**
- **White Balance**: Daylight (5600K) or slightly warm (+50-100K) to prevent blue cast on snow
- **Highlights**: -60 to -80 (snow blows out easily)
- **Shadows**: +30 to +50 (reveal shadow snow detail)
- **HSL Blue**: Saturation -20 to -30 (reduce excessive blue sky saturation at altitude)
- **HSL Cyan**: Saturation -15 (remove unwanted cyan cast on snow shadows)
- **Tint**: +5 to +10 (slight magenta to counteract blue-green cast)
- **Vibrance**: +20 (boost rock/alpine foliage selectively)
- **Contrast**: +10 to +20
- **LAB b-channel in shadows**: -3 (subtle cool blue shadow tint is actually natural/good)
- **De-haze**: +10 to +15

**Best Footage Type:** Alpine peaks, ski resorts, polar landscapes, glacier flyovers
**Implementation Complexity:** Medium — careful white balance + blue/cyan HSL management

---

### 2.6 autumn_foliage

**Color Challenges:**
Red-orange-yellow foliage needs enhancement without going garish. Green foliage not yet turned competes and muddies the palette. Sky blue provides complementary contrast. Tree canopy from above looks like color patchwork.

**Specific Adjustments:**
- **HSL Orange**: Saturation +25 to +35, Hue -5 (push toward deeper amber), Luminance +10
- **HSL Red**: Saturation +20, Hue -8 (richer crimson)
- **HSL Yellow**: Saturation +15, Hue -10 toward orange
- **HSL Green**: Saturation -20 (reduce competing unturned leaves), Hue +5 toward yellow
- **HSL Blue (sky)**: Saturation +20, Luminance -10 (deepen sky contrast)
- **Temperature**: +100 to +200K (autumn warmth)
- **Contrast**: +20 to +25
- **Shadows**: +20 (reveal detail in dark tree shadows)
- **LAB a-channel**: +5 (slight red-green shift toward warm)
- **Split toning**: Highlights → amber/warm orange, Shadows → cool brown-blue

**Best Footage Type:** Northeast USA forests, European deciduous forests, Japanese momiji
**Implementation Complexity:** Medium — multiple HSL adjustments needed across warm hue range

---

## 3. CINEMATIC LUT EQUIVALENTS

### 3.1 Kodak 2383 (Film Print Emulation)

**Visual Look:**
Warm, rich, nostalgic 90s cinema aesthetic. "Cinematic, nostalgic, and professional." Deep blacks with subtle color tints (avoids crushed digital black). Soft gentle highlight rolloff — bright areas transition gently rather than clipping. Strong midtone contrast with excellent detail retention in both highlights and shadows. Warm saturated palette emphasizing reds and organic skin tones. Green foliage shifts toward yellow.

**Key Characteristics:**
- Highlights: Gentle rolloff — simulates film compression, not hard clip
- Shadows: Deep but not crushed, with warm/neutral tint
- Midtones: High contrast, rich color saturation
- Greens: Shift toward yellow (characteristic of 2383)
- Overall: Warm-orange bias throughout tonal range

**OpenCV/NumPy Approximation:**
```python
# Step 1: Apply S-curve with strong midtone contrast
def kodak_2383_curve(value):
    # Lift shadows gently, compress highlights, boost midtones
    x = value / 255.0
    # Approximate film toe/shoulder curve
    y = np.where(x < 0.1, x * 0.9,          # toe: slightly lifted blacks
        np.where(x > 0.85, 0.85 + (x - 0.85) * 0.6,  # shoulder: compressed highlights
        x * 1.08 - 0.04))                    # midtone: slight gain
    return np.clip(y * 255, 0, 255).astype(np.uint8)

# Step 2: Warm bias in LAB
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
lab[:,:,2] += 6   # warm b-channel push globally
lab[:,:,1] += 3   # slight red-green shift toward warm

# Step 3: Greens toward yellow (shift green hue in HSV)
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
green_mask = (hsv[:,:,0] >= 35) & (hsv[:,:,0] <= 85)
hsv[:,:,0][green_mask] += 5   # shift green toward yellow
```

**Implementation Complexity:** High — requires LUT or multi-stage curve application

---

### 3.2 ARRI LogC-to-Rec709

**Visual Look:**
Clean, clinical, highly refined cinematic baseline. Exceptional highlight preservation with smooth rolloff. Natural, accurate color reproduction without warm or cool bias. Shadow detail excellent. The "gold standard" for cinema cameras — neutral but beautiful. Often used as starting point before creative grading.

**Key Characteristics:**
- Highlights: Exceptional rolloff, Log C flatter than Rec709 baseline
- Shadows: Better shadow detail than standard Rec709
- Color: Slightly less saturated (compensates for tone mapping saturation increase)
- Tone curve: Extended toe/shoulder vs standard gamma
- Black level: Middle gray mapped differently (LogC4: gray = 28%)

**OpenCV/NumPy Approximation:**
```python
# Simulate LogC to Rec709 conversion approximation
def logc_to_rec709_approx(frame):
    # Convert to float
    f = frame.astype(np.float32) / 255.0
    # Apply approximate LogC decode (linearize the log curve)
    # LogC3 encode: linear = (10^((x - 0.385537) / 0.2471896)) - 0.00937677
    linear = np.power(10, (f - 0.385537) / 0.2471896) - 0.00937677
    linear = np.clip(linear, 0, 1)
    # Apply Rec709 gamma encode: 1.099 * linear^0.45 - 0.099
    rec709 = np.where(linear < 0.018,
                      linear * 4.5,
                      1.099 * np.power(linear, 0.45) - 0.099)
    # Slight desaturation to compensate tone mapping boost
    # (done in LAB space)
    result = np.clip(rec709 * 255, 0, 255).astype(np.uint8)
    return result
```

**Implementation Complexity:** Medium — well-documented math for LogC decode

---

### 3.3 RED IPP2 (Image Processing Pipeline 2)

**Visual Look:**
Modern, clean, highly accurate color science with improved out-of-gamut color handling. Midtones less susceptible to unrealistic hue shifts. Adjustable highlight rolloff (softer than legacy). Excellent shadow latitude (LOG3G10 encoding = 10 stops over middle gray). Neon signs and saturated colors retain plausibility rather than becoming solid blobs.

**Key Characteristics:**
- Gamut: REDWideGamutRGB — handles edge-of-gamut colors gracefully
- Log encoding: Log3G10 — 10 stops above middle gray protected
- Highlights: Smoother, adjustable rolloff vs legacy RED
- Shadows: Better preserved with natural detail
- Color accuracy: Reduced hue shift during color operations
- Neon/saturated colors: Natural saturation, no out-of-gamut clipping artifacts

**OpenCV/NumPy Approximation:**
```python
# IPP2 look: clean, accurate, slight highlight softness
def ipp2_approx(frame):
    f = frame.astype(np.float32) / 255.0
    # Log3G10 decode approximation
    # log3g10 encode: y = (log10(x * 155.975 + 1)) / log10(155.975 + 1)
    linear = (np.power(10, f * np.log10(156.975)) - 1) / 155.975
    linear = np.clip(linear, 0, 1)
    # Soft highlight rolloff (sigmoid in highlights)
    highlight_mask = linear > 0.7
    linear[highlight_mask] = 0.7 + (linear[highlight_mask] - 0.7) * 0.75
    # Apply Rec709 gamma
    rec709 = np.where(linear < 0.018, linear * 4.5,
                      1.099 * np.power(np.clip(linear, 1e-6, 1), 0.45) - 0.099)
    return np.clip(rec709 * 255, 0, 255).astype(np.uint8)
```

**Implementation Complexity:** Medium-High

---

### 3.4 Fujifilm 3513 (Positive Film Print)

**Visual Look:**
Cooler, slightly green-skewed midtones compared to Kodak 2383. More neutral palette — less aggressive warmth. Clean whites. Excellent skin tone rendition with slight magenta tint. Subtle but distinctive teal in shadow zones. Sharpness rendering on par with Kodak but less aggressive grain structure.

**Key Characteristics:**
- Highlights: Slightly cooler than 2383, very clean
- Shadows: Slight teal/cyan tint (differentiates from Kodak's warm-neutral shadows)
- Midtones: Neutral with subtle green-magenta bias
- Overall: More modern/neutral than 2383's nostalgic warmth

**OpenCV/NumPy Approximation:**
```python
# Fujifilm 3513 approximation
lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB).astype(np.float32)
# Shadows: slight teal (b- in dark zones)
shadow_mask = lab[:,:,0] < 80
lab[:,:,1][shadow_mask] -= 2   # slight green push
lab[:,:,2][shadow_mask] -= 4   # slight teal/blue push
# Highlights: cool neutral (slightly negative b)
highlight_mask = lab[:,:,0] > 200
lab[:,:,2][highlight_mask] -= 2   # very slightly cooler highlights
# Midtones: slight magenta
mid_mask = (lab[:,:,0] >= 80) & (lab[:,:,0] <= 200)
lab[:,:,1][mid_mask] += 3   # slight warm-red in midtones
lab = np.clip(lab, 0, 255).astype(np.uint8)
```

**Implementation Complexity:** Medium

---

### 3.5 Technicolor 2-Strip (Vintage Process)

**Visual Look:**
Highly stylized vintage 1920s-1940s look. Cyan-green and red-orange only — missing full blue channel creates characteristic magenta-free palette. Extremely warm, almost sepia in highlights. Deep teal-to-green in shadows. High contrast. Colors appear saturated yet limited to two complementary tones. Often used for period pieces, nostalgic mood, or deliberate vintage stylization.

**Key Characteristics:**
- Color palette: Limited — cyan/teal + orange/red dominant
- Blue channel: Suppressed/absent (replaced by overlap of red+green)
- Shadows: Deep teal-green
- Highlights: Orange-amber
- Contrast: Very high
- Saturation: Intense in the surviving color bands

**OpenCV/NumPy Approximation:**
```python
def technicolor_2strip(frame):
    b, g, r = cv2.split(frame.astype(np.float32))
    # 2-strip: layer 1 = green-cyan, layer 2 = red-orange
    # Suppress blue channel, mix into the other two
    new_r = r * 1.2 + b * 0.1   # red/orange boost from blue leakage
    new_g = g * 1.1 + b * 0.15  # green/cyan boost
    new_b = b * 0.3              # suppress blue heavily
    # High contrast S-curve
    result = cv2.merge([new_b, new_g, new_r])
    result = np.clip(result, 0, 255).astype(np.uint8)
    # Additional warm highlight shift via LAB
    lab = cv2.cvtColor(result, cv2.COLOR_BGR2LAB).astype(np.float32)
    lab[:,:,2] += 10  # warm the whole image
    lab[:,:,0] = np.clip(lab[:,:,0] * 1.1, 0, 255)  # contrast boost on L
    return cv2.cvtColor(np.clip(lab, 0, 255).astype(np.uint8), cv2.COLOR_LAB2BGR)
```

**Implementation Complexity:** Medium — primarily channel mixing with LAB overlay

---

## 4. TRENDING SOCIAL MEDIA PALETTES (2025-2026)

### 4.1 Teal-Orange Cinematic (Most Popular)

**Visual Description:**
Deep desaturated teal/cyan in shadows and cool zones (sky, water, shade) contrasted against warm orange/amber in highlights and warm zones (skin, sand, sunlight). The most widely recognized "Hollywood blockbuster" look. Extremely popular for drone content with ocean/desert/urban subjects.

**Specific Adjustments:**
- **Split toning**: Shadows → teal (HSL H: 185-195°, S: 40-60%), Highlights → orange (HSL H: 25-35°, S: 30-50%)
- **HSL Blue**: Hue shift toward teal (-10 on hue), Saturation +20
- **HSL Orange**: Hue shift toward red-orange (+5), Saturation +25
- **Global Saturation**: -10 to -15 (desaturate everything except the split tones)
- **Contrast**: +20 to +30
- **OpenCV HSV (0-179 hue)**: Teal at H≈92-97, Orange at H≈12-16

**Implementation in HSV:**
```python
# Shadows to teal, highlights to orange
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
# Shift existing blues toward teal
blue_mask = (hsv[:,:,0] >= 100) & (hsv[:,:,0] <= 130)
hsv[:,:,0][blue_mask] = 95  # teal target
hsv[:,:,1][blue_mask] = np.clip(hsv[:,:,1][blue_mask] * 1.2, 0, 255)
# Shift reds/yellows toward orange in highlights
warm_mask = (hsv[:,:,0] <= 20) | (hsv[:,:,0] >= 160)
hsv[:,:,0][warm_mask] = 15  # orange target
```

**Best For:** Ocean, desert, urban, any high-contrast subject
**Platform Fit:** Instagram Reels, YouTube, TikTok

---

### 4.2 Desaturated Moody (Dark Aesthetic 2025)

**Visual Description:**
Deep blacks, muted palette with selective color retention. Very low global saturation with only 1-2 specific hues preserved for drama (often teal sky or warm light source). Dark and brooding. Trending for "cinematic" travel content on Instagram. Works beautifully for overcast/storm aerial footage.

**Specific Adjustments:**
- **Global Saturation**: -30 to -40
- **Preserve**: Blue/cyan (sky, water) at original saturation
- **Blacks**: -40 to -60 (crush for drama)
- **Shadows**: -10 (let them stay dark)
- **Contrast**: +30 to +40
- **Tone curve**: Strong toe crush, slight highlight compression
- **Vignette**: 40-60%
- **HSL**: Reduce saturation on all channels EXCEPT blue/cyan

**OpenCV Approximation:**
```python
# Selective desaturation — keep blues
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
non_blue_mask = ~((hsv[:,:,0] >= 85) & (hsv[:,:,0] <= 130))
hsv[:,:,1][non_blue_mask] *= 0.5  # reduce saturation of non-blue
frame_desaturated = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8),
                                  cv2.COLOR_HSV2BGR)
```

**Best For:** Overcast, storm footage, moody mountain/ocean scenes
**Platform Fit:** Instagram, editorial YouTube

---

### 4.3 Warm Pastel Muted

**Visual Description:**
Soft, washed-out, slightly overexposed look with warm pastels. Lifted blacks (faded look), reduced contrast, very slight warmth. Popular for travel/lifestyle content. Dreamy and approachable rather than dramatic. Often called "film wash" or "airy" look.

**Specific Adjustments:**
- **Blacks/Lift**: +30 to +50 (fade/matte blacks — the defining characteristic)
- **Whites**: -20 to -30 (compress highlights to keep airy)
- **Contrast**: -20 to -30
- **Saturation**: -15 to -25
- **Vibrance**: +10 (selective saturation recovery)
- **Temperature**: +100 to +200K
- **Tint**: +5 (slight magenta/pink for "warm film" feel)
- **Highlights**: Warm (+3 to +5 on LAB b-channel)
- **Shadows**: Lifted to near-gray (matte base)

**Best For:** Beach, travel, destination, summer aerial content
**Platform Fit:** Instagram feed, Pinterest, lifestyle brand content

---

### 4.4 Dark Moody Neon (Cyberpunk Trend 2025)

**Visual Description:**
Nearly black shadows with electric neon accent colors (cyan, magenta, purple) from city lights or creative color grading. Very high contrast. Inspired by cyberpunk aesthetics. Popular for urban night drone footage and FPV city runs. Combines deep dark moody base with shocking neon pops.

**Specific Adjustments:**
- **Exposure**: -0.8 to -1.2
- **Blacks**: -60 to -80 (near complete black crush)
- **Contrast**: +40 to +60
- **HSL Cyan**: Saturation +50, Luminance +20 (electric neon cyan)
- **HSL Magenta/Purple**: Saturation +40 (neon pink/purple lights)
- **HSL Orange**: Saturation +30 (warm sodium vapor contrast)
- **Global saturation**: -15 (mute everything except the boosted neons)
- **Vignette**: 50-70% (deep edges)
- **Split toning**: Shadows → near-black blue, Highlights → warm-to-neon

**Best For:** Urban night, FPV city, stadium events, industrial
**Platform Fit:** TikTok, YouTube Shorts, Instagram Reels (FPV content)

---

### 4.5 Hyper-Realistic Natural (Emerging 2026 Trend)

**Visual Description:**
Countertrend to heavy grading. Faithful color reproduction prioritizing authenticity. Natural skin tones, accurate environmental colors, minimal manipulation. Still involves careful technical correction (white balance, exposure) but resists creative stylization. Associated with documentary/photojournalistic aesthetic gaining popularity as audiences grow fatigued with over-processed content.

**Specific Adjustments:**
- **White balance**: Precisely match shooting conditions (Kelvin matched)
- **Exposure**: 0 to +0.2 (natural brightness)
- **Contrast**: +5 to +10 (very subtle)
- **Saturation**: 0 to +5
- **Vibrance**: +5 to +10
- **No split toning**
- **No vignette or minimal**
- **De-noise**: Careful, preserve detail
- **De-haze**: Only if atmospheric haze present

**Best For:** Nature documentaries, conservation content, photojournalism-style aerial
**Platform Fit:** YouTube long-form, nature/wildlife channels

---

## 5. IMPLEMENTATION RECOMMENDATIONS FOR ColorGrader MODULE

### Preset Architecture

For the existing `ColorGrader` class in `/Users/matthewdeane/Documents/Data Science/python/_projects/_p-ai-drone-video/src/drone_reel/core/color_grader.py`, the following preset additions are recommended:

**New Time-of-Day Presets:**
```python
COLOR_PRESETS = {
    # Existing presets...
    "golden_hour": {
        "brightness": 8,       # +0.3 stop equivalent
        "contrast": 20,
        "saturation": 12,
        "temperature": 15,     # warm shift
        "shadow_tint": {"a": 0, "b": -4},    # LAB: cool shadows
        "highlight_tint": {"a": 3, "b": 10},  # LAB: warm highlights
        "hsv_adjustments": {
            "orange": {"s_scale": 1.20, "v_scale": 1.15},
            "yellow": {"s_scale": 1.15, "v_scale": 1.10},
            "blue": {"s_scale": 0.90},
        }
    },
    "blue_hour": {
        "brightness": -5,
        "contrast": 15,
        "saturation": 10,
        "temperature": -20,   # cool shift
        "shadow_tint": {"a": -2, "b": -12},  # deep blue shadows
        "highlight_tint": {"a": 0, "b": -3}, # neutral-cool highlights
        "hsv_adjustments": {
            "blue": {"s_scale": 1.30, "v_scale": 0.90},
            "cyan": {"s_scale": 1.20},
            "orange": {"s_scale": 1.25},  # warm lights pop
        }
    },
    "teal_orange": {
        "brightness": 0,
        "contrast": 25,
        "saturation": -10,    # global desaturate
        "shadow_tint": {"a": -3, "b": 6},    # teal shadows
        "highlight_tint": {"a": 5, "b": 12}, # orange highlights
        "hsv_adjustments": {
            "blue": {"h_shift": -10, "s_scale": 1.20},  # push to teal
            "orange": {"s_scale": 1.25},
        }
    },
    "dark_moody": {
        "brightness": -15,
        "contrast": 35,
        "saturation": -30,
        "shadow_tint": {"a": -1, "b": -8},
        "highlight_tint": {"a": 0, "b": 3},
        "lift": 0,    # keep blacks crushed
        "vignette": 0.5,
    },
    "warm_pastel": {
        "brightness": 15,
        "contrast": -25,
        "saturation": -20,
        "lift": 40,   # matte/faded blacks
        "temperature": 12,
        "shadow_tint": {"a": 2, "b": 5},
        "highlight_tint": {"a": 3, "b": 8},
    },
}
```

**New Terrain Presets to Add:**
- `ocean_coastal`, `forest_jungle`, `urban_city`, `desert_arid`, `snow_mountain`, `autumn_foliage`

**New Cinematic LUT Presets:**
- `kodak_2383`, `arri_rec709`, `red_ipp2`, `fujifilm_3513`, `technicolor_2strip`

---

## 6. RESEARCH SOURCES

1. [Unlock Cinematic Magic: DJI D-Log & D-Log M Grading 2026](https://aaapresets.com/en-in/blogs/camera-specific-color-grading-series/unlock-cinematic-magic-the-ultimate-guide-to-grading-dji-d-log-d-log-m-footage-for-aerial-brilliance-in-2026)
2. [Mastering Aerial Aesthetics: LUTs for Drone Footage 2026](https://aaapresets.com/en-gb/blogs/camera-specific-color-grading-series/mastering-aerial-aesthetics-the-ultimate-guide-to-luts-for-drone-footage-in-2026-sunsets-oceans-and-forests)
3. [Kodak 2383 LUT - Preset Curator Guide](https://presetcurator.com/kodak-2383-lut/)
4. [Print Film Emulation 2021 - Juan Melara](https://juanmelara.com.au/blog/print-film-emulation-luts-for-download)
5. [ARRI Color FAQ - Image Science](https://www.arri.com/en/learn-help/learn-help-camera-system/image-science/color-faq)
6. [ARRI Log C Curve Usage in VFX (PDF)](https://www.arri.com/resource/blob/31918/66f56e6abb6e5b6553929edf9aa7483e/2017-03-alexa-logc-curve-in-vfx-data.pdf)
7. [RED IPP2 Overview - RED Support](https://support.red.com/hc/en-us/articles/115004913827-IPP2-Overview)
8. [Complete Color Grading Arizona Drone Footage - AirAzona FPV](https://airazonafpv.com/blog/Complete_Guide_to_Color_Grading_Arizona_Drone_Footage.html)
9. [Drone Pilot Guide to Cinematic Color Correction - Dronegenuity](https://www.dronegenuity.com/pilot-guide-to-color-correcting-drone-footage/)
10. [Color Grading Trends 2025 - Beverly Boy Productions](https://beverlyboy.com/film-technology/color-grading-trends-in-2025-bold-moody-and-realistic-looks/)
11. [Orange and Teal Color Grading Guide - Kevin Raposo](https://kevinraposo.com/a-guide-to-the-orange-and-teal-look/)
12. [Image Shadow and Highlight Correction with OpenCV - GitHub Gist](https://gist.github.com/HViktorTsoi/8e8b0468a9fb07842669aa368382a7df)
13. [Lab Adjustments - RawPedia/RawTherapee](https://rawpedia.rawtherapee.com/Lab_Adjustments)
14. [Color Grading in Film - LocalEyes Video Production](https://localeyesit.com/color-grading-in-film/)
15. [ARRI REVEAL Color Science Explained - Frame.io](https://blog.frame.io/2024/06/10/arri-reveal-color-science-explained/)
