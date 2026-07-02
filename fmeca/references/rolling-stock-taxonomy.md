# Rolling Stock / Rail — Equipment Taxonomy & Failure Mode Library

## Table of Contents

1. [Traction & Propulsion](#traction)
2. [Braking Systems](#braking)
3. [Bogie & Running Gear](#bogie)
4. [Doors & Access Systems](#doors)
5. [HVAC & Passenger Comfort](#hvac)
6. [Electrical Power & Distribution](#electrical)
7. [Pantograph & Current Collection](#pantograph)
8. [Couplers & Gangways](#couplers)
9. [Body & Structure](#body)
10. [Onboard Electronics & Control](#electronics)
11. [Auxiliary Systems](#auxiliary)

Each equipment class follows: Sub-system → Component → Typical Functions → Common Failure Modes →
Common Failure Causes/Mechanisms. Use as a starting point — always adapt to the specific vehicle type.

---

## 1. Traction & Propulsion <a name="traction"></a>

### Traction Motor
**Functions**: Convert electrical energy to mechanical torque; deliver rated torque at specified speed range
**Common Failure Modes**:
- Winding insulation breakdown (turn-to-turn, phase-to-phase, phase-to-ground)
- Bearing failure (seizure, excessive play, noise)
- Rotor bar cracking or breakage (squirrel cage motors)
- Overheating / thermal shutdown
- Loss of output torque
- Excessive vibration

**Common Causes**: Thermal cycling, moisture ingress, bearing lubrication degradation, contamination
(brake dust, water), electrical transients/surges, misalignment, age-related insulation
degradation, overloading

### Traction Inverter / Drive
**Functions**: Convert DC (or AC) supply to variable frequency AC for traction motors; regulate
motor speed and torque
**Common Failure Modes**:
- IGBT/power semiconductor failure (short circuit or open circuit)
- Gate driver circuit failure
- DC link capacitor degradation
- Control board failure
- Cooling system failure (fan, heat sink, liquid cooling)
- Communication loss with vehicle management system

**Common Causes**: Thermal stress, power cycling fatigue, voltage transients, coolant contamination,
vibration, firmware errors, EMI, age-related capacitor dry-out

### Gearbox / Transmission
**Functions**: Transmit torque from traction motor to axle; provide speed reduction at specified ratio
**Common Failure Modes**:
- Gear tooth wear (pitting, spalling, scuffing)
- Bearing failure (spalling, seizure)
- Oil seal failure (leakage)
- Shaft misalignment
- Oil degradation or loss
- Housing crack

**Common Causes**: Insufficient lubrication, contamination, overloading, misalignment, fatigue,
thermal cycling, inadequate oil change intervals

---

## 2. Braking Systems <a name="braking"></a>

### Friction Brake (Disc or Tread)
**Functions**: Convert kinetic energy to heat via friction; decelerate vehicle at specified rate;
hold vehicle stationary
**Common Failure Modes**:
- Brake pad/shoe worn below minimum thickness
- Brake disc cracked or warped
- Brake caliper seized (applied or released position)
- Uneven pad wear causing vibration
- Brake drag (incomplete release)
- Reduced braking force (below specified deceleration rate)

**Common Causes**: Normal abrasive wear, thermal stress/overheating, contamination (oil, water),
caliper slide pin corrosion, hydraulic seal failure, adjustment mechanism failure

### Magnetic Track Brake
**Functions**: Provide emergency braking by magnetic adhesion to rail; supplement friction brakes
**Common Failure Modes**:
- Electromagnetic coil open circuit
- Coil insulation failure
- Pole shoe worn below limit
- Suspension/deployment mechanism failure (fails to lower or retract)
- Reduced magnetic force

**Common Causes**: Mechanical wear on pole shoes, vibration damage to coils, wiring chafe,
corrosion, deployment mechanism fatigue

### Brake Control Unit (BCU)
**Functions**: Manage braking force distribution; implement ABS/WSP; process brake demands
**Common Failure Modes**:
- Control unit hardware failure
- Software fault / logic error
- Sensor input failure (speed, load, pressure)
- Communication bus failure
- Incorrect brake force distribution
- Wheel slide protection malfunction

**Common Causes**: Electronic component failure, software bugs, connector corrosion, vibration,
EMI, sensor contamination, power supply issues

### Pneumatic/Hydraulic Brake Circuit
**Functions**: Transmit and regulate braking pressure from BCU to caliper actuators
**Common Failure Modes**:
- Pressure loss (pipe leak, fitting failure, seal failure)
- Valve stuck open or closed
- Air dryer failure (moisture in pneumatic system)
- Accumulator pre-charge loss
- Contamination in hydraulic fluid

**Common Causes**: Vibration-induced fatigue, seal ageing, corrosion, contamination, inadequate
fluid maintenance, thermal cycling

---

## 3. Bogie & Running Gear <a name="bogie"></a>

### Bogie Frame
**Functions**: Carry and distribute vehicle load to axles; provide interface for suspension,
braking, and traction components; maintain wheel alignment
**Common Failure Modes**:
- Fatigue crack initiation at stress concentration (welds, holes, transitions)
- Crack propagation to critical length
- Corrosion-induced section loss
- Distortion affecting wheel alignment

**Common Causes**: Cyclic loading (track irregularities, curves), weld quality issues, corrosion
(salt, water), impact damage, overloading

### Wheelset (Wheel + Axle)
**Functions**: Support vehicle weight; transmit traction and braking forces; guide vehicle on track
**Common Failure Modes**:
- Wheel tread wear (flange, tread profile)
- Wheel flat (localised tread damage)
- Wheel out-of-round
- Axle fatigue crack
- Wheel bearing failure
- Tyre looseness (shrink-fit wheels)

**Common Causes**: Normal rolling contact wear, wheel slide (WSP failure), track contamination,
material defects, bearing lubrication failure, thermal overload from braking, track geometry

### Primary Suspension
**Functions**: Provide axle-to-bogie spring support; absorb high-frequency track irregularities
**Common Failure Modes**:
- Spring fatigue/fracture (coil or chevron)
- Rubber element degradation/cracking
- Damper failure (loss of damping force)
- Bump stop failure
- Suspension height out of specification

**Common Causes**: Fatigue, rubber ageing (ozone, UV, heat), damper oil leak, overloading,
foreign object damage

### Secondary Suspension
**Functions**: Provide bogie-to-body spring support; isolate passenger saloon from bogie motions
**Common Failure Modes**:
- Air spring leak or burst
- Air spring bellows cracking
- Levelling valve failure
- Lateral damper failure
- Anti-roll bar link failure

**Common Causes**: Rubber ageing, puncture/impact damage, valve contamination, fatigue, corrosion

---

## 4. Doors & Access Systems <a name="doors"></a>

### Passenger Doors (Sliding/Plug)
**Functions**: Enable safe passenger boarding/alighting; seal vehicle envelope when closed; provide
emergency egress
**Common Failure Modes**:
- Door fails to open on command
- Door fails to close fully (obstruction detection loop)
- Door opens uncommanded
- Excessive opening/closing time
- Door seal failure (air/water ingress)
- Emergency release mechanism failure
- Step/gap filler failure

**Common Causes**: Motor/actuator wear, limit switch failure, obstruction sensor fault, door
guide rail contamination/wear, control relay failure, wiring damage, vandalism, ice/debris

### Door Control Unit
**Functions**: Process open/close commands; manage sensitive edge/obstruction detection; interface
with vehicle management system for interlock
**Common Failure Modes**:
- Controller hardware failure
- Communication loss
- False obstruction detection (nuisance faults)
- Interlock signal failure
- Incorrect door status reporting

**Common Causes**: Component failure, connector corrosion, software fault, EMI, vibration

---

## 5. HVAC & Passenger Comfort <a name="hvac"></a>

### Roof-Mounted HVAC Unit
**Functions**: Maintain saloon temperature within specified range; provide ventilation; filter air
**Common Failure Modes**:
- Compressor failure (seizure, valve failure, loss of capacity)
- Refrigerant leak
- Condenser/evaporator coil blockage or corrosion
- Fan motor failure
- Heater element failure (open circuit)
- Control sensor failure (incorrect temperature reading)
- Filter blockage (reduced airflow)

**Common Causes**: Vibration fatigue on pipe joints, corrosion, compressor mechanical wear, bearing
failure, contamination, electrical failures, filter maintenance neglect

---

## 6. Electrical Power & Distribution <a name="electrical"></a>

### Auxiliary Power Supply (SIV / Static Inverter)
**Functions**: Convert traction supply to vehicle auxiliary voltages (415V AC, 24V DC, etc.)
**Common Failure Modes**:
- Output voltage out of specification
- Total output loss
- Overload shutdown
- Capacitor failure
- Cooling fan failure

**Common Causes**: Component ageing, thermal stress, overloading, contamination, vibration

### Battery System
**Functions**: Provide emergency power; support starting; buffer auxiliary loads
**Common Failure Modes**:
- Reduced capacity (below specified Ah)
- Cell failure (open circuit or short circuit)
- Excessive self-discharge
- Terminal corrosion
- Thermal runaway (lithium chemistries)

**Common Causes**: Age/cycling degradation, overcharging, deep discharge, thermal exposure,
manufacturing defect, corrosion

### Wiring & Connectors
**Functions**: Distribute electrical power and signals throughout vehicle
**Common Failure Modes**:
- Insulation chafe/damage
- Connector corrosion or looseness
- Wire fatigue fracture (at flex points)
- Short circuit
- Earth fault

**Common Causes**: Vibration, chafe against structure, moisture ingress, rodent damage, improper
routing, connector fretting, thermal cycling

---

## 7. Pantograph & Current Collection <a name="pantograph"></a>

### Pantograph
**Functions**: Maintain contact with overhead wire; collect traction current at specified force range
**Common Failure Modes**:
- Carbon strip excessive wear
- Carbon strip fracture/loss
- Loss of contact force (spring/pneumatic failure)
- Pantograph fails to raise or lower
- Excessive bounce/arcing
- Horn damage from OHW irregularity

**Common Causes**: Overhead wire condition, ice/contamination, pneumatic system failure, spring
fatigue, carbon strip material quality, incorrect static force setting

---

## 8. Couplers & Gangways <a name="couplers"></a>

### Automatic Coupler
**Functions**: Mechanically connect vehicles; provide pneumatic and electrical continuity
**Common Failure Modes**:
- Coupling mechanism failure to latch
- Uncoupling under load
- Pneumatic seal failure
- Electrical contact degradation
- Excessive coupler play

**Common Causes**: Wear, corrosion, contamination, impact damage, misalignment, seal degradation

### Gangway / Bellows
**Functions**: Provide enclosed passenger access between vehicles; weather seal
**Common Failure Modes**:
- Bellows tearing or cracking
- Floor plate failure
- Water ingress
- Excessive relative movement

**Common Causes**: Rubber/fabric ageing, UV exposure, fatigue from articulation, vandalism, debris

---

## 9. Body & Structure <a name="body"></a>

### Vehicle Body Shell
**Functions**: Contain and protect passengers; support all mounted equipment; resist crash loads
**Common Failure Modes**:
- Fatigue cracking at structural joints
- Corrosion (internal and external)
- Impact damage
- Window seal failure
- Floor delamination

**Common Causes**: Cyclic loading, water/salt ingress, collision, age, UV degradation, poor
drainage design

### Windows & Glazing
**Functions**: Provide visibility; contain passengers; resist impact loads
**Common Failure Modes**:
- Lamination failure (delamination, fogging)
- Crack or chip
- Seal failure (water leak)
- Emergency egress window mechanism failure

**Common Causes**: Impact (vandalism, stone strike), thermal stress, seal ageing, adhesive failure

---

## 10. Onboard Electronics & Control <a name="electronics"></a>

### Vehicle Management System (VMS) / Train Control Management System (TCMS)
**Functions**: Coordinate all vehicle subsystems; manage traction/braking demands; log diagnostics;
interface with driver and signalling
**Common Failure Modes**:
- Central processor failure
- Communication bus failure (MVB, Ethernet, CAN)
- Software fault / crash / hang
- Data logging failure
- Incorrect subsystem command output
- Display unit failure

**Common Causes**: Component failure, software bugs, power supply instability, EMI, overheating,
connector issues

### Passenger Information System (PIS)
**Functions**: Display destination, next stop, service information; make audio announcements
**Common Failure Modes**:
- Display blank or garbled
- Audio system failure
- GPS/location tracking failure
- Incorrect information displayed

**Common Causes**: LCD/LED failure, amplifier failure, GPS antenna issue, data feed error,
vibration damage to connectors

---

## 11. Auxiliary Systems <a name="auxiliary"></a>

### Sanding System
**Functions**: Dispense sand to wheel-rail interface to improve adhesion
**Common Failure Modes**:
- Sand hopper empty (inadequate filling)
- Sand nozzle blocked
- Sand valve failure
- Incorrect sand delivery rate
- Wet sand bridging in hopper

**Common Causes**: Moisture ingress, contamination, valve wear, nozzle alignment, supply chain
issues, environmental conditions

### Windscreen Wiper & Washer
**Functions**: Maintain driver visibility in precipitation
**Common Failure Modes**:
- Wiper motor failure
- Blade deterioration (streaking, chattering)
- Washer pump failure
- Washer fluid reservoir empty/frozen

**Common Causes**: Motor wear, rubber degradation (UV, age), pump failure, fluid maintenance neglect

### Fire Detection & Suppression
**Functions**: Detect fire/smoke; alert crew; suppress fire (where fitted)
**Common Failure Modes**:
- Detector failure to alarm on genuine fire (hidden failure)
- False alarm (nuisance activation)
- Suppression system fails to discharge (hidden failure)
- Suppression agent depleted/leaked

**Common Causes**: Detector contamination, sensor ageing, wiring fault, agent leak past seals,
pressure loss, incorrect detector type for environment

---

## Usage Notes

- This taxonomy is based on typical light rail and tram vehicles (e.g. Bombardier/Alstom Citadis
  class, Siemens Combino/Flexity). Adapt for specific vehicle types.
- Heavy rail (locomotive-hauled, DMU, EMU) will have additional systems: engine/powertrain (diesel),
  fuel system, exhaust aftertreatment, specific signalling interfaces (ETCS/ATP).
- Freight rolling stock omits passenger-specific systems but adds wagon-specific items: bogie
  centre plates, side bearers, hand brakes, hopper/gondola mechanisms.
- Always confirm the actual system configuration with the client before assuming this taxonomy applies.
