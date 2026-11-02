# Platform and Embedded Constraints

> Status: **TBD** — the lead will describe the platform.
> `TBD` / `[ASSUMPTION]` items are derived from the existing repository being worked on and recorded in its `MEMORY.md` (AGENTS.md, section 1, "Adapting to existing repositories").

## Hardware Platform

| Parameter | Value |
|---|---|
| MCU / SoC | TBD |
| Core, clock | TBD |
| Flash / RAM | TBD |
| Board | TBD |

## Software Platform

| Parameter | Value |
|---|---|
| RTOS / bare-metal | TBD |
| HAL / SDK | TBD |
| Languages | C, C++ |
| Compiler, version | TBD |
| Build system | **CMake** |
| Unit tests | **GoogleTest / GoogleMock**, host build (see [testing.md](testing.md)) |
| Debugger / programmer | TBD |

## Commands

```sh
# build
TBD
# flash
TBD
# tests (host) — see testing.md
cmake -S . -B build-host -DBUILD_TESTING=ON && cmake --build build-host && ctest --test-dir build-host --output-on-failure
```

## Code Constraints

TBD. Typical questions to fill in:
- Dynamic memory (`malloc`/`new`) — allowed?
- Exceptions, RTTI, STL — allowed?
- ISR rules (duration, allowed calls)
- Stack budget, firmware size
- `volatile`, atomicity, critical sections
