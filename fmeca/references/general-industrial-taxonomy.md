# General Industrial — Cross-Sector Equipment Taxonomy & Failure Mode Library

## Table of Contents

1. [Centrifugal Pumps](#centrifugal-pumps)
2. [Positive Displacement Pumps](#pd-pumps)
3. [Electric Motors (LV)](#lv-motors)
4. [Fans & Blowers](#fans)
5. [Compressors](#compressors)
6. [Valves](#valves)
7. [Heat Exchangers](#heat-exchangers)
8. [Pressure Vessels & Tanks](#vessels)
9. [Piping Systems](#piping)
10. [HVAC Systems (Building/Plant)](#hvac)
11. [Electrical Distribution](#electrical)
12. [Instrumentation & Control](#instrumentation)
13. [Cranes & Lifting Equipment](#cranes)
14. [Fire Protection Systems](#fire)
15. [Civil & Structural](#civil)

Each class aligns with ISO 14224 equipment boundaries where applicable.

---

## 1. Centrifugal Pumps <a name="centrifugal-pumps"></a>

**ISO 14224 Boundary**: Driver, pump unit, power transmission, control/monitoring, miscellaneous

### Pump Unit
**Functions**: Deliver fluid at specified flow rate and head; contain fluid without leakage;
maintain suction and discharge pressure
**Common Failure Modes**:
- Impeller wear (erosion, corrosion, cavitation damage)
- Impeller blockage (solids, rags, debris)
- Casing wear or corrosion
- Mechanical seal failure (leakage exceeding specification)
- Gland packing failure (excessive leakage)
- Bearing failure (drive end and non-drive end)
- Shaft failure (fatigue, corrosion)
- Coupling failure
- Wear ring clearance excessive (loss of efficiency)
- Cavitation (insufficient NPSH)
- Loss of prime

**Common Causes**: Abrasive/corrosive fluid, off-BEP operation, dry running, insufficient NPSHa,
bearing lubrication failure, misalignment, pipe strain, foreign object ingress, seal face damage,
thermal shock, water hammer

---

## 2. Positive Displacement Pumps <a name="pd-pumps"></a>

### Reciprocating Pump (Piston/Plunger/Diaphragm)
**Functions**: Deliver fluid at specified flow against high pressure; provide accurate dosing
**Common Failure Modes**:
- Valve failure (suction or discharge — not seating, cracked, worn)
- Packing/seal failure (plunger leak)
- Diaphragm rupture
- Check valve failure
- Pulsation damper failure
- Plunger/piston wear
- Crankshaft bearing failure

**Common Causes**: Abrasive fluid, chemical attack, fatigue, overheating, suction starvation,
overpressure, inadequate pulsation dampening

### Rotary Pump (Gear/Screw/Lobe)
**Functions**: Deliver viscous fluid at specified flow; maintain pressure
**Common Failure Modes**:
- Rotor/gear wear (loss of volumetric efficiency)
- Shaft seal failure
- Bearing failure
- Housing wear
- Relief valve failure
- Overpressure

**Common Causes**: Fluid contamination, dry running, overpressure, bearing lubrication failure,
abrasive particles, viscosity change

---

## 3. Electric Motors (LV — <1kV) <a name="lv-motors"></a>

**Functions**: Convert electrical energy to mechanical rotary motion at specified speed and torque

**Common Failure Modes**:
- Bearing failure (noise, vibration, seizure)
- Stator winding insulation failure (turn-to-turn, phase-to-phase, phase-to-ground)
- Rotor failure (bar cracking in squirrel cage, slip ring wear in wound rotor)
- Cooling fan failure / blockage (overheating)
- Terminal box connection failure (loose, corroded)
- Shaft seal failure (contamination ingress)
- Excessive vibration
- Overheating / thermal trip

**Common Causes**: Bearing lubrication degradation, thermal ageing of insulation, voltage
imbalance, overloading, environmental contamination (dust, moisture, chemicals), misalignment
with driven equipment, excessive starts, voltage transients, inadequate ventilation

---

## 4. Fans & Blowers <a name="fans"></a>

### Centrifugal/Axial Fan
**Functions**: Move air/gas at specified volume flow and pressure; provide ventilation, cooling,
or process air
**Common Failure Modes**:
- Impeller/blade wear (erosion, corrosion)
- Impeller imbalance (vibration)
- Bearing failure
- Shaft seal failure
- Belt drive failure (if belt-driven)
- Motor failure
- Damper/vane actuator failure
- Housing corrosion
- Blade cracking or detachment

**Common Causes**: Erosive/corrosive gas, material buildup on blades, imbalance, bearing
lubrication, belt tension/alignment, fatigue, temperature extremes

---

## 5. Compressors <a name="compressors"></a>

### Reciprocating Compressor
**Functions**: Compress gas to specified pressure and flow; maintain discharge quality
**Common Failure Modes**:
- Valve failure (suction/discharge — not seating, broken)
- Piston ring wear
- Cylinder liner wear
- Packing failure (rod seal leak)
- Bearing failure (main, crosshead, crank pin)
- Intercooler failure
- Unloader failure
- Capacity control failure
- Oil carry-over

**Common Causes**: Valve fatigue, contaminated gas, inadequate lubrication, overheating,
liquid carry-over (slugging), overpressure, pulsation

### Screw Compressor
**Functions**: Compress air/gas to specified pressure; provide continuous flow
**Common Failure Modes**:
- Rotor wear or contact
- Bearing failure
- Oil separator failure (carry-over)
- Inlet valve failure
- Minimum pressure valve failure
- Thermostatic valve failure
- Air/oil cooler blockage
- Capacity control failure

**Common Causes**: Oil degradation, contamination, overheating, bearing lubrication, air filter
neglect, moisture in intake air

---

## 6. Valves <a name="valves"></a>

### Isolation Valves (Gate/Ball/Butterfly)
**Functions**: Isolate sections of pipe/equipment; provide full bore flow when open; seal when closed
**Common Failure Modes**:
- Internal leakage (seat wear, scoring, erosion)
- External leakage (stem packing, body gasket, bonnet)
- Fails to open (seized, actuator failure)
- Fails to close (obstruction, actuator failure, galling)
- Slow operation (stiff, partially seized)
- Handle/actuator failure

**Common Causes**: Corrosion, erosion, cavitation damage, infrequent operation (seizing), debris
in seat, packing degradation, galling (stainless), thermal cycling, overtorquing

### Control Valves
**Functions**: Modulate flow to maintain process variable at setpoint; respond to controller output
**Common Failure Modes**:
- Valve sticking (hysteresis, dead band)
- Seat leakage
- Stem packing leakage
- Actuator failure (diaphragm, spring, positioner)
- Positioner failure (electronic or pneumatic)
- Cavitation/flashing damage
- Trim erosion
- Fail position not achieved on air/signal loss

**Common Causes**: Process deposits, corrosion, actuator diaphragm ageing, instrument air quality,
positioner calibration drift, high pressure drop causing cavitation, packing wear

### Relief Valves (PRV/PSV)
**Functions**: Protect equipment from overpressure; open at set pressure; reseat after pressure
relieved (HIDDEN FAILURE — not evident under normal operation)
**Common Failure Modes**:
- Fails to open at set pressure (stuck closed) — HIDDEN
- Leaks below set pressure (premature opening or seat damage)
- Chattering (rapid open-close cycling)
- Fails to reseat after relieving
- Set pressure drift
- Discharge pipe blockage

**Common Causes**: Corrosion, deposit buildup on seat, spring relaxation, back-pressure issues,
process fouling, infrequent testing, incorrect set pressure

---

## 7. Heat Exchangers <a name="heat-exchangers"></a>

### Shell & Tube Heat Exchanger
**Functions**: Transfer heat between two fluids at specified duty; contain fluids without cross-
contamination; maintain approach temperature
**Common Failure Modes**:
- Tube leak (through-wall — cross contamination)
- Tube blockage (fouling, scaling, biological growth)
- Baffle damage or displacement
- Shell corrosion
- Tube sheet corrosion/erosion
- Gasket failure
- Reduced thermal performance (fouling)

**Common Causes**: Corrosion (pitting, crevice, galvanic), erosion at tube inlet, vibration-induced
fatigue, fouling, thermal cycling, water chemistry, inadequate cleaning

### Plate Heat Exchanger
**Functions**: Transfer heat efficiently in compact footprint
**Common Failure Modes**:
- Plate gasket failure (external leak or cross-contamination)
- Plate perforation (corrosion)
- Plate fouling
- Frame bolt relaxation

**Common Causes**: Chemical attack, gasket ageing, clamping pressure loss, fouling, thermal shock

---

## 8. Pressure Vessels & Tanks <a name="vessels"></a>

### Pressure Vessel
**Functions**: Contain fluid/gas at specified pressure; provide process volume; interface with
instruments and piping
**Common Failure Modes**:
- Corrosion (internal — under deposit, pitting; external — under insulation)
- Fatigue cracking (nozzle welds, saddle supports)
- Erosion (impingement areas)
- Brittle fracture (low temperature or hydrogen embrittlement)
- Relief device failure (hidden)
- Insulation failure
- Level instrument failure

**Common Causes**: Corrosive contents, thermal cycling, inadequate corrosion allowance, CUI
(corrosion under insulation), hydrogen service, fatigue, overpressure events

### Atmospheric Storage Tank
**Functions**: Store liquid at atmospheric pressure; maintain content quality
**Common Failure Modes**:
- Floor plate corrosion (underside)
- Shell corrosion (internal, external)
- Roof corrosion or structural failure
- Floor settlement
- Leak at shell-to-floor weld
- Floating roof seal failure
- Overflow (level instrument failure)

**Common Causes**: Soil-side corrosion, water bottoms, product corrosivity, foundation settlement,
coating failure, age, inadequate cathodic protection

---

## 9. Piping Systems <a name="piping"></a>

**Functions**: Transport fluid between equipment; contain fluid; resist operating pressure and
temperature
**Common Failure Modes**:
- External corrosion (atmospheric, CUI)
- Internal corrosion (uniform, pitting, erosion-corrosion)
- Flange joint leak (gasket failure, bolt relaxation)
- Threaded connection leak
- Weld defect propagation
- Vibration fatigue cracking (small-bore connections)
- Thermal expansion stress
- Water hammer damage
- Support/hanger failure

**Common Causes**: Corrosive environment/contents, CUI, vibration, thermal cycling, water
chemistry, inadequate support, flow-induced vibration, dead legs, incorrect material selection

---

## 10. HVAC Systems (Building/Plant) <a name="hvac"></a>

### Air Handling Unit (AHU)
**Functions**: Condition and distribute air to specified zones; maintain temperature, humidity, filtration
**Common Failure Modes**:
- Supply fan motor failure
- Fan bearing failure
- Belt drive failure
- Cooling coil leak or blockage
- Heating coil failure
- Filter blockage (excessive pressure drop)
- Damper actuator failure
- Condensate drain blockage
- Control system failure

**Common Causes**: Bearing lubrication, belt wear, coil fouling, filter neglect, damper mechanism
corrosion, control component failure, refrigerant leak, drain trap dry-out

### Chiller (Air/Water Cooled)
**Functions**: Provide chilled water at specified temperature and flow
**Common Failure Modes**:
- Compressor failure (motor, valves, bearings)
- Refrigerant leak
- Condenser fouling
- Evaporator fouling or freeze-up
- Expansion device failure
- Control system failure
- Oil management failure

**Common Causes**: Compressor wear, refrigerant charge loss, water treatment issues, electrical
faults, sensor failure, low flow, start-up/shutdown stress

---

## 11. Electrical Distribution <a name="electrical"></a>

### Transformer (Power)
**Functions**: Transform voltage to specified level; supply rated load
**Common Failure Modes**:
- Winding insulation failure
- Bushing failure
- Tap changer failure (OLTC)
- Oil degradation
- Cooling system failure (fans, pumps, radiators)
- Core insulation failure
- Terminal connection failure
- Tank leak

**Common Causes**: Thermal ageing, moisture ingress, oil contamination, overloading, through-faults,
lightning, tap changer mechanism wear, gasket degradation

### Switchgear (MV/LV)
**Functions**: Switch, protect, and isolate electrical circuits; interrupt fault current
**Common Failure Modes**:
- Circuit breaker fails to trip on fault (HIDDEN)
- Circuit breaker fails to close
- Relay/protection maloperation (nuisance trip or failure to operate)
- Busbar insulation failure
- Cable termination failure
- Arc flash incident
- Mechanism failure (springs, operating rod)

**Common Causes**: Mechanism lubrication, contact wear, insulation degradation, moisture/
contamination, relay calibration drift, infrequent operation, ageing

---

## 12. Instrumentation & Control <a name="instrumentation"></a>

### Transmitters (Pressure/Temperature/Flow/Level)
**Functions**: Measure process variable; transmit signal to control system; maintain specified accuracy
**Common Failure Modes**:
- Output drift (reading inaccurate)
- Output stuck (fixed value regardless of process)
- No output (signal loss)
- Erratic output (noise, spikes)
- Process connection blockage (impulse line)
- Diaphragm failure
- Electronics failure

**Common Causes**: Process fouling, impulse line blockage, vibration, temperature extremes,
corrosion, moisture ingress, EMI, component ageing, calibration drift

### PLC / DCS Controller
**Functions**: Execute control logic; process inputs/outputs; communicate with HMI and field devices
**Common Failure Modes**:
- CPU failure
- I/O module failure
- Communication failure
- Power supply failure
- Program error / corruption
- Redundancy switchover failure (HIDDEN)

**Common Causes**: Component ageing, power quality, overheating, dust, firmware bugs, network
issues, backup battery failure

### Final Control Elements (see Valves section for control valves)

---

## 13. Cranes & Lifting Equipment <a name="cranes"></a>

### Overhead Crane (EOT)
**Functions**: Lift and transport loads within building/bay; position loads precisely
**Common Failure Modes**:
- Hoist motor/brake failure
- Wire rope wear or failure
- Hook/block failure
- Bridge/trolley drive failure
- Limit switch failure (overtravel, overload) — HIDDEN
- Runway rail wear/misalignment
- Festoon/conductor system failure
- Structural fatigue (girder, end truck)

**Common Causes**: High-cycle fatigue, rope wear, brake lining wear, rail misalignment, electrical
failures, overloading, infrequent inspection of hidden safety devices

---

## 14. Fire Protection Systems <a name="fire"></a>

### Fire Detection System
**Functions**: Detect fire/smoke; raise alarm; activate suppression (HIDDEN FAILURE for most modes)
**Common Failure Modes**:
- Detector fails to alarm on genuine fire (HIDDEN)
- False alarm (nuisance activation)
- Panel failure
- Communication failure to monitoring station
- Power supply failure
- Detector contamination

**Common Causes**: Detector ageing, contamination (dust, insects), incorrect detector type,
battery failure, wiring faults, panel component failure

### Sprinkler / Deluge System
**Functions**: Suppress fire; control spread; protect structure and contents (HIDDEN FAILURE)
**Common Failure Modes**:
- Sprinkler head blockage or corrosion (HIDDEN)
- Main valve fails to open (HIDDEN)
- Jockey pump failure
- Fire pump failure (HIDDEN — only tested periodically)
- Pipe corrosion/blockage (HIDDEN)
- Alarm valve failure

**Common Causes**: Internal pipe corrosion (MIC — microbiologically influenced corrosion), valve
seizure from infrequent operation, pump maintenance neglect, system modification errors, freezing

---

## 15. Civil & Structural <a name="civil"></a>

### Building Structure (Steel)
**Functions**: Support operational loads; resist environmental loads; provide safe enclosure
**Common Failure Modes**:
- Corrosion section loss (columns, beams, connections)
- Connection failure (bolt loosening, weld cracking)
- Foundation settlement
- Impact damage
- Fire damage

**Common Causes**: Coating failure, environmental exposure, vibration, ground conditions,
vehicle/equipment impact, corrosive atmosphere

### Concrete Structures
**Functions**: Support loads; contain materials; provide foundations
**Common Failure Modes**:
- Reinforcement corrosion (chloride, carbonation)
- Concrete spalling
- Cracking (structural, shrinkage, settlement)
- Alkali-silica reaction (ASR)
- Acid attack (chemical environments)
- Foundation bearing failure

**Common Causes**: Chloride ingress, carbonation, inadequate cover, poor construction, chemical
exposure, overloading, ground movement, water ingress, age

---

## Usage Notes

- This taxonomy covers equipment found across most industrial sectors. Use in combination with
  sector-specific taxonomies for specialised items.
- ISO 14224 provides standardised boundary definitions — when in doubt about what's "inside" or
  "outside" a pump, motor, etc., refer to ISO 14224 boundaries.
- Hidden failures are marked explicitly — these are critical for RCM-based analysis and are the
  most commonly missed failure modes in practice.
- For equipment not covered here, use the hierarchy structure and failure mode style as a template,
  and adapt using OEM documentation and operating experience.
