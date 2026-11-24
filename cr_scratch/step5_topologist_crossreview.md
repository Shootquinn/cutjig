## 1. Euler and genus: SIGNED

Material loop: bottom-open slits (az 82, 142, 202, 262, 322, 22) cut ring, ledge and wall up to z 29; the 3 mm top band (z 29 to 32) bridges them. Top-open slits (az 52, 112, ...) cut z >= 3; the ring and the 0.5 strip above the ledge bridge them. A closed zigzag band: one solid, genus 1, so 2 - 2g = 0 for every size.

OCC counts V - E + F = 0 + sum over faces of (excess of a non-disk face). Notch contribution, derived: dV +8 (4 floor, 4 top corners), dE +12 (4 floor, 2 wall tops, 4 wall-to-cone curves, 2 split top arcs), dF +4 (floor, 2 walls, top-face split). 8 - 12 + 4 = 0. Notch count 1 to 7 does not move euler_VEF. Label pocket adds the same increment to every size. The absolute value depends on where the seam of the outer cone falls (label az 7 +-11.3 deg covers the seam at az 0); it is identical across sizes because the builder is the same. C7 asserts equality only, which is correct. Do not assert an absolute number.

Faces that differ in count by d: none for the seven sizes. Torus lip band: 12 pieces (top-open and bottom-open slits) for z_e + 0.293 <= 29, that is every d <= 105. Chamfer band: 6 pieces. At d 106.585 the lip sits above hole top, so torus 6 pieces and each notch cuts the chamfer through (floor 29.0 below chamfer start 29.79). Envelope end only, no test builds it.

## 2. Boolean order

Within a cut, fuse tools into one compound (slits 12, holes 12, notches n). Across cuts, stay staged: the C2 contract needs per-cut before, after, tool, expected. Revolve (with lip and chamfer) first, key fuse second.

- Lip against relief hole, d <= 91.6 (d 90 is built): SIGNED, OCC-safe. Basis difference, both pass: the 0.086 is lip start 21.086 minus nominal hole bottom 21.000. The exposed hole bottom on the bore is 21.0715 (at slit wall, t 0.75). Separations are 0.015 in z (hole-to-slit-wall vertex against lip circle) and 0.075 in t (slit wall 0.75, crossing 0.825). Crossing is transversal at 11.9 deg (slope t/sqrt(16 - t^2) = 0.211). No tangency; smallest feature 0.015 is 1e5 times the 1e-7 boolean tolerance. The hole-torus intersection curve spans t 0.75 to 2.4, a normal bounded curve. Order slits, then holes, lip already revolved: as written.
- Hole top against chamfer edge, d >= 105.6: lip start 29.086 against exposed hole top 28.929: 0.157, no crossing. Pass.
- Notch against slit, notch against hole: arc gap 15 deg at r >= 43.5 is >= 4.4 mm beyond half-widths. Pass.
- Label against slit and hole: 3.0 mm lateral, 1.0 mm in z. Pass.
- Slit tool top (z 25) and bottom (z 7) faces lie on the hole axis plane inside the hole volume. Transversal edges, no coincident face. Pass.
- Key fuse: key and ring share planes z 0 and 1.995; same-domain faces, standard. Key 15 deg from nearest slit. Pass.
- Top-open hole bottom 3.0 against ledge top 2.5: 0.5. Pass.

## 3. slit_plane_faces: SIGNED, 0 by construction

The probe counts planar faces with normal.z = 0 and |n . COM| < 0.01. Planes present: slit walls at offset 0.75, notch walls 3, label sides 12, key sides 5.875, key end 70.04. Horizontal planes have |n.z| = 1. Zero.

## 4. Clamped solids: SIGNED

Slits close symmetrically about the slit centre plane (w/2 each side): w = 1.238 (Kd1), 0.584 (Kmax); the walls stay 0.58 apart, no contact face. Radial move is inward: bore, lip, chamfer, ledge by s - g; cone by s + g/cos10. Cone gap to the holder cone is 0.00508 radial, 0.005 normal, over parallel coaxial cones: no intersection curve, common volume exactly 0, below 0.01. Kmax shoulder: holder bottom z 2.0 against ring top 1.995, a 0.005 plane gap. Slit tool inner r 38 stays below the moved ledge ID (d 90 Kmax: 41.25).

## 5. Per-item result

WITHHELD on line 16 (label): "Tool = conical band (0.8/cos10 radial)" gives a tool outer face coincident with the part's outer cone. Edit: "Tool = conical band from r_out(z) - 0.8/cos10 to r_out(z) + `collet.tool_overshoot`, intersect box."

WITHHELD on lines 13 to 15 (radial extents): only the slit tool states r 38 to 72. Edit: append "Hole and notch tools span r 38 to 72 (hole axis radial, length 34); notch tool z 29 to 33."

Non-blocking: the clamped builder reuses the unclamped c and z_e.

WITHHELD: line 16, lines 13 to 15.
