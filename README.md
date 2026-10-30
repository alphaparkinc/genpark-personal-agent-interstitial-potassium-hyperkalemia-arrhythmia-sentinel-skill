# Interstitial Potassium & Hyperkalemia Arrhythmia Sentinel Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `monitor_hyperkalemia_arrhythmia_risk`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Cross-analyzes interstitial/serum potassium levels against ECG morphometric features (T-wave peaking, T/R amplitude ratio, PR prolongation) to guard against lethal arrhythmias.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Electrolyte Cardioprotection)`

## MCP Tool Specification
### `monitor_hyperkalemia_arrhythmia_risk`
Parameters:
- `potassium_meq_l` (float): Serum or validated interstitial potassium level (mEq/L)
- `t_wave_amplitude_mv` (float): Peak amplitude of ECG T-wave in precordial leads (mV)
- `r_wave_amplitude_mv` (float): Amplitude of preceding R-wave (mV)
- `pr_interval_ms` (float): PR interval in milliseconds
- `qrs_duration_ms` (float): QRS complex duration in milliseconds

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-interstitial-potassium-hyperkalemia-arrhythmia-sentinel-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-interstitial-potassium-hyperkalemia-arrhythmia-sentinel-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
