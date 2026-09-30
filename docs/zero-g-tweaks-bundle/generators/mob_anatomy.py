"""Anatomy refinements inside the silhouettes specified by the mob sheets.

The source boxes remain the authority for overall size. Small ears, nostrils,
paw/hoof/toe shapes and joint subdivisions make each species readable in close
views. No vanilla model or texture is redistributed.
"""

from mobs_data import both

EXTRA = {
    "crystal_stag": both(
        ("Ears", -5, 25, -10, -2, 27, -8, "fur_lt", "fur"),
        ("Inner ears", -4.5, 25.4, -10.15, -2.5, 26.6, -10, "belly", "noise"),
        ("Nostrils", -1.1, 22.6, -15.15, -0.5, 23.2, -15, "hoof", "noise")),
    "dust_grazer": both(
        ("Ears", -7, 15, -11, -4, 17, -9, "mane", "fur"),
        ("Nostrils", -2.4, 11, -18.15, -1.3, 12, -18, "hoof", "noise")),
    "frost_yak": both(
        ("Ears", -6, 15, -11, -4, 17, -9, "wool_dk", "fur"),
        ("Muzzle", -3.5, 10, -17, -0.2, 13, -16, "face", "noise"),
        ("Nostrils", -2.6, 11.4, -17.1, -1.6, 12.2, -17, "hoof", "noise")),
    "cinder_hound": both(
        ("Nostrils", -1.6, 11, -15.2, -0.5, 11.8, -15, "jaw", "noise"),
        ("Fangs", -1.7, 8.7, -14.7, -1.1, 10.3, -14.1, "claw", "noise")),
    "rime_stalker": [
        ("Muzzle", -2, 9, -14, 2, 11.5, -12, "fur_dk", "fur"),
        ("Nose", -1, 10.7, -14.2, 1, 11.5, -14, "claw", "noise")],
    "moon_hopper": [
        ("Muzzle", -1.5, 5.8, -6.25, 1.5, 7.2, -6, "fluff_dk", "fur"),
        ("Incisors", -0.6, 5.4, -6.4, 0.6, 6.5, -6.2, "fluff", "noise")],
    "azure_fowl": both(
        ("Toes", -2.5, 0, -2, -1.8, 0.8, 1, "beak", "noise"),
        ("Toes", -1.6, 0, -2, -0.9, 0.8, 1, "beak", "noise")),
    "slag_boar": both(
        ("Ears", -4.5, 12.5, -11, -2.5, 15, -9, "bristle", "fur"),
        ("Nostrils", -1.6, 7, -16.2, -0.6, 8, -16, "hoof", "noise")),
    "scorch_wyrmling": [
        ("Lower jaw", -2, 5, -11, 2, 6.5, -7, "belly", "noise")]
        + both(("Nostrils", -1.8, 8, -10.2, -0.9, 8.6, -10, "horn", "noise")),
    "regolith_crawler": both(
        ("Antennae", -4.5, 5, -13, -4, 8, -12, "mand", "noise")),
    "rust_beetle": both(
        ("Antennae", -3.5, 6, -10, -3, 9, -9, "leg", "noise")),
    "sand_skitter": both(
        ("Pincer", -5, 3.5, -11, -3.5, 5.5, -8, "carapace_dk", "noise")),
    "gildcrab": both(
        ("Pincer finger", -10, 4, -12, -8.5, 5.5, -10, "claw", "noise"),
        ("Pincer thumb", -7.5, 6.5, -12, -6, 8, -10, "shell_hi", "noise")),
    "glimmerfish": [
        ("Mouth", -0.8, 5.5, -5.15, 0.8, 6, -5, "scale_dk", "noise")],
    "deep_eel": [
        ("Lower tail", -1, 4.5, 14, 1, 7, 19, "skin_dk", "stripes")],
    "bog_lurker": both(
        ("Toes", -7.7, 0, -8.5, -6.8, 1, -5.5, "moss", "noise"),
        ("Toes", -5.8, 0, -8.5, -4.9, 1, -5.5, "moss", "noise")),
    "rift_tyrant": both(
        ("Fangs", -4.8, 18.5, -21.8, -3.6, 22, -20.6, "horn", "noise"),
        ("Brow", -6.4, 27, -20.5, -1.5, 28.5, -19.5, "hide", "noise")),
}


def refine_boxes(key: str, spec: dict) -> list[tuple]:
    if key=="dune_burrower":
        # Original low desert arthropod inspired by Silverfish, not its vanilla mesh.
        result=[("Head",-2.5,1,-10,2.5,4.5,-6,"seg_dk","chitin"),
                ("Mouth",-1.3,1.4,-10.08,1.3,2.2,-10,"maw","noise")]
        for index,(width,height,z0,z1) in enumerate(((7,5,-6,-2),(8,5.5,-2,2),(6,4.5,2,5),(4.5,3.5,5,8),(2.5,2.5,8,11))):
            result.append((f"Segment {index}",-width/2,1,z0,width/2,height,z1,"seg" if index%2==0 else "seg_dk","chitin"))
            if index<3:
                result+=both((f"Legs segment {index}",-width/2-1.5,.3,z0+.5,-width/2+.2,1.5,z0+1.5,"seg_dk","noise"))
        result+=both(("Antennae",-2.4,3,-13,-1.9,3.5,-9.9,"teeth","noise"))
        result.append(("Tail",-.5,1,11,.5,1.6,14,"seg_dk","noise"))
        return result
    result = []
    prior = "body"
    for raw in spec["boxes"]:
        label, x0, y0, z0, x1, y1, z1, material, pattern = raw
        prior = label or prior
        label = label or prior
        # Knees/hocks are child bones, so bending them keeps the foot attached.
        if "legs" in label.lower() and y1-y0 >= 6:
            knee = round((y0 + (y1-y0)*0.46)*4)/4
            result.append(("Upper " + label, x0, knee, z0, x1, y1, z1, material, pattern))
            result.append(("Lower " + label, x0+0.15, y0, z0+0.1, x1-0.15, knee, z1-0.1, material, pattern))
        else:
            result.append((label, x0, y0, z0, x1, y1, z1, material, pattern))
    result.extend(EXTRA.get(key, []))
    # Give long-legged animals a contact patch without changing overall height.
    if key in {"cinder_hound", "rime_stalker", "slag_boar", "scorch_wyrmling", "ash_strider", "rift_tyrant"}:
        material = next((p for p in ("hoof", "claw", "leg", "hide_dk") if p in spec["pal"]), next(iter(spec["pal"])))
        for raw in list(result):
            label, x0,y0,z0,x1,y1,z1,_,_ = raw
            if label and label.startswith("Lower "):
                result.append(("Feet", x0-0.2, y0, z0-0.5, x1+0.2, y0+1.2, z1+0.2, material, "noise"))
    return result
