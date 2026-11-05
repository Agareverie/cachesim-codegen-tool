# CacheSim Codegen Tool

Python-based tooling for code generation, benchmarking, and visualization for a cache simulator written in C. This software is developed for **2190250 Computer Architecture and Organization** in Chulalongkorn University.

## Overview

This project explores the behavior and performance of different cache organizations and replacement policies through simulation.

The simulator supports three cache configurations:

- `direct-mapped`: Each memory block maps to exactly one cache line.
- `least-recently-used`: An N-way set-associative cache that replaces the least recently accessed cache line.
- `Round Robin`: An N-way set-associative cache that selects replacement candidates in a cyclic order.

A Python utility package handles configuration, C code generation, and visualization of simulation results.

## Requirements

- [uv](https://docs.astral.sh/uv/)
- Python 3.14
- Clang or GCC
- [mise](https://mise.jdx.dev/) (optional)
- clang-format (optional)

## Getting Started

Clone the repository:

```bash
git clone <repository-url>
cd <repository-directory>
```

### Option 1: Using uv

uv can automatically download and manage Python versions required by the project.

Install uv if you haven't already:

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Install Python 3.14 explicitly:

```bash
uv python install 3.14
```

Install the project dependencies:

```bash
uv sync
```

uv will create the project's virtual environment and install the required dependencies.

### Option 2: Using mise

Install mise following its [installation instructions](https://mise.jdx.dev/getting-started.html).

Install the project tools:

```bash
mise use uv@latest
```

This adds the selected tool versions to `mise.toml`. Then install the project dependencies:

```bash
mise install
uv sync
```

Both setup methods result in the same development environment and support the commands described below.

## Usage

The project provides separate CLI commands for plotting simulation results and generating C code.

### Code Generation

Generate and bulk-compile C code for a particular cache organization:

```bash
uv run codegen direct-mapped
uv run codegen least-recently-used
uv run codegen round-robin
```

### Bulk Execution

Run the compiled binaries and save their data into their respective CSV file:

```bash
uv run execute-all direct-mapped
uv run execute-all least-recently-used
uv run execute-all round-robin
```

Data is saved to the project's data directory.

### Plotting

Generate visualizations from simulation results:

```bash
uv run plot direct-mapped
uv run plot least-recently-used
uv run plot round-robin
```

### Everything

Or you can just do all 3 of them at the same time:

```bash
uv run everything 
```

Plots are saved to the project's plots directory.

## Cache Configuration

Cache geometry is derived from cache size, block size, and associativity.

| Property | Formula |
|---|---|
| Cache size | $C$ |
| Block size | $B$ |
| Associativity | $A$ |
| Index size | $S = C / (B \cdot A)$ |
| Offset length | $O = \log_2(B)$ |
| Index length | $I = \log_2(S)$ |
| Tag length | $T = 32 - I - O$ |

Direct-mapped caches use an associativity of one. Set-associative caches use the configured number of ways.

## Acknowledgements

- **Krerk Piromsopa Ph.D.** for creating the [original Cache Simulator source code](https://www.cp.eng.chula.ac.th/~krerk/books/Computer%20Architecture/CacheSim) used in the project. The original code has been modified by me and my friend to allow modern C compilers to compile without any warnings or errors.